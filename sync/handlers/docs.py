"""
Handler for syncing documents (sales, purchases, movements, etc.)
"""

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
        
        # Get consultant (pass original data with store info)
        consultant_doc = {
            'store': data.get('store'),
            'comment': comment
        }
        doc['consultant'] = get_consultant(consultant_doc)
        
        # Limit positions if too many
        if len(doc.get('positions', [])) > 100:
            doc['positions'] = doc['positions'][:100]
        
        return doc
    
    def get_endpoint(self) -> str:
        return '/docs/api/mass-create-update'

