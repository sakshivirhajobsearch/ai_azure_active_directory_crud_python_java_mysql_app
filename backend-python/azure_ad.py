import requests
from config import AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET

def get_token():
    url = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AZURE_CLIENT_ID,
        "client_secret": AZURE_CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

def get_users():
    token = get_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get("https://graph.microsoft.com/v1.0/users", headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch users: {response.status_code}, {response.text}")
        return []

    data = response.json()
    return data.get("value", [])
