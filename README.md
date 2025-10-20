# Email Query App

A Streamlit application that fetches Outlook emails and allows you to ask questions about their content using LangChain and OpenAI.

## Features

- 📧 Fetches Outlook emails using Microsoft Graph API
- 🤖 Processes emails with LangChain and stores in ChromaDB vector database
- ❓ Interactive Q&A interface for querying email content
- 🔒 Secure credential management with .env file

## Setup

### 1. Prerequisites

- Python 3.8+
- Azure account with app registration permissions
- OpenAI API key

### 2. Azure Configuration

1. Register a new application in Microsoft Entra ID
2. Create a client secret and copy its value
3. Add Microsoft Graph API permission: `Mail.Read`
4. Grant admin consent for the permissions

### 3. Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 4. Usage

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Configuration

Create a `.env` file with:

```env
CLIENT_ID=your_azure_client_id
TENANT_ID=your_azure_tenant_id
CLIENT_SECRET=your_azure_client_secret
USER_PRINCIPAL_NAME=user@domain.com
OPENAI_API_KEY=sk-your_openai_key
```
