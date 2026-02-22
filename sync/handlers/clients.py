"""
Handler for syncing clients.
"""

import requests
from typing import Dict, Optional
import logging
from datetime import datetime

from utils.config import COMMON_HEADERS, COMMON_URL
from utils.common import clean_phone, calculate_time
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
        phones = data.get('phones', [])
        phone = clean_phone(phones[0]) if phones and phones[0] else None
        
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
            try:
                if isinstance(bday, (int, float)):
                    birthday = datetime.fromtimestamp(bday).strftime('%Y-%m-%d')
                elif isinstance(bday, str):
                    birthday = bday
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

