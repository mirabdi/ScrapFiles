"""
Main entry point for notification-based sync.
"""

import argparse
import logging
from pathlib import Path
from typing import Dict

from .notification_manager import NotificationManager
from .handlers.docs import DocHandler
from .handlers.clients import ClientHandler
from utils.config import BASE_URL


def setup_logging():
    """Configure logging"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'sync.log'),
            logging.StreamHandler()
        ]
    )


def main(limit: int = 10000) -> Dict:
    """
    Main sync function.
    
    Args:
        limit: Maximum notifications to process per run
        
    Returns:
        Stats dict with processing results
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize manager
    manager = NotificationManager()
    
    # Initialize handlers
    handlers = {
        'docs': DocHandler(BASE_URL),
        'clients': ClientHandler(BASE_URL),
        # Add more handlers as needed (products, suppliers, etc.)
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

