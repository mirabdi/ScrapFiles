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

