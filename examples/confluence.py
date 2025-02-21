from data_connectors_api.api_client import ConfluenceAPIClient
# Create a .env file in your project root:
#
# CONFLUENCE_API_TOKEN=your_confluence_api_token
# CONFLUENCE_EMAIL=your_email@example.com
# CONFLUENCE_DOMAIN=your_confluence_domain.atlassian.net

if __name__ == "__main__":
    confluence_client = ConfluenceAPIClient()

    json_file, csv_file = confluence_client.save_all_pages()

    print(f"Saved JSON file: {json_file}")
    print(f"Saved CSV file: {csv_file}")
