from confluence_api.api_client import ConfluenceAPIClient, SlackAPIClient, NotionAPIClient
from datetime import datetime

def run_data_pipeline():
    clients = {
        "confluence": ConfluenceAPIClient(),
        "slack": SlackAPIClient(),
        "notion": NotionAPIClient()
    }

    data_sources = {
        "confluence_pages": clients['confluence'].get_all_pages(),
        "slack_channels": clients['slack'].list_channels(),
        "notion_databases": clients['notion'].get_databases()
    }

    analytics = {
        "content_stats": {
            "total_pages": len(data_sources['confluence_pages']),
            "avg_page_length": sum(
                len(p.get('body', {}).get('storage', {}).get('value', '')) 
                for p in data_sources['confluence_pages']
            ) / len(data_sources['confluence_pages'])
        },
        "collaboration_metrics": {
            "active_channels": len([c for c in data_sources['slack_channels']
                                  if c['num_members'] > 10]),
            "shared_databases": len(data_sources['notion_databases'])
        }
    }

    clients['notion'].save_to_json(
        analytics, 
        f"analytics_{datetime.now().date().isoformat()}.json"
    )
    clients['slack'].save_to_csv(
        data_sources['slack_channels'],
        "daily_channels.csv",
        ['id', 'name', 'num_members', 'created']
    )

    print("pipeline completed successfully")
    

if __name__ == "__main__":
	run_data_pipeline()