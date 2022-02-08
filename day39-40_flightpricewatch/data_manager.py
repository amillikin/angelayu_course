import requests
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class DataManager:
   
    def __init__(self):
        '''
            Holds the set of data from flight spreadsheet.
        '''
        load_dotenv(os.environ.get("PYENV"))
        self.EXCEL_CREDS = Credentials.from_service_account_file(
            str(os.environ.get("EXCEL_SA_JSON")),
        )
        self.EXCEL_SHEET_ID = os.getenv("EXCEL_SHEET_ID_39")
        self.EXCEL_FLIGHT_SHEET_RANGE = "prices!A:C"
        self.EXCEL_USER_SHEET_RANGE = "users!A:C"
        self.EXCEL_MAJOR_DIMENSION = "ROWS"
        self.flight_data = []
        self.user_data = []
        self.read_spreadsheet()


    def read_spreadsheet(self):
        try:
            service = build('sheets', 'v4', credentials=self.EXCEL_CREDS)

            sheet = service.spreadsheets()
            
            result = sheet.values().get(
                spreadsheetId=self.EXCEL_SHEET_ID,
                range=self.EXCEL_FLIGHT_SHEET_RANGE,
                majorDimension=self.EXCEL_MAJOR_DIMENSION,
            ).execute()
            self.flight_data = result.get('values', [])
            
            result = sheet.values().get(
                spreadsheetId=self.EXCEL_SHEET_ID,
                range=self.EXCEL_USER_SHEET_RANGE,
                majorDimension=self.EXCEL_MAJOR_DIMENSION,
            ).execute()
            self.user_data = result.get('values', [])
        except HttpError as err:
            print(err)


    def update_spreadsheet(self, update_data, data_type):
        '''
            Leverages excel get and update API for a sheet shared with a
            google cloud service account.
        '''
        if data_type == "flight":
            self.flight_data = update_data
            update_range = self.EXCEL_FLIGHT_SHEET_RANGE
        elif data_type == "user":
            self.user_data = update_data
            update_range = self.EXCEL_USER_SHEET_RANGE
        else:
            print(f"Invalid date_type")

        try:
            service = build('sheets', 'v4', credentials=self.EXCEL_CREDS)

            body = {
                "majorDimension": self.EXCEL_MAJOR_DIMENSION,
                "values": update_data
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.EXCEL_SHEET_ID,
                valueInputOption="RAW",
                range=update_range,
                body=body
            ).execute()
        except HttpError as err:
            print(err)
