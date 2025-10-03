from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from azure_ad import get_users
from ai_module import predict_role_risk
from utils import log_info, log_error

app = Flask(__name__)
CORS(app)

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
        log_error(f"MySQL connection error: {err}")
        return None

@app.route('/')
def index():
    return jsonify({'message': 'AI + Azure AD Flask API Running'})

@app.route('/users', methods=['GET'])
def list_users():
    try:
        users = get_users()
        for u in users:
            u['risk'] = predict_role_risk(u)
        log_info("Fetched users and applied risk predictions.")
        return jsonify(users)
    except Exception as e:
        log_error(f"Error in /users: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@app.route('/users/save', methods=['POST'])
def save_users():
    try:
        users = get_users()
        if not users:
            log_error("No users returned from Azure AD.")
            return jsonify({'error': 'No users to save'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()
        for u in users:
            risk = predict_role_risk(u)
            cursor.execute("""
                INSERT INTO azure_users (id, displayName, mail, jobTitle, risk) 
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    displayName=%s, mail=%s, jobTitle=%s, risk=%s
            """, (
                u['id'], u['displayName'], u.get('mail', ''), u.get('jobTitle', ''), risk,
                u['displayName'], u.get('mail', ''), u.get('jobTitle', ''), risk
            ))

        conn.commit()
        cursor.close()
        conn.close()
        log_info("Users saved to MySQL successfully.")
        return jsonify({'message': 'Users saved to MySQL'})
    except Exception as e:
        log_error(f"Error in /users/save: {str(e)}")
        return jsonify({'error': 'Failed to save users'}), 500

# ✅ /test-post endpoint for POST testing
@app.route('/test-post', methods=['POST'])
def test_post():
    try:
        data = request.get_json()
        log_info(f"Received test POST data: {data}")
        return jsonify({
            "status": "Test POST successful",
            "received": data
        })
    except Exception as e:
        log_error(f"Error in /test-post: {str(e)}")
        return jsonify({'error': 'Test POST failed'}), 500

if __name__ == '__main__':
    log_info("Starting Flask server at http://127.0.0.1:5000/")
    app.run(debug=True)
