from typing import Dict, List
from .base import BaseHandler

class DocHandler(BaseHandler):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.doc_types = {
            'sales': 'sales',
            'return_sales': 'return_sales',
            'purchases': 'purchases',
            'return_purchases': 'return_purchases'
        }
        self.endpoint = 'docs/api/mass-create-update'

    def clean_positions(self, products: List[Dict]) -> List[Dict]:
        """Clean positions data"""
        cleaned_positions = []
        for product in products:
            cleaned_pos = {
                'cloudshop_id': product['_id'],
                'quantity': abs(product['qty']),  # Convert negative to positive
                'sum': product['sum'],
                'sub': product['sub'],
                'price': product['price'],
                'discount_sum': product.get('discount_sum', 0),
                'discount_percent': product.get('discount_percent', 0)
            }
            cleaned_positions.append(cleaned_pos)
        return cleaned_positions

    def clean_doc(self, data: Dict) -> Dict:
        """Clean document data"""
        doc = {
            'style': data['type'],
            'number': data['number'],
            'cloudshop_id': data['_id'],
            'store': data['store'],
            'date': data['date'],
            'created': data['created'],
            'client': data.get('_contragent'),
            'sum': data['sum'],
            'positions': self.clean_positions(data['products']),
            'shift_id': data.get('_shift'),
            'register_id': data.get('_register'),
            'bonus_cashback': data.get('bonus_cashback', 0),
            'bonus_spent': data.get('bonus_spent', 0),
            'bonus_discount': data.get('bonus_discount', 0),
            'status': data['status'],
            'comment': data.get('comment', ''),
        }

        # Extract consultant from comment if present
        comment = data.get('comment', '')
        consultant = None
        if '@' in comment:
            consultant = comment.split('@')[1].split()[0]
            if consultant == 'undefined':
                consultant = None
        doc['consultant'] = consultant

        return doc

    def create(self, data: Dict):
        """Create new document"""
        doc = self.clean_doc(data)
        self.make_api_request(self.endpoint, data=[doc])

    def update(self, data: Dict):
        """Update existing document"""
        doc = self.clean_doc(data)
        self.make_api_request(self.endpoint, data=[doc])