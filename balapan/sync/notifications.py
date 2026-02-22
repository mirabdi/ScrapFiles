# sync/notifications.py
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
import requests

from .handlers.base import BaseHandler
from .handlers.clients import ClientHandler
from .handlers.docs import DocHandler
from .config import COMMON_HEADERS, COMMON_URL, BASE_URL, SERVER_MODE

logger = logging.getLogger(__name__)

class NotificationManager:
    HANDLERS = {
        'sales': DocHandler,
        'return_sales': DocHandler,
        'purchases': DocHandler,
        'return_purchases': DocHandler,
        'clients': ClientHandler,
    }

    def __init__(self):
        self.common_headers = COMMON_HEADERS
        self.common_url = COMMON_URL
        self.base_url = BASE_URL
        self.org_id = "57c09c3b3ce7d59d048b46c9"  # Store in config
        self.sync_state_file = 'data/sync_state.json'

    def load_sync_state(self) -> Dict:
        """Load sync state from file"""
        try:
            with open(self.sync_state_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'last_notification_id': None}

    def save_sync_state(self, state: Dict):
        """Save sync state to file"""
        with open(self.sync_state_file, 'w') as f:
            json.dump(state, f)

    def fetch_notifications(self, offset: int = 0, limit: int = 15) -> List[Dict]:
        """Fetch notifications from Cloudshop API"""
        try:
            params = {
                "path": f"/{self.org_id}/notifications/{offset}/{limit}",
                "api": "v3",
                "timezone": "32400",
            }
            response = requests.get(
                self.common_url,
                headers=self.common_headers,
                params=params
            )
            response.raise_for_status()
            return response.json()['data']
        except requests.RequestException as e:
            logger.error(f"Failed to fetch notifications: {str(e)}")
            return []

    def get_handler(self, resource: str) -> Optional[BaseHandler]:
        """Get appropriate handler for the resource"""
        handler_class = self.HANDLERS.get(resource)
        if handler_class:
            return handler_class(base_url=self.base_url)
        return None

    def process_notification(self, notification: Dict) -> bool:
        """Process a single notification"""
        try:
            resource = notification['resource']
            method = notification['method']
            data = notification['data']
            notification_id = notification['_id']

            handler = self.get_handler(resource)
            if not handler:
                logger.warning(f"No handler for resource: {resource}")
                return False

            if method == 'POST':
                handler.create(data)
            elif method == 'PUT':
                handler.update(data)
            
            # Save the last processed notification ID
            state = self.load_sync_state()
            state['last_notification_id'] = notification_id
            self.save_sync_state(state)

            return True

        except Exception as e:
            logger.error(f"Failed to process notification: {str(e)}")
            return False

    def sync_loop(self, interval: int = 60):
        """Main sync loop"""
        while True:
            try:
                state = self.load_sync_state()
                last_notification_id = state.get('last_notification_id')

                notifications = self.fetch_notifications()
                
                if not notifications:
                    time.sleep(interval)
                    continue

                # Process only new notifications
                if last_notification_id:
                    notifications = [n for n in notifications if n['_id'] > last_notification_id]

                for notification in notifications:
                    self.process_notification(notification)

            except Exception as e:
                logger.error(f"Sync loop error: {str(e)}")
                time.sleep(interval)
