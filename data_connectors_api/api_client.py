import csv
from datetime import datetime
import json
import requests
from requests.auth import HTTPBasicAuth, AuthBase
from urllib.parse import urlparse, parse_qs
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from data_connectors_api.config import (
    CONFLUENCE_API_TOKEN, CONFLUENCE_EMAIL, CONFLUENCE_DOMAIN,
    SLACK_API_TOKEN, NOTION_SECRET
)

class BaseAPIClient:
    def save_to_json(self, data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filename

    def save_to_csv(self, data, filename=None, fieldnames=None):
        if not data:
            raise ValueError("No data to save")
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.csv"
        if not fieldnames and isinstance(data[0], dict):
            fieldnames = list(data[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return filename


class ConfluenceAPIClient(BaseAPIClient):
    def __init__(self, email=None, api_token=None, domain=None):
        self.email = email or CONFLUENCE_EMAIL
        self.api_token = api_token or CONFLUENCE_API_TOKEN
        self.domain = domain or CONFLUENCE_DOMAIN
        self.base_url = f"https://{self.domain}/wiki/api/v2"
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {"Accept": "application/json"}

    def _process_pages(self, pages):
        return [{
            'id': p.get('id'),
            'title': p.get('title'),
            'spaceId': p.get('spaceId'),
            'creatorId': p.get('creatorId'),
            'createdAt': p.get('createdAt'),
            'version': p.get('version', {}).get('number'),
            'contentLength': len(p.get('body', {}).get('storage', {}).get('value', ''))
        } for p in pages]

    def save_all_pages(self, json_file=None, csv_file=None):
        pages = self.get_all_pages()
        json_path = self.save_to_json(pages, json_file)
        processed = self._process_pages(pages)
        csv_path = self.save_to_csv(processed, csv_file, ['id','title','spaceId','creatorId','createdAt','version','contentLength'])
        return json_path, csv_path

    def _request(self, method, endpoint, params=None):
        response = requests.request(
            method,
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            auth=self.auth,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        return self._request('GET', endpoint, params)

    def get_paginated(self, endpoint, params=None):
        results = []
        next_endpoint = endpoint
        next_params = params.copy() if params else {}
        
        while True:
            response = self.get(next_endpoint, params=next_params)
            results.extend(response.get('results', []))
            
            next_link = response.get('_links', {}).get('next')
            if not next_link:
                break
            
            parsed = urlparse(next_link)
            next_endpoint = parsed.path
            next_params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        
        return results

    def get_all_pages(self):
        return self.get_paginated('/pages')

    def get_all_blog_posts(self):
        return self.get_paginated('/blogposts')

    def get_all_spaces(self):
        return self.get_paginated('/spaces')

    def get_attachments_for_page(self, page_id):
        return self.get_paginated(f'/pages/{page_id}/attachments')

class BearerTokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request

class SlackAPIClient(BaseAPIClient):
    def __init__(self, bot_token=None):
        self.bot_token = bot_token or SLACK_API_TOKEN
        self.base_url = "https://slack.com/api"
        self.session = requests.Session()
        self.session.auth = BearerTokenAuth(self.bot_token)
        self.session.headers.update({"Content-Type": "application/json"})
        
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def _process_channels(self, channels):
        return [{
            'id': c.get('id'),
            'name': c.get('name'),
            'is_private': c.get('is_private'),
            'num_members': c.get('num_members'),
            'created': c.get('created')
        } for c in channels]

    def save_all_channels(self, json_file=None, csv_file=None):
        channels = self.list_channels()
        json_path = self.save_to_json(channels, json_file)
        processed = self._process_channels(channels)
        csv_path = self.save_to_csv(processed, csv_file, ['id','name','is_private','num_members','created'])
        return json_path, csv_path
    
    def _handle_response(self, response):
        data = response.json()
        if not data.get('ok'):
            error = data.get('error', 'unknown_error')
            if error == 'ratelimited':
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._handle_response(response)
            raise requests.exceptions.HTTPError(f"Slack API error: {error}")
        return data

    def _request(self, method, endpoint, params=None):
        response = self.session.request(method, f"{self.base_url}{endpoint}", params=params)
        return self._handle_response(response)

    def get_paginated(self, endpoint, data_key, params=None):
        results = []
        next_cursor = None
        params = params.copy() if params else {}
        
        while True:
            if next_cursor:
                params['cursor'] = next_cursor
            response = self._request('GET', endpoint, params=params)
            results.extend(response.get(data_key, []))
            next_cursor = response.get('response_metadata', {}).get('next_cursor')
            if not next_cursor:
                break
        return results

    def list_channels(self):
        return self.get_paginated('/conversations.list', 'channels', {'types': 'public_channel,private_channel'})

    def get_users(self):
        return self.get_paginated('/users.list', 'members')
