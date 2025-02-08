import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set up the credentials and authorize
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

@app.before_first_request
def authorize_google_sheets():
    global client
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    if not credentials_json:
        part1 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_1")
        part2 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_2")
        credentials_json = part1 + part2

    if credentials_json:
        credentials_dict = json.loads(credentials_json)  # Convert JSON string to dictionary
        CREDS = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
        client = gspread.authorize(CREDS)
    else:
        raise ValueError("No credentials found! Set the GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")

# Home route
@app.route("/")
def home():
    return "¡Hola! Tu servidor Flask está funcionando."

# Route to get data from the spreadsheet
@app.route("/data", methods=["GET"])
def get_data():
    try:
        # Open the spreadsheet
        spreadsheet = client.open("my first sheet")
        worksheet = spreadsheet.sheet1

        # Get all records
        data = worksheet.get_all_records()
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)