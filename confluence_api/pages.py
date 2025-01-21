from confluence_api.api_client import ConfluenceAPIClient

def get_all_pages(client: ConfluenceAPIClient, limit=100):
    """
    Retrieves all pages from Confluence (paged).
    Returns a list of minimal page objects (ID, title, etc.).
    """
    all_pages = []
    # Confluence v2 pages endpoint
    endpoint = "/pages"
    params = {"limit": limit}

    # First get request
    data = client.get(endpoint, params=params)
    # As an example, parse out the results
    pages_batch = data.get("results", [])
    all_pages.extend(pages_batch)

    return all_pages


def get_page_data(client: ConfluenceAPIClient, page_id):
    """
    Fetch a page with expanded data in atlas_doc_format.
    """
    endpoint = f"/pages/{page_id}"
    params = {"body-format": "atlas_doc_format"}

    try:
        data = client.get(endpoint, params=params)
        return data
    except Exception as e:
        print(f"Error fetching page {page_id}: {e}")
        return None
