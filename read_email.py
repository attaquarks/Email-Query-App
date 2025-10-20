import msal
import requests

CLIENT_ID = "0cda293f-ed86-46d9-8cb5-9149b62570d3"
TENANT_ID = "75df096c-8b72-48e4-9b91-cbf79d87ee3a"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read"]

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
else:
    result = None

if not result:
    print("🔑 Opening browser for Microsoft login...")
    result = app.acquire_token_interactive(scopes=SCOPES)

if "access_token" in result:
    print("✅ Access token acquired successfully.\n")

    headers = {"Authorization": f"Bearer {result['access_token']}"}
    endpoint = "https://graph.microsoft.com/v1.0/me/messages"

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json().get("value", [])
        print(f"📬 Fetched {len(data)} emails!\n")
        for i, mail in enumerate(data[:5], start=1):
            print(f"{i}. {mail['subject']} (from {mail['from']['emailAddress']['address']})")
            print(f"   Received: {mail['receivedDateTime']}")
            print("-" * 60)
    else:
        print("❌ Error fetching emails:", response.status_code, response.text)
else:
    print("❌ Failed to acquire token:", result.get("error_description"))
