# Notification-Based Incremental Sync

## Overview

This module provides an efficient notification-driven incremental sync system that replaces the bulk-fetch approach. Instead of uploading everything every time, it:

1. Fetches recent notifications from CloudShop
2. Extracts entity IDs (`cloudshop_id`) from notifications  
3. Fetches only new/updated entities by their IDs
4. Batch uploads only changed data to Balapan backend

## Quick Start

```bash
# Run notification-based sync
python -m sync.main --limit 10000

# Or via balapan.py
python balapan.py --notifications --limit 10000
```

## Architecture

- **NotificationManager**: Central coordinator that fetches notifications and dispatches to handlers
- **BaseHandler**: Abstract base class for all resource handlers
- **DocHandler**: Handles documents (sales, purchases, movements, etc.)
- **ClientHandler**: Handles client entities
- **State Management**: Tracks sync progress via `data/sync_state.json`

## Key Features

✅ **Efficiency**: Only syncs changed entities  
✅ **Scalability**: No time window limitations  
✅ **Resilience**: Checkpoint-based state recovery  
✅ **Batch Processing**: Optimized API calls  

## Adding New Handlers

1. Create a new handler class extending `BaseHandler`
2. Implement `fetch_entity()`, `clean_entity()`, and `get_endpoint()`
3. Register in `NotificationManager.RESOURCE_HANDLERS`
4. Add to handlers dict in `sync/main.py`

See `docs/NOTIFICATION_BASED_SYNC.md` for detailed implementation guide.

## State Management

Sync state is persisted in `data/sync_state.json`:
- `last_notification_id`: Last processed notification ID
- `last_sync_timestamp`: Timestamp of last sync
- `processed_count`: Total entities processed
- `error_count`: Total errors encountered

## Error Handling

- Failed entities are logged but don't stop the sync
- Retry logic can be added to handlers
- Dead letter queue for persistent failures (future enhancement)

