from typing import Dict
from .base import BaseHandler

class ClientHandler(BaseHandler):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.endpoint = 'import/clients-api'

    def clean_phone(self, phone: str) -> str:
        """Clean phone number"""
        if not phone:
            return None
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) == 9:
            return '996' + phone
        elif len(phone) == 10 and phone[0] == '0':
            return '996' + phone[1:]
        elif len(phone) == 12:
            return phone
        return None

    def process_name(self, name: str) -> tuple:
        """Process name into first_name and last_name"""
        name_parts = name.strip().split()
        if len(name_parts) >= 3:
            return f"{name_parts[0]} {name_parts[1]}", name_parts[2]
        elif len(name_parts) == 2:
            return name_parts[0], name_parts[1]
        return name, ""

    def clean_client(self, data: Dict) -> Dict:
        """Clean client data"""
        phone = self.clean_phone(data.get('phones', [None])[0])
        last_name, first_name = self.process_name(data['name'])

        return {
            'cloudshop_id': data['_id'],
            'phone': phone,
            'first_name': first_name,
            'last_name': last_name,
            'gender': data.get('sex', 'female') or 'female',
            'created': data['created'],
            'birthday': data.get('birthday', '2100-01-01'),
            'bonus_balance': data.get('bonus_balance', 0),
            'bonus_spent': data.get('bonus_spent', 0),
            'discount_percent': data.get('discount_percent'),
            'is_added': True,
            'registered': True
        }

    def create(self, data: Dict):
        """Create new client"""
        client = self.clean_client(data)
        self.make_api_request(self.endpoint, data={'data': [client]})

    def update(self, data: Dict):
        """Update existing client"""
        client = self.clean_client(data)
        self.make_api_request(self.endpoint, data={'data': [client]})