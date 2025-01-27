import argparse
import json
from confluence_api.api_client import ConfluenceAPIClient

def main():
    """Command-line interface for Confluence API with flexible endpoint support."""
    parser = argparse.ArgumentParser(
        description="Fetch paginated data from Confluence Cloud API v2",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--endpoint',
        required=True,
        help='API endpoint path (e.g., /pages, /pages/{id}/attachments)'
    )
    parser.add_argument(
        '--id',
        help='ID to replace {id} placeholder in the endpoint'
    )
    parser.add_argument(
        '--param',
        action='append',
        help='Query parameters as key=value pairs (e.g., --param spaceKey=ABC)'
    )
    parser.add_argument(
        '--output',
        help='File path to save JSON output (prints to console if omitted)'
    )
    
    args = parser.parse_args()
    client = ConfluenceAPIClient()

    try:
        final_endpoint = args.endpoint
        if '{id}' in final_endpoint:
            if not args.id:
                raise ValueError("Endpoint contains {id} but --id was not provided")
            final_endpoint = final_endpoint.format(id=args.id)
        
        params = {}
        if args.param:
            for param in args.param:
                key, value = param.split('=', 1)
                params[key] = value
        
        data = client.get_paginated(final_endpoint, params=params)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(data)} items to {args.output}")
        else:
            print(json.dumps(data, indent=2))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()