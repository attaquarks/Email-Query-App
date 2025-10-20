Email Query App with LangChain and Streamlit

This application fetches Outlook emails for a specific user on a given day, processes them using LangChain, stores them in a Chroma vector database, and allows you to ask natural language questions about the email content.

Features

Fetches emails securely using Microsoft Graph API with Application permissions.

Uses LangChain to process and structure email content.

Embeds email data into a ChromaDB vector store for efficient semantic search.

Provides a simple and interactive Streamlit web interface for querying.

Keeps API keys and sensitive configurations secure using a .env file.

Setup and Installation

1. Prerequisites

Python 3.8+

An Azure account with permissions to register applications in Microsoft Entra ID.

An OpenAI API key.

2. Azure App Registration

Register a new application in the Microsoft Entra ID portal.

Go to Certificates & secrets and create a new Client Secret. Copy the secret's Value immediately, as it will be hidden later.

Go to API permissions, click + Add a permission > Microsoft Graph > Application permissions.

Select Mail.Read and add the permission.

Click the Grant admin consent for [Your Tenant] button.

3. Project Configuration

Clone this repository or create the folder structure and files as described.

Create a file named .env in the email_query_app root directory.

Populate the .env file with your credentials:

CLIENT_ID="your_client_id_here"
TENANT_ID="your_tenant_id_here"
CLIENT_SECRET="your_client_secret_value_here"
USER_PRINCIPAL_NAME="user.email@yourdomain.com"
OPENAI_API_KEY="sk-your_openai_api_key_here"


4. Running the Application

Create a virtual environment:

python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`


Install dependencies:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run app.py


Open your web browser and navigate to http://localhost:8501.
