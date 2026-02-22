# Notification-Based Incremental Sync Implementation Guide

## Overview

This guide proposes a notification-driven incremental sync architecture that replaces the current bulk-fetch approach. Instead of uploading everything every time, the system will:

1. Fetch recent notifications from CloudShop
2. Extract entity IDs (`cloudshop_id`) from notifications
3. Fetch only new/updated entities by their IDs
4. Batch upload only changed data to Balapan backend

## Architecture Design

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│              Notification Sync Manager                    │
├─────────────────────────────────────────────────────────┤
│  • Fetch notifications (incremental with checkpoint)     │
│  • Extract and group by resource type                   │
│  • Dispatch to resource handlers                         │
│  • Track sync state (last_notification_id)              │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  Docs    │   │ Clients │   │ Products │
  │ Handler  │   │ Handler │   │ Handler  │
  └──────────┘   └──────────┘   └──────────┘
```

### Key Benefits

- **Efficiency**: Only fetch/sync changed entities
- **Scalability**: Handle large datasets without time windows
- **Real-time**: Process notifications as they arrive
- **Resilience**: Checkpoint-based state for crash recovery
- **Cost-effective**: Reduced API calls and bandwidth

## Implementation Structure

### 1. Notification Manager (`sync/notification_manager.py`)

```python
"""
Central coordinator for notification-based incremental sync.
Manages state, fetches notifications, and dispatches to handlers.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
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
        
        # Initialize handlers (lazy import to avoid circular deps)
        self.handlers = {}
        
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
                json.dump({
                    'last_notification_id': self.state.last_notification_id,
                    'last_sync_timestamp': self.state.last_sync_timestamp,
                    'processed_count': self.state.processed_count,
                    'error_count': self.state.error_count,
                }, f, indent=2)
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
            
            # Try to get ID from data object
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
```

### 2. Base Handler (`sync/handlers/base.py`)

```python
"""
Base class for resource handlers.
Each resource type (docs, clients, products) extends this.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests

from utils.config import BASE_URL


class BaseHandler(ABC):
    """
    Base handler for syncing resources.
    
    Subclasses must implement:
    - fetch_entity(cloudshop_id) -> Dict
    - clean_entity(data) -> Dict
    - get_endpoint() -> str
    """
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def fetch_entity(self, cloudshop_id: str) -> Optional[Dict]:
        """
        Fetch full entity data from CloudShop by cloudshop_id.
        
        Args:
            cloudshop_id: Entity ID in CloudShop
            
        Returns:
            Entity data dict or None if not found
        """
        pass
    
    @abstractmethod
    def clean_entity(self, data: Dict) -> Dict:
        """
        Transform CloudShop data to Balapan format.
        
        Args:
            data: Raw entity data from CloudShop
            
        Returns:
            Cleaned entity data for Balapan
        """
        pass
    
    @abstractmethod
    def get_endpoint(self) -> str:
        """
        Get Balapan API endpoint for this resource.
        
        Returns:
            Endpoint path (e.g., '/docs/api/mass-create-update')
        """
        pass
    
    def batch_upload(
        self, 
        entities: List[Dict],
        batch_size: int = 10
    ) -> Dict[str, int]:
        """
        Upload entities to Balapan in batches.
        
        Args:
            entities: List of cleaned entities
            batch_size: Number of entities per batch
            
        Returns:
            Stats dict with created/updated/error counts
        """
        endpoint = self.get_endpoint()
        url = f"{self.base_url}{endpoint}"
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for i in range(0, len(entities), batch_size):
            batch = entities[i:i + batch_size]
            
            try:
                response = requests.post(
                    url,
                    json=batch,
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse response (adjust based on your API format)
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, dict):
                    if 'statuses' in result:
                        # Format: {"statuses": [{"action": "create", ...}]}
                        for status in result['statuses']:
                            action = status.get('action', 'error')
                            if action == 'create':
                                created_count += 1
                            elif action == 'update':
                                updated_count += 1
                            else:
                                error_count += 1
                    elif 'created' in result:
                        # Format: {"created": 5, "updated": 3}
                        created_count += result.get('created', 0)
                        updated_count += result.get('updated', 0)
                else:
                    # Assume all succeeded if no details
                    created_count += len(batch)
                
            except requests.RequestException as e:
                self.logger.error(
                    f"Batch upload failed: {e}\n"
                    f"Batch size: {len(batch)}\n"
                    f"First entity: {batch[0].get('cloudshop_id', 'unknown')}"
                )
                error_count += len(batch)
        
        return {
            'created': created_count,
            'updated': updated_count,
            'errors': error_count,
            'total': len(entities)
        }
    
    def sync_entities(
        self, 
        cloudshop_ids: List[str]
    ) -> Dict[str, int]:
        """
        Fetch, clean, and upload entities.
        
        Args:
            cloudshop_ids: List of cloudshop IDs to sync
            
        Returns:
            Stats dict with processing results
        """
        self.logger.info(f"Syncing {len(cloudshop_ids)} entities...")
        
        entities = []
        failed_ids = []
        
        # Fetch and clean entities
        for cloudshop_id in cloudshop_ids:
            try:
                raw_entity = self.fetch_entity(cloudshop_id)
                if not raw_entity:
                    self.logger.warning(
                        f"Entity not found: {cloudshop_id}"
                    )
                    failed_ids.append(cloudshop_id)
                    continue
                
                cleaned_entity = self.clean_entity(raw_entity)
                entities.append(cleaned_entity)
                
            except Exception as e:
                self.logger.error(
                    f"Failed to process {cloudshop_id}: {e}",
                    exc_info=True
                )
                failed_ids.append(cloudshop_id)
        
        # Batch upload
        if entities:
            upload_stats = self.batch_upload(entities)
        else:
            upload_stats = {
                'created': 0,
                'updated': 0,
                'errors': len(failed_ids),
                'total': 0
            }
        
        return {
            'processed': len(entities),
            'failed': len(failed_ids),
            **upload_stats
        }
