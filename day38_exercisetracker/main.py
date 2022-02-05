import requests
import os
from datetime import datetime, date
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


load_dotenv(os.environ.get("PYENV"))

NUTRITIONIX_ID = os.getenv("NUTRITIONIX_ID")
NUTRITIONIX_KEY = os.getenv("NUTRITIONIX_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

EXCEL_CREDS = Credentials.from_service_account_file(
    str(os.environ.get("EXCEL_SA_JSON")),
)
EXCEL_SHEET_ID = os.getenv("EXCEL_SHEET_ID_38")
EXCEL_SHEET_RANGE = "workouts!A:E"
EXCEL_MAJOR_DIMENSION = "COLUMNS"


def get_nutritionix_resp(nat_lang_query: str):
    '''
        Takes a natural language string from user's input,
        passes the string to nutritionix,
        then returns a list of exercise activities
    '''
    nix_headers = {
        "x-app-id": NUTRITIONIX_ID,
        "x-app-key": NUTRITIONIX_KEY,
        "x-remote-user-id": "0",
    }

    nix_params = {
        "query": nat_lang_query,
        "gender": "male",
        "weight_kg": "75",
        "height_cm": "182",
        "age": "31",
    }

    response = requests.post(
        url=NUTRITIONIX_ENDPOINT,
        json=nix_params,
        headers=nix_headers,
    )
    response.raise_for_status()
    data = response.json()["exercises"]

    return data


def update_spreadsheet(spreadsheet_entries):
    '''
        Leverages excel get and update API for a sheet shared with a
        google cloud service account.
    '''
    try:
        service = build('sheets', 'v4', credentials=EXCEL_CREDS)

        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=EXCEL_SHEET_ID,
            range=EXCEL_SHEET_RANGE,
            majorDimension=EXCEL_MAJOR_DIMENSION,
        ).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        for entry_i in range(len(spreadsheet_entries)):
            for column_i in range(len(values)):
                values[column_i].append(spreadsheet_entries[entry_i][column_i])

        body = {
            "majorDimension": EXCEL_MAJOR_DIMENSION,
            "values": values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=EXCEL_SHEET_ID,
            valueInputOption="RAW",
            range=EXCEL_SHEET_RANGE,
            body=body
        ).execute()
    except HttpError as err:
        print(err)


def build_exercise_entries(data):
    '''
    Takes data from nutritionix and returns a list of 
    exercise activities submitted, where each activity contains
    all the data necessary for one row in excel
    '''
    entries = []
    for i in range(len(data)):
        date_today = date.strftime(date.today(), "%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        duration = data[i]["duration_min"]
        activity = data[i]["name"]
        cal = data[i]["nf_calories"]
        new_entry = [date_today,
                     time,
                     duration,
                     activity,
                     cal]
        entries.append(new_entry)
    
    return entries


user_input = input("What exercise have you completed?\n>")

nix_data = get_nutritionix_resp(user_input)

exercise_entries = build_exercise_entries(nix_data)

update_spreadsheet(exercise_entries)
