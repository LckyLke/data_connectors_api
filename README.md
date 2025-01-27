# Confluence API

A Python project that provides an interface for interacting with the Confluence REST API (v2). 
---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/lckylke/confluence_api.git
   cd confluence_api
   ```

2. **Create a Conda Environment**:

   ```bash
   conda create --name venv python=3.10.13
   conda activate venv
   ```

3. **Install Dependencies**:

   ```bash
   pip install -e .
   ```

---

## Configuration

1. **Set Environment Variables**:

   You can set these in an `.env` file:
   ```bash
   CONFLUENCE_API_TOKEN=<your-token>
   CONFLUENCE_EMAIL=<your-email>
   CONFLUENCE_DOMAIN=<your-domain>.atlassian.net
   ```

---

## Usage

### Basic Examples

```bash
# Get all pages
fetchconf --endpoint /pages

# Fetch blog posts
fetchconf --endpoint /blogposts

# Get attachments for page ID 123
fetchconf --endpoint '/pages/{id}/attachments' --id 123

# List spaces with query parameters
fetchconf --endpoint /spaces --param limit=50 --param status=current
```