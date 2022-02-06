import os
import requests
from dotenv import load_dotenv


class FlightSearch:
    

    def __init__(self, iata_list):
        '''
            This class is responsible for talking to the Flight Search API.
        '''
        load_dotenv(os.environ.get("PYENV"))
        self.TEQUILA_KEY = os.getenv("TEQUILA_KEY")
        self.iata_codes = iata_list
        if len(self.iata_codes) == 0:
            update_iata_codes()

    
    def update_iata_codes(self):
        headers = {
            "apikey": self.TEQUILA_KEY
        }

        params = {
            "term": 
        }
