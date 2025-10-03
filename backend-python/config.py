MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"
MYSQL_DB = "ai_azure_active_directory"

TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

GRAPH_API_URL = "https://graph.microsoft.com/v1.0"

if __name__ == "__main__":
    print("MySQL DB:", MYSQL_DB)
    print("Azure Graph API:", GRAPH_API_URL)