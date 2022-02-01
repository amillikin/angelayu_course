import requests

QUIZ_API = "https://opentdb.com/api.php"
NUMBER_OF_QUESTIONS = "10"
QUESTION_TYPE = "boolean"

parameters = {
    "amount": NUMBER_OF_QUESTIONS,
    "type": QUESTION_TYPE,
}

response = requests.get(QUIZ_API, params=parameters)
response.raise_for_status()
data = response.json()
question_data = data["results"]
