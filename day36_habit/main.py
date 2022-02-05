import requests
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(os.environ.get("PYENV"))
PIXELA_USERNAME = "loofy"
PIXELA_KEY = os.getenv("PIXELA_KEY")
PIEXLA_ENDPOINT = "https://pixe.la/v1/users/"
CYCLING_GRAPH_ID = "graph1"
TODAY = date.strftime(date.today(), "%Y%m%d")

graph_endpoint = f"{PIEXLA_ENDPOINT}{PIXELA_USERNAME}/graphs/{CYCLING_GRAPH_ID}"

headers = {
    "X-USER-TOKEN": PIXELA_KEY
}
parameters = {
    "date": TODAY,
    "quantity": "0.1",
}

response = requests.post(
    url=graph_endpoint,
    json=parameters,
    headers=headers,
)
print(response.text)
