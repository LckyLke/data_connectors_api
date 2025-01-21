import requests
from requests.auth import HTTPBasicAuth

from confluence_api.config import CONFLUENCE_API_TOKEN, CONFLUENCE_EMAIL, CONFLUENCE_DOMAIN

class ConfluenceAPIClient:
    """
    A reusable client for Confluence REST API v2.
    """

    def __init__(self, email=None, api_token=None, domain=None):
        self.email = email or CONFLUENCE_EMAIL
        self.api_token = api_token or CONFLUENCE_API_TOKEN
        self.domain = domain or CONFLUENCE_DOMAIN
        self.base_url = f"https://{self.domain}/wiki/api/v2"
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {"Accept": "application/json"}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, auth=self.auth, params=params)
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
