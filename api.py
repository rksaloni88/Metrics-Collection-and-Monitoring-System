from flask import Flask, request, jsonify
import sqlite3
from flask_httpauth import HTTPBasicAuth
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
auth = HTTPBasicAuth()

DATABASE_NAME = os.getenv('DATABASE_NAME', 'metrics.db')
USERNAME = os.getenv('API_USERNAME', 'admin')
PASSWORD = os.getenv('API_PASSWORD', 'password')

logging.basicConfig(level=logging.INFO)

@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and password == PASSWORD:
        return username

def query_db(query, args=(), one=False):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return None

@app.route('/metrics', methods=['GET'])
@auth.login_required
def get_metrics():
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    if not start_time or not end_time:
        return jsonify({"error": "Please provide 'start' and 'end' query parameters"}), 400

    query = "SELECT * FROM metrics WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp"
    result = query_db(query, [start_time, end_time])

    if result is None:
        return jsonify({"error": "Database error"}), 500

    return jsonify(result)

@app.route('/metrics/average', methods=['GET'])
@auth.login_required
def get_average_metrics():
    metric_type = request.args.get('type', 'cpu')  # Default to 'cpu' if not specified

    if metric_type not in ['cpu', 'memory', 'disk_io', 'network_io']:
        return jsonify({"error": "Invalid metric type"}), 400

    query = f"SELECT AVG({metric_type}) FROM metrics WHERE timestamp >= datetime('now', '-1 hour')"
    result = query_db(query, one=True)

    return jsonify({f"average_{metric_type}_last_hour": result[0] if result[0] is not None else 0})

@app.route('/metrics/min', methods=['GET'])
@auth.login_required
def get_min_metrics():
    metric_type = request.args.get('type', 'cpu')  # Default to 'cpu' if not specified

    if metric_type not in ['cpu', 'memory', 'disk_io', 'network_io']:
        return jsonify({"error": "Invalid metric type"}), 400

    query = f"SELECT MIN({metric_type}) FROM metrics WHERE timestamp >= datetime('now', '-1 day')"
    result = query_db(query, one=True)

    return jsonify({f"min_{metric_type}_last_day": result[0] if result[0] is not None else 0})

@app.route('/metrics/max', methods=['GET'])
@auth.login_required
def get_max_metrics():
    metric_type = request.args.get('type', 'cpu')  # Default to 'cpu' if not specified

    if metric_type not in ['cpu', 'memory', 'disk_io', 'network_io']:
        return jsonify({"error": "Invalid metric type"}), 400

    query = f"SELECT MAX({metric_type}) FROM metrics WHERE timestamp >= datetime('now', '-1 day')"
    result = query_db(query, one=True)

    return jsonify({f"max_{metric_type}_last_day": result[0] if result[0] is not None else 0})

if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'true').lower() in ['true', '1', 't']
    app.run(debug=DEBUG)