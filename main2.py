import os
from requests.auth import HTTPBasicAuth
import requests
import json

# Fetch from environment variables
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
EMAIL = "lukefriedrichs@gmail.com"
CONFLUENCE_DOMAIN = "lukefriedrichs.atlassian.net"

# v2 endpoint for pages
BASE_URL = f"https://{CONFLUENCE_DOMAIN}/wiki/api/v2"
PAGES_ENDPOINT = f"{BASE_URL}/pages"

def get_all_pages(email, api_token, url):
    """
    Retrieves all pages from Confluence, handling pagination.
    Returns a list of minimal page objects (ID, title, etc.).
    """
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}
    
    limit = 100  
    all_pages = []
    params = {"limit": limit}
    
    response = requests.get(url, headers=headers, auth=auth, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching pages: {response.status_code} - {response.text}")
        return []
    
    data = response.json()
    pages_batch = data.get("results", [])
    all_pages.extend(pages_batch)
    
    return all_pages

def get_page_data(email, api_token, page_id):
    url = f"{BASE_URL}/pages/{page_id}?body-format=atlas_doc_format"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching page {page_id}: {response.status_code} - {response.text}")
        return None

def main():
    # 1. Fetch all pages (IDs, titles, etc.) - minimal info
    if not API_TOKEN:
        print("Error: API token is not set. Please set CONFLUENCE_API_TOKEN environment variable.")
        return
    
    all_pages = get_all_pages(EMAIL, API_TOKEN, PAGES_ENDPOINT)
    print(f"Total pages found: {len(all_pages)}")
    
    # 2. Fetch expanded data for each page
    knowledge_base = []
    for page in all_pages:
        page_id = page.get("id")
        title = page.get("title")
        
        # Retrieve expanded page data
        page_expanded_data = get_page_data(EMAIL, API_TOKEN, page_id)
        if not page_expanded_data:
            continue
        
        kb_entry = {
            "id": page_id,
            "title": title,
            "full_data": page_expanded_data
        }
        knowledge_base.append(kb_entry)
        print(f"Fetched expanded data for page '{title}' (ID: {page_id})")
    
    for kb in knowledge_base:
        print(json.dumps(kb, sort_keys=True, indent=4, separators=(",", ": ")))

if __name__ == "__main__":
    main()
