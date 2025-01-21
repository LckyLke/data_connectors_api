import os
from dotenv import load_dotenv

load_dotenv()  

CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL", "lukefriedrichs@gmail.com")
CONFLUENCE_DOMAIN = os.getenv("CONFLUENCE_DOMAIN", "lukefriedrichs.atlassian.net")