```

### 3. Doc Handler (`sync/handlers/docs.py`)

```python
"""
Handler for syncing documents (sales, purchases, movements, etc.)
"""

import json
import requests
from typing import Dict, Optional
import logging

from utils.config import COMMON_HEADERS, COMMON_URL
from .base import BaseHandler
from docs.docs_utils import (
    handle_sale,
    handle_return_sale,
    handle_purchase,
    handle_return_purchase,
    handle_movement,
    handle_change
)
from docs.docs import get_consultant


class DocHandler(BaseHandler):
    """Handler for document resources"""
    
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.company_id = "57c09c3b3ce7d59d048b46c9"
    
    def fetch_entity(self, cloudshop_id: str) -> Optional[Dict]:
        """
        Fetch document from CloudShop.
        
        Args:
            cloudshop_id: Document ID
            
        Returns:
            Document data or None
        """
        params = {
            "path": f"/docs/{self.company_id}/{cloudshop_id}",
            "api": "v3",
            "timezone": "32400",
        }
        
        try:
            response = requests.get(
                COMMON_URL,
                headers=COMMON_HEADERS,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json().get('data', [])
            if data:
                return data[0]  # API returns list, get first item
            
            return None
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch doc {cloudshop_id}: {e}")
            return None
    
    def clean_entity(self, data: Dict) -> Dict:
        """
        Transform document data to Balapan format.
        
        Args:
            data: Raw document from CloudShop
            
        Returns:
            Cleaned document for Balapan
        """
        doc_type = data.get('type')
        
        # Route to appropriate handler
        if doc_type == 'sales':
            doc = handle_sale(data)
        elif doc_type == 'return_sales':
            doc = handle_return_sale(data)
        elif doc_type == 'purchases':
            doc = handle_purchase(data)
        elif doc_type == 'return_purchases':
            doc = handle_return_purchase(data)
        elif doc_type == 'movements':
            doc = handle_movement(data)
        elif doc_type == 'changes':
            if isinstance(data.get('products'), list):
                doc = handle_change(data)
            else:
                raise ValueError(f"Invalid changes doc: {data.get('_id')}")
        else:
            raise ValueError(f"Unknown doc type: {doc_type}")
        
        # Add common fields
        doc['shift_id'] = data.get('_shift')
        doc['register_id'] = data.get('_register')
        doc['bonus_cashback'] = data.get('bonus_cashback', 0)
        doc['bonus_spent'] = data.get('bonus_spent', 0)
        doc['bonus_discount'] = data.get('bonus_discount', 0)
        doc['status'] = data.get('status')
        doc['deleted'] = data.get('deleted', False)
        
        # Extract consultant from comment
        comment = data.get('comment', '')
        doc['comment'] = comment
        doc['kkm'] = '111' in comment
        doc['consultant'] = get_consultant(doc)
        
        # Limit positions if too many
        if len(doc.get('positions', [])) > 100:
            doc['positions'] = doc['positions'][:100]
        
        return doc
    
    def get_endpoint(self) -> str:
        return '/docs/api/mass-create-update'
```

### 4. Client Handler (`sync/handlers/clients.py`)

```python
"""
Handler for syncing clients.
"""

import requests
from typing import Dict, Optional
import logging

from utils.config import COMMON_HEADERS, COMMON_URL
from .base import BaseHandler


class ClientHandler(BaseHandler):
    """Handler for client resources"""
    
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.company_id = "57c09c3b3ce7d59d048b46c9"
    
    def fetch_entity(self, cloudshop_id: str) -> Optional[Dict]:
        """Fetch client from CloudShop"""
        params = {
            "path": f"/data/{self.company_id}/clients/{cloudshop_id}",
            "api": "v3",
            "timezone": "32400",
        }
        
        try:
            response = requests.get(
                COMMON_URL,
                headers=COMMON_HEADERS,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get('data')
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch client {cloudshop_id}: {e}")
            return None
    
    def clean_entity(self, data: Dict) -> Dict:
        """Transform client data to Balapan format"""
        from utils.common import clean_phone, calculate_time
        
        phones = data.get('phones', [])
        phone = clean_phone(phones[0] if phones else None) if phones else None
        
        # Parse name into first/last
        name = data.get('name', '').strip()
        name_parts = name.split()
        if len(name_parts) >= 2:
            first_name = ' '.join(name_parts[:-1])
            last_name = name_parts[-1]
        else:
            first_name = name
            last_name = ''
        
        # Format birthday
        birthday = None
        bday = data.get('bday')
        if bday:
            from datetime import datetime
            try:
                birthday = datetime.fromtimestamp(bday).strftime('%Y-%m-%d')
            except:
                pass
        
        return {
            'cloudshop_id': data.get('_id'),
            'phone': phone,
            'first_name': first_name,
            'last_name': last_name,
            'gender': data.get('sex', 'female') or 'female',
            'created': calculate_time(data.get('created')),
            'birthday': birthday or '2100-01-01',
            'bonus_balance': data.get('bonus_balance', 0),
            'bonus_spent': data.get('bonus_spent', 0),
            'discount_percent': data.get('discount', 0),
            'is_added': True,
            'registered': True
        }
    
    def get_endpoint(self) -> str:
        return '/import/clients-api'
```

### 5. Main Entry Point (`sync/main.py`)

```python
"""
Main entry point for notification-based sync.
"""

import argparse
import logging
from typing import Dict

from .notification_manager import NotificationManager
from .handlers.docs import DocHandler
from .handlers.clients import ClientHandler
from .handlers.products import ProductHandler
from utils.config import BASE_URL


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/sync.log'),
            logging.StreamHandler()
        ]
    )


