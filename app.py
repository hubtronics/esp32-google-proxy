from flask import Flask, request, jsonify
import requests
import os
from werkzeug.middleware.proxy_fix import ProxyFix  # Add this!

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)  # Add this line!

# Your Google Apps Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyuxS5DDVhFVAS36rVWLp-RsMuqr9_V0R_f7XVD_mSoUbu4qg0xUkSG9B6pJRRAAhM57g/exec"

@app.route('/')
def home():
    return "ESP32 Proxy Server is running!", 200

@app.route('/receive-data', methods=['GET'])
def receive_data():
    data = request.args.get('data')

    if not data:
        return jsonify({"error": "No data received"}), 400

    try:
        response = requests.get(GOOGLE_SCRIPT_URL, params={"data": data}, timeout=10)
        return response.text, response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to contact Google Sheets: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
