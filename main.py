import json

from confluence_api.api_client import ConfluenceAPIClient
from confluence_api.pages import get_all_pages, get_page_data
from confluence_api.spaces import get_all_spaces

def main():
    # 1. Initialize the Confluence client
    client = ConfluenceAPIClient()

    # 2. Fetch all pages
    print("Fetching pages...")
    pages = get_all_pages(client, limit=100)
    print(f"Total pages found: {len(pages)}")

    # 3. For each page, fetch expanded page data
    knowledge_base = []
    for page in pages:
        page_id = page.get("id")
        title = page.get("title")

        page_expanded_data = get_page_data(client, page_id)
        if page_expanded_data:
            kb_entry = {
                "id": page_id,
                "title": title,
                "full_data": page_expanded_data
            }
            knowledge_base.append(kb_entry)
            print(f"Fetched expanded data for page '{title}' (ID: {page_id})")

    # 4. Print or store the knowledge base
    for kb_item in knowledge_base:
        print(json.dumps(kb_item, indent=2, sort_keys=True))

    # 5. Example: fetching spaces
    print("Fetching spaces...")
    spaces = get_all_spaces(client, limit=50)
    print(f"Total spaces found: {len(spaces)}")

    for space in spaces:
        print(f"Space name: {space.get('name')}, Key: {space.get('key')}")

if __name__ == "__main__":
    main()
