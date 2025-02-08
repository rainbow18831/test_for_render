import os
import json
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set up the credentials and authorize
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not credentials_json:
    part1 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_1")
    part2 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_2")
    credentials_json = part1 + part2

print("Credentials JSON:", credentials_json)

if credentials_json:
    credentials_dict = json.loads(credentials_json)  # Convert JSON string to dictionary
    CREDS = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
    client = gspread.authorize(CREDS)
else:
    raise ValueError("No credentials found! Set the GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")

@app.route('/')
def index():
    # Open the spreadsheet
    spreadsheet = client.open("my first sheet")
    worksheet = spreadsheet.sheet1

    # Get all records
    data = worksheet.get_all_records()

    return render_template('index.html', data=data)  # Pass data to the template

if __name__ == '__main__':
    app.run(debug=True)