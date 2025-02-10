import json
import os
import requests
from typing import Dict, List, Optional
from data_connectors_api.config import NOTION_SECRET

class NotionAPIClient:
    def __init__(self):
        self.api_key = NOTION_SECRET
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, url: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        response = requests.request(method, url, headers=self.headers, params=params, json=data)
        response.raise_for_status()
        print(response.json())
        return response.json()

    def get_all_pages(self) -> List[Dict]:
        all_pages = []
        start_cursor = None
        while True:
            body = {
                "filter": {
                    "property": "object",
                    "value": "page"
                },
                "page_size": 100
            }
            if start_cursor:
                body["start_cursor"] = start_cursor
            response = self._make_request("POST", f"{self.base_url}/search", data=body)
            all_pages.extend(response.get("results", []))
            if not response.get("has_more", False):
                break
            start_cursor = response.get("next_cursor")
        return all_pages

    def get_block_children(self, block_id: str) -> List[Dict]:
        all_blocks = []
        start_cursor = None
        while True:
            params = {"page_size": 100}
            if start_cursor:
                params["start_cursor"] = start_cursor
            response = self._make_request("GET", f"{self.base_url}/blocks/{block_id}/children", params=params)
            blocks = response.get("results", [])
            all_blocks.extend(blocks)
            if not response.get("has_more", False):
                break
            start_cursor = response.get("next_cursor")
        return all_blocks

    def get_all_blocks(self, block_id: str) -> List[Dict]:
        blocks = self.get_block_children(block_id)
        for block in blocks:
            if block.get("has_children", False):
                block_id = block["id"]
                children = self.get_all_blocks(block_id)
                block["children"] = children
        return blocks

    def save_all_pages(self, output_dir: str = "pages") -> None:
        os.makedirs(output_dir, exist_ok=True)
        pages = self.get_all_pages()
        for page in pages:
            page_id = page["id"]
            try:
                blocks = self.get_all_blocks(page_id)
                page_data = {
                    "page": page,
                    "blocks": blocks
                }
                filename = os.path.join(output_dir, f"{page_id}.json")
                with open(filename, "w") as f:
                    json.dump(page_data, f, indent=2, ensure_ascii=False)
                print(f"Saved page {page_id} to {filename}")
            except Exception as e:
                print(f"Failed to process page {page_id}: {e}")