def main(limit: int = 10000):
    """
    Main sync function.
    
    Args:
        limit: Maximum notifications to process per run
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize manager
    manager = NotificationManager()
    
    # Initialize handlers
    handlers = {
        'docs': DocHandler(BASE_URL),
        'clients': ClientHandler(BASE_URL),
        'products': ProductHandler(BASE_URL),
        # Add more handlers as needed
    }
    
    # Run sync
    try:
        stats = manager.sync(handlers, limit=limit)
        logger.info(f"Sync completed: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Sync failed: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Notification-based incremental sync'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10000,
        help='Maximum notifications to process'
    )
    
    args = parser.parse_args()
    main(limit=args.limit)
```

### 6. Integration with `balapan.py`

Update `balapan.py` to use notification-based sync:

```python
from sync.main import main as sync_notifications
from sync.notification_manager import NotificationManager

def main(skip_load):
    # Option 1: Replace existing scrappers with notification sync
    if not skip_load:
        # Run notification-based sync
        stats = sync_notifications(limit=10000)
        print(f"Sync stats: {stats}")
        return
    
    # Option 2: Hybrid approach - run full sync periodically
    from datetime import datetime
    from_date = datetime(2025, 10, 27)
    to_date = datetime.now()
    
    # Run notification sync for recent changes
    sync_notifications(limit=10000)
    
    # Run full sync periodically (e.g., once per day)
    # scrape_docs(skip_load, from_date, to_date)
```

## Backend API Design (Balapan)

### Recommended Endpoints

```python
# Django/Flask example structure

# 1. Bulk Create/Update Endpoint
POST /docs/api/mass-create-update
Body: [{"cloudshop_id": "...", ...}, ...]
Response: {
    "statuses": [
        {"cloudshop_id": "...", "action": "create|update|error", ...}
    ],
    "summary": {"created": 5, "updated": 3, "errors": 0}
}

# 2. Check Endpoint (Optional - for deduplication)
POST /docs/api/check
Body: {"cloudshop_ids": ["id1", "id2", ...]}
Response: {
    "exists": ["id1"],  # IDs already in DB
    "missing": ["id2"]  # IDs not in DB
}
```

### Backend Handler Example (Django)

```python
# backend/api/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def mass_create_update_docs(request):
    """
    Handle bulk document create/update.
    Uses cloudshop_id to determine create vs update.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        docs = json.loads(request.body)
        
        statuses = []
        created_count = 0
        updated_count = 0
        
        for doc_data in docs:
            cloudshop_id = doc_data.get('cloudshop_id')
            
            # Check if document exists
            try:
                doc = Document.objects.get(cloudshop_id=cloudshop_id)
                # Update existing
                for key, value in doc_data.items():
                    setattr(doc, key, value)
                doc.save()
                statuses.append({
                    'cloudshop_id': cloudshop_id,
                    'action': 'update'
                })
                updated_count += 1
                
            except Document.DoesNotExist:
                # Create new
                doc = Document.objects.create(**doc_data)
                statuses.append({
                    'cloudshop_id': cloudshop_id,
                    'action': 'create'
                })
                created_count += 1
        
        return JsonResponse({
            'statuses': statuses,
            'summary': {
                'created': created_count,
                'updated': updated_count,
                'total': len(docs)
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

## Best Practices

### 1. Error Handling
- Retry logic with exponential backoff
- Dead letter queue for failed entities
- Comprehensive logging

### 2. Performance
- Parallel fetching using ThreadPoolExecutor
- Batch processing for API calls
- Connection pooling

### 3. State Management
- Atomic state updates
- Backup state files
- Recovery from crashes

### 4. Monitoring
- Metrics: processed, failed, rate
- Alerts for sync failures
- Dashboard for sync status

## Migration Strategy

1. **Phase 1**: Implement notification sync alongside existing scrappers
2. **Phase 2**: Run both in parallel, compare results
3. **Phase 3**: Switch primary sync to notifications
4. **Phase 4**: Keep full sync as backup (weekly/monthly)

## Testing

```python
# tests/test_notification_sync.py

def test_notification_extraction():
    manager = NotificationManager()
    notifications = [
        {
            'resource': 'sales',
            'data': {'_id': 'doc123'},
            '_id': 'notif1'
        }
    ]
    
    entity_ids = manager.extract_entity_ids(notifications)
    assert 'docs' in entity_ids
    assert 'doc123' in entity_ids['docs']

def test_doc_handler():
    handler = DocHandler(BASE_URL)
    # Mock fetch_entity
    # Test clean_entity
    # Verify format
```

## Usage

```bash
# Run notification sync
python -m sync.main --limit 10000

# Or integrate into balapan.py
python balapan.py --notification-sync
```

This architecture provides a scalable, efficient solution for incremental synchronization based on notifications.

