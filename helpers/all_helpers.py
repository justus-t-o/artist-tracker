import requests 

def paginate_requests(url, headers, params, item_key, pagination_key):
    all_responses = []

    
    while url:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"error paginating requests: {response.json()}")

        data = response.json()
        all_responses.extend(data[item_key])
        url = data.get(pagination_key)
        params = None
    
    return all_responses