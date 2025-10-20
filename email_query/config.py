import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
load_dotenv()

# --- Microsoft Graph API Credentials ---
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_PRINCIPAL_NAME = os.getenv("USER_PRINCIPAL_NAME") # The mailbox to query

# --- OpenAI API Key ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- ChromaDB Configuration ---
CHROMA_DIR = "email_db"

# --- Validation ---
# Ensure that all necessary configuration variables are present
if not all([CLIENT_ID, TENANT_ID, CLIENT_SECRET, USER_PRINCIPAL_NAME, OPENAI_API_KEY]):
    raise ValueError(
        "One or more required environment variables are missing. "
        "Please check your .env file."
    )