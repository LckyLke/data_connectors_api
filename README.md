# Confluence API

A Python project that provides a interface for interacting with the Confluence REST API (v2). 
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

   You can set these in your shell or in an optional `.env` file:
   ```bash
   CONFLUENCE_API_TOKEN=<your-token>
   CONFLUENCE_EMAIL=<your-email>
   CONFLUENCE_DOMAIN=<your-domain>.atlassian.net
   ```
   If you use a `.env` file, the project uses `python-dotenv` to automatically load them.


---

## Usage

In the project’s root directory:

```bash
python confluence_api/main.py
```

