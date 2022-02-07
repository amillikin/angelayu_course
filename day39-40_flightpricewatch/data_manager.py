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
        self.EXCEL_SHEET_RANGE = "prices!A:C"
        self.EXCEL_MAJOR_DIMENSION = "ROWS"
        self.EXCEL_COLUMNS = ["City", "IATA Code", "Lowest Price"]
        self.data = []
        self.read_spreadsheet()


    def read_spreadsheet(self):
        try:
            service = build('sheets', 'v4', credentials=self.EXCEL_CREDS)

            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.EXCEL_SHEET_ID,
                range=self.EXCEL_SHEET_RANGE,
                majorDimension=self.EXCEL_MAJOR_DIMENSION,
            ).execute()
            self.data = result.get('values', [])
        except HttpError as err:
            print(err)


    def update_spreadsheet(self, update_data):
        '''
            Leverages excel get and update API for a sheet shared with a
            google cloud service account.
        '''
        self.data = update_data
        try:
            service = build('sheets', 'v4', credentials=self.EXCEL_CREDS)

            body = {
                "majorDimension": self.EXCEL_MAJOR_DIMENSION,
                "values": self.data
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.EXCEL_SHEET_ID,
                valueInputOption="RAW",
                range=self.EXCEL_SHEET_RANGE,
                body=body
            ).execute()
        except HttpError as err:
            print(err)


    def to_dict(self):
        data_dict = {key: None for key in self.EXCEL_COLUMNS}
        
