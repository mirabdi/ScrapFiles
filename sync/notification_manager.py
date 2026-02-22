"""
Central coordinator for notification-based incremental sync.
Manages state, fetches notifications, and dispatches to handlers.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import requests

from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


@dataclass
class SyncState:
    """Track sync progress"""
    last_notification_id: Optional[str] = None
    last_sync_timestamp: Optional[float] = None
    processed_count: int = 0
    error_count: int = 0


class NotificationManager:
    """
    Manages notification-based incremental sync.
    
    Features:
    - Checkpoint-based state persistence
    - Resource-type routing
    - Error handling and retry logic
    - Batch processing
    """
    
    # Resource type to handler mapping
    RESOURCE_HANDLERS = {
        'sales': 'docs',
        'return_sales': 'docs',
        'purchases': 'docs',
        'return_purchases': 'docs',
        'movements': 'docs',
        'changes': 'docs',
        'clients': 'clients',
        'catalog': 'products',
        'suppliers': 'suppliers',
        'stores': 'stores',
        'registers': 'registers',
        'shifts': 'shifts',
    }
    
    def __init__(
        self, 
        company_id: str = "57c09c3b3ce7d59d048b46c9",
        state_file: str = "data/sync_state.json",
        batch_size: int = 100
    ):
        self.company_id = company_id
        self.state_file = Path(state_file)
        self.batch_size = batch_size
        self.logger = logging.getLogger(__name__)
        
        # Load sync state
        self.state = self._load_state()
        
    def _load_state(self) -> SyncState:
        """Load sync state from file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return SyncState(**data)
            except Exception as e:
                self.logger.error(f"Failed to load state: {e}")
        return SyncState()
    
    def _save_state(self):
        """Persist sync state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def fetch_notifications(
        self, 
        limit: int = 10000,
        offset: int = 0
    ) -> List[Dict]:
        """
        Fetch notifications from CloudShop API.
        
        Args:
            limit: Maximum number of notifications to fetch
            offset: Pagination offset
            
        Returns:
            List of notification objects
        """
        params = {
            "path": f"/{self.company_id}/notifications/{offset}/{limit}",
            "api": "v3",
            "timezone": "32400",
        }
        
        try:
            response = requests.get(
                COMMON_URL, 
                params=params, 
                headers=COMMON_HEADERS,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            notifications = data.get('data', [])
            
            self.logger.info(
                f"Fetched {len(notifications)} notifications "
                f"(offset={offset}, limit={limit})"
            )
            
            return notifications
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch notifications: {e}")
            return []
    
    def extract_entity_ids(
        self, 
        notifications: List[Dict]
    ) -> Dict[str, Set[str]]:
        """
        Extract cloudshop_ids grouped by resource type.
        
        Args:
            notifications: List of notification objects
            
        Returns:
            Dict mapping resource_type -> set of cloudshop_ids
        """
        entity_ids = {}
        
        for notification in notifications:
            resource = notification.get('resource')
            method = notification.get('method')
            data = notification.get('data', {})
            
            # Skip if not a tracked resource
            if resource not in self.RESOURCE_HANDLERS:
                continue
            
            # Extract cloudshop_id from notification
            cloudshop_id = None
            
            # Try to get ID from data object (full data may be in notification)
            if isinstance(data, dict):
                cloudshop_id = data.get('_id')
            
            # Fallback to notification _id if data._id missing
            if not cloudshop_id:
                cloudshop_id = notification.get('_id')
            
            if not cloudshop_id:
                self.logger.warning(
                    f"Notification missing cloudshop_id: {notification.get('_id')}"
                )
                continue
            
            # Group by resource type
            handler_type = self.RESOURCE_HANDLERS[resource]
            
            if handler_type not in entity_ids:
                entity_ids[handler_type] = set()
            
            entity_ids[handler_type].add(cloudshop_id)
        
        self.logger.info(
            f"Extracted IDs: {', '.join(f'{k}: {len(v)}' for k, v in entity_ids.items())}"
        )
        
        return entity_ids
    
    def process_notifications(
        self, 
        notifications: List[Dict],
        handlers: Dict[str, 'BaseHandler']
    ) -> Dict[str, int]:
        """
        Process notifications and sync entities.
        
        Args:
            notifications: List of notifications to process
            handlers: Dict of resource handlers
            
        Returns:
            Stats dict with counts per resource type
        """
        stats = {}
        
        # Extract entity IDs by resource type
        entity_ids_by_resource = self.extract_entity_ids(notifications)
        
        # Process each resource type
        for handler_type, cloudshop_ids in entity_ids_by_resource.items():
            if handler_type not in handlers:
                self.logger.warning(f"No handler for {handler_type}")
                continue
            
            handler = handlers[handler_type]
            
            try:
                # Fetch and sync entities
                result = handler.sync_entities(list(cloudshop_ids))
                stats[handler_type] = result
                self.state.processed_count += result.get('processed', 0)
                
            except Exception as e:
                self.logger.error(
                    f"Failed to process {handler_type}: {e}",
                    exc_info=True
                )
                self.state.error_count += len(cloudshop_ids)
                stats[handler_type] = {'error': str(e)}
        
        # Update state with last notification ID
        if notifications:
            last_notification = max(
                notifications, 
                key=lambda n: n.get('date', 0)
            )
            self.state.last_notification_id = last_notification.get('_id')
            self.state.last_sync_timestamp = datetime.now().timestamp()
        
        self._save_state()
        
        return stats
    
    def sync(
        self, 
        handlers: Dict[str, 'BaseHandler'],
        limit: int = 10000
    ) -> Dict[str, int]:
        """
        Main sync method: fetch notifications and process.
        
        Args:
            handlers: Dict of resource handlers
            limit: Max notifications to process per run
            
        Returns:
            Stats dict with processing results
        """
        self.logger.info("Starting notification sync...")
        
        # Fetch notifications
        notifications = self.fetch_notifications(limit=limit)
        
        if not notifications:
            self.logger.info("No new notifications")
            return {}
        
        # Process notifications
        stats = self.process_notifications(notifications, handlers)
        
        self.logger.info(f"Sync completed: {stats}")
        
        return stats

