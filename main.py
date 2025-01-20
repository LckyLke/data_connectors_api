import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Replace with your details
api_token = os.getenv("CONFLUENCE_API_TOKEN")
email = "lukefriedrichs@gmail.com"

url = "https://lukefriedrichs.atlassian.net/wiki/api/v2/pages"

auth = HTTPBasicAuth(email, api_token)

headers = {
  "Accept": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

