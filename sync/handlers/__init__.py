"""
Resource handlers for different entity types.
"""

from .base import BaseHandler
from .docs import DocHandler
from .clients import ClientHandler

__all__ = ['BaseHandler', 'DocHandler', 'ClientHandler']

