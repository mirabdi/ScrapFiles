from typing import Dict, Any
from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

# Constants
API_ENDPOINTS = {
    'CREATE_UPDATE': f'{BASE_URL}/parties/api/clients/create-update/',
    'DELETE': f'{BASE_URL}/parties/api/clients/delete/'
}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s || %(levelname)s || %(message)s')
logger = logging.getLogger(__name__)

def api_request(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make an API request to the specified endpoint.
    
    Args:
        endpoint (str): The API endpoint to send the request to.
        data (Dict[str, Any]): The data to send in the request.
    
    Returns:
        Dict[str, Any]: The JSON response from the API.
    """
    try:
        response = requests.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return {'status': 1, 'error': str(e)}

def log_operation(operation: str, client: Dict[str, Any], response: Dict[str, Any]):
    """
    Log the result of a client operation.
    
    Args:
        operation (str): The operation performed (create, update, or delete).
        client (Dict[str, Any]): The client data.
        response (Dict[str, Any]): The API response.
    """
    log_message = f"{operation} || {client['name']} || {client['cloudshop_id']} || {response}"
    if response['status'] != 0:
        logger.warning(log_message)
    else:
        logger.info(log_message)

def create_update_client(client: Dict[str, Any]):
    """Create or update a client."""
    response = api_request(API_ENDPOINTS['CREATE_UPDATE'], client)
    log_operation("clients.create_update", client, response)

def delete_client(client: Dict[str, Any]):
    """Delete a client."""
    response = api_request(API_ENDPOINTS['DELETE'], client)
    log_operation("clients.delete", client, response)

def extract_client_data(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant client data from the notification item.
    
    Args:
        item (Dict[str, Any]): The notification data.
    
    Returns:
        Dict[str, Any]: Extracted client data.
    """
    birthday = calculate_time(item.get('bday'))
    if birthday:
        birthday = f"{dt.datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S').date()}"

    return {
        'cloudshop_id': item.get('_id'),
        'name': item.get('name'),
        'gender': item.get('sex'),
        'created': calculate_time(item.get('created')),
        'discount': item.get('discount', 0),
        'discount_card': item.get('discount_card'),
        'phone': item.get('phones', [None])[0],
        'birthday': birthday,
        'description': item.get('description'),
    }

def handle_client(notification: Dict[str, Any]):
    """
    Handle a client notification.
    
    Args:
        notification (Dict[str, Any]): The notification data.
    """
    method = notification['method']
    client = extract_client_data(notification['data'])

    if method in ['POST', 'PUT']:
        create_update_client(client)
    elif method == 'DELETE':
        delete_client(client)
    else:
        logger.warning(f"Unknown method: {method}")