import os
from dotenv import load_dotenv

load_dotenv()  

# Confluence configurations
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL", "lukefriedrichs@gmail.com")
CONFLUENCE_DOMAIN = os.getenv("CONFLUENCE_DOMAIN", "lukefriedrichs.atlassian.net")

# Slack configuration
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")
SLACK_REFRESH_TOKEN = os.getenv("SLACK_REFRESH_TOKEN")


# Notion
NOTION_SECRET = os.getenv("NOTION_SECRET")


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")