import json
import csv
from datetime import datetime
from confluence_api.api_client import ConfluenceAPIClient

def save_confluence_data_example():
    # Initialize client with default body format
    client = ConfluenceAPIClient(
        default_query_params={
            'body-format': 'storage',  # Get content in storage format
            'expand': 'body.storage'   # Include body content in response
        }
    )

    try:
        # Fetch all pages with default parameters
        print("Fetching Confluence pages...")
        all_pages = client.get_all_pages({
            'limit': 100,  
            'status': 'current'
        })

        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"confluence_pages_{timestamp}.json"
        csv_filename = f"confluence_pages_{timestamp}.csv"

        # Save as JSON (full fidelity)
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(all_pages, json_file, indent=2, ensure_ascii=False)
        print(f"Saved {len(all_pages)} pages to {json_filename}")

        # Save as CSV (simplified structure)
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[
                'id', 
                'title',
                'spaceId',
                'creatorId',
                'createdAt',
                'version',
                'contentLength'
            ])
            
            writer.writeheader()
            for page in all_pages:
                writer.writerow({
                    'id': page.get('id'),
                    'title': page.get('title'),
                    'spaceId': page.get('spaceId'),
                    'creatorId': page.get('creatorId'),
                    'createdAt': page.get('createdAt'),
                    'version': page.get('version', {}).get('number'),
                    'contentLength': len(page.get('body', {}).get('storage', {}).get('value', ''))
                })
        print(f"Saved simplified version to {csv_filename}")

    except Exception as e:
        print(f"Error fetching/saving data: {str(e)}")

if __name__ == "__main__":
    save_confluence_data_example()