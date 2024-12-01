import requests

def get_nested_value(data, keys):
    """Retrieve a nested value from a dictionary using a list of keys."""
    for key in keys:
        data = data.get(key, {})
    return data

def paginate_requests(url, headers, params, item_key, pagination_key):
    """
    Function to paginate API requests and handle nested keys.
    
    Args:
        url (str): The API endpoint URL.
        headers (dict): HTTP headers for the request.
        params (dict): Query parameters for the request.
        item_key (list): List of keys for nested items to extract.
        pagination_key (str): Key for the next page URL.

    Returns:
        list: Aggregated items from paginated responses.
    """
    all_responses = []

    while url:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error paginating requests: {response.json()}")

        data = response.json()
        items = get_nested_value(data, item_key)
        if isinstance(items, list):
            all_responses.extend(items)
        else:
            raise Exception(f"Expected list at {item_key}, got {type(items).__name__}")

        url = data.get(pagination_key)
        params = None  

    return all_responses
