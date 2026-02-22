from abc import ABC, abstractmethod
from typing import Dict
import requests
import logging

logger = logging.getLogger(__name__)

class BaseHandler(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def create(self, data: Dict):
        pass

    @abstractmethod
    def update(self, data: Dict):
        pass

    def make_api_request(self, endpoint: str, method: str = 'POST', data: Dict = None) -> Dict:
        """Make API request to Django backend"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
