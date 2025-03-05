
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Google Apps Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyuxS5DDVhFVAS36rVWLp-RsMuqr9_V0R_f7XVD_mSoUbu4qg0xUkSG9B6pJRRAAhM57g/exec"

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
    app.run(host='0.0.0.0', port=10000)
