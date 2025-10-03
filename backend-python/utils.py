import logging
from datetime import datetime
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

with open("app.log", "w") as log_file:
    log_file.truncate()

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def log_info(message):
    logging.info(message)
    print(f"[INFO] {message}")

def log_error(message):
    logging.error(message)
    print(f"[ERROR] {message}")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return conn
    except mysql.connector.Error as err:
        log_error(f"MySQL Connection Error: {err}")
        return None

def current_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    log_info("Test: Logging an info message from utils.py")
    log_error("Test: Logging an error message from utils.py")

    conn = get_db_connection()
    if conn:
        print("✅ MySQL connection successful.")
        conn.close()
    else:
        print("❌ MySQL connection failed.")

    print("Current Timestamp:", current_timestamp())