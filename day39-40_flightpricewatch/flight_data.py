import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta


class FlightData:
    

    def __init__(self):
        '''
            This class is responsible for talking to the Flight Search API.
        '''
        load_dotenv(os.environ.get("PYENV"))
        self.TEQUILA_KEY = os.getenv("TEQUILA_KEY")

    
    def get_cheapest_flight(self, code):
        api_endpoint = "https://tequila-api.kiwi.com/v2/search"
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        latest_date = (datetime.now() + timedelta(days=6*30)).strftime("%d/%m/%Y")

        headers = {
            "apikey": self.TEQUILA_KEY
        }

        params = {
            "fly_from": "city:LON",
            "fly_to": code,
            "date_from": tomorrow,
            "date_to": latest_date,
            "nights_in_dst_from": "7",
            "nights_in_dst_to": "30",
            "flight_type": "round",
            "locale": "en-US",
            "location_types": "airport",
            "curr": "GBP",
            "locale": "en"
        }

        response = requests.get(
            url=api_endpoint,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()["data"][0]
