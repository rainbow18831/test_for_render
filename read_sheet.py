import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the credentials and authorize
SCOPE = SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

part1 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_1")
part2 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_2")
credentials_json = part1 + part2

if credentials_json:
    credentials_dict = json.loads(credentials_json)  # Convert JSON string to dictionary
    CREDS = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
    client = gspread.authorize(CREDS)
else:
    raise ValueError("No credentials found! Set the GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")


# Open the spreadsheet
spreadsheet = client.open("my first sheet")
worksheet = spreadsheet.sheet1

# Get all records
data = worksheet.get_all_records()
print(data)
