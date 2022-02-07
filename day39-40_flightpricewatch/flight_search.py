import os
import requests
from dotenv import load_dotenv


class FlightSearch:
    

    def __init__(self):
        '''
            This class is responsible for talking to the Flight Search API.
        '''
        load_dotenv(os.environ.get("PYENV"))
        self.TEQUILA_KEY = os.getenv("TEQUILA_KEY")

    
    def get_iata_code(self, city):
        api_endpoint = "https://tequila-api.kiwi.com/locations/query"

        headers = {
            "apikey": self.TEQUILA_KEY
        }

        params = {
            "term": city,
            "locale": "en-US",
            "location_types": "airport",
        }

        response = requests.get(
            url=api_endpoint,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()["locations"][0]["code"]


