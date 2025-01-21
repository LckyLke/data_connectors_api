from confluence_api.api_client import ConfluenceAPIClient

def get_all_spaces(client: ConfluenceAPIClient, limit=50):
    """
    Fetch a list of all spaces from Confluence.
    """
    endpoint = "/spaces"
    params = {"limit": limit}

    try:
        data = client.get(endpoint, params=params)
        return data.get("results", [])
    except Exception as e:
        print(f"Error fetching spaces: {e}")
        return []
