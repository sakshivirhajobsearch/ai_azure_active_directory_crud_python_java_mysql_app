import requests
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, GRAPH_API_URL
from utils import log_info, log_error

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        access_token = r.json()['access_token']
        log_info("Azure AD access token retrieved.")
        return access_token
    except Exception as e:
        log_error(f"Error getting Azure AD token: {str(e)}")
        return None

def get_users():
    token = get_access_token()
    if not token:
        return []
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{GRAPH_API_URL}/users", headers=headers)
        response.raise_for_status()
        log_info("Successfully fetched Azure AD users.")
        return response.json()['value']
    except Exception as e:
        log_error(f"Error fetching Azure AD users: {str(e)}")
        return []

if __name__ == "__main__":
    users = get_users()
    print(f"Fetched {len(users)} users from Azure AD")