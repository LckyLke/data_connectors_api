import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse, parse_qs

from confluence_api.config import CONFLUENCE_API_TOKEN, CONFLUENCE_EMAIL, CONFLUENCE_DOMAIN

class ConfluenceAPIClient:
    """
    A reusable client for Confluence REST API v2 with pagination support and default query parameters.
    """

    def __init__(self, email=None, api_token=None, domain=None, default_query_params=None):
        self.email = email or CONFLUENCE_EMAIL
        self.api_token = api_token or CONFLUENCE_API_TOKEN
        self.domain = domain or CONFLUENCE_DOMAIN
        self.base_url = f"https://{self.domain}/wiki/api/v2"
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {"Accept": "application/json"}
        self.default_query_params = default_query_params.copy() if default_query_params else {}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        # Merge default query parameters with the provided ones
        merged_params = self.default_query_params.copy()
        if params:
            merged_params.update(params)
        response = requests.get(url, headers=self.headers, auth=self.auth, params=merged_params)
        response.raise_for_status()  
        return response.json()

    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return True

    def get_paginated(self, endpoint, params=None):
        """
        Fetches all paginated results from a Confluence API endpoint.
        
        Args:
            endpoint (str): The API endpoint to fetch data from.
            params (dict, optional): Query parameters for the initial request.
        
        Returns:
            list: Aggregated results from all pages.
        """
        results = []
        next_endpoint = endpoint
        next_params = params.copy() if params else {}
        
        while True:
            response = self.get(next_endpoint, params=next_params)
            current_results = response.get('results', [])
            results.extend(current_results)
            
            next_link = response.get('_links', {}).get('next')
            if not next_link:
                break
            
            parsed = urlparse(next_link)
            next_endpoint = parsed.path
            query_params = parse_qs(parsed.query)
            next_params = {k: v[0] for k, v in query_params.items()}
        
        return results

    # Example specific methods for common endpoints
    def get_all_pages(self, params=None):
        return self.get_paginated('/pages', params=params)
    
    def get_all_blog_posts(self, params=None):
        return self.get_paginated('/blogposts', params=params)
    
    def get_attachments_for_page(self, page_id, params=None):
        endpoint = f'/pages/{page_id}/attachments'
        return self.get_paginated(endpoint, params=params)