import msal
import requests
from email_query.config import CLIENT_ID, TENANT_ID

# The authority endpoint remains the same
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Use the simple Delegated scope
SCOPES = ["Mail.Read"]

def fetch_emails_for_day(date_str):
    """
    Fetches all Outlook emails for a specific day using Microsoft Graph API
    with Delegated (User) permissions via an interactive flow.
    """
    # 1. Switch to Public Client Application
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY
    )

    # 2. Acquire token interactively
    accounts = app.get_accounts()
    if accounts:
        # Try silent acquisition first
        token_result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        token_result = None

    if not token_result:
        print("Opening browser for Microsoft login...")
        # Use interactive flow to get the user's consent/token
        token_result = app.acquire_token_interactive(scopes=SCOPES)
    
    if "access_token" not in token_result:
        error_desc = token_result.get('error_description', 'Unknown error')
        error_code = token_result.get('error', 'unknown_error')
        raise Exception(f"Failed to acquire token - Error: {error_code}, Description: {error_desc}")

    access_token = token_result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 3. Use 'me' endpoint since the token is for the logged-in user
    # Note: You no longer need to reference USER_PRINCIPAL_NAME
    base_url = "https://graph.microsoft.com/v1.0/me"

    # OData query to filter emails received within the selected date range
    odata_filter = f"receivedDateTime ge {date_str}T00:00:00Z and receivedDateTime le {date_str}T23:59:59Z"
    
    params = {
        "$filter": odata_filter,
        "$select": "subject,body,from,receivedDateTime"
    }
    
    # ... (rest of the fetching logic remains the same)
    response = requests.get(f"{base_url}/messages", headers=headers, params=params)

    if response.status_code != 200:
        error_msg = f"Error fetching emails: {response.status_code} - {response.text}"
        # ...
        raise Exception(error_msg)

    emails = response.json().get("value", [])
    
    # ... (rest of the content extraction remains the same)
    email_docs = []
    for msg in emails:
        content = (
            f"Subject: {msg.get('subject', 'N/A')}\n"
            f"From: {msg.get('from', {}).get('emailAddress', {}).get('address', 'N/A')}\n"
            f"Received: {msg.get('receivedDateTime', 'N/A')}\n\n"
            f"Body:\n{msg.get('body', {}).get('content', 'N/A')}"
        )
        email_docs.append(content)

    return email_docs