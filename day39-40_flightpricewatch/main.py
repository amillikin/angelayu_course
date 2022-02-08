from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from dateutil import parser
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def check_iata_codes(historical_data):
    need_iata_code = False
    for row in historical_data:
        if row[1] == "":
            need_iata_code = True

    if need_iata_code:
        iata_lookup = FlightSearch()
        for i in range(1, len(historical_data)):
            historical_data[i][1] = iata_lookup.get_iata_code(historical_data[i][0])
        spreadsheet.update_spreadsheet(update_data=historical_data, data_type="flight")


def check_flights(historical_data, email_list):
    price_finder = FlightData()
    bargain_flights = []
    for i in range(1, len(historical_data)):
        new_data = price_finder.get_cheapest_flight(historical_data[i][1])
        if new_data is not None:
            price = new_data["price"]
            if price < int(historical_data[i][2]):
                historical_data[i][2] = price
                bargain_flights.append(new_data)
    if len(bargain_flights) > 0:
        spreadsheet.update_spreadsheet(update_data=historical_data, data_type="flight")
        if len(email_list) > 1:
            email_subject = "Subject:New flight deals!\n\n"
            email_body = ""
            for flight in bargain_flights:
                formated_departure = parser.parse(flight['local_departure']).strftime("%Y-%m-%d")
                formated_arrival = parser.parse(flight['local_arrival']).strftime("%Y-%m-%d")
                email_body += (
                    f"Only {flight['price']} GBP to fly from {flight['cityFrom']}-" +
                    f"{flight['cityCodeFrom']} to {flight['cityTo']}-" +
                    f"{flight['cityCodeTo']}, from {formated_departure}" +
                    f" to {formated_arrival}\n\n"
                )
            recipients = [user[2] for user in email_list]
            notifier = NotificationManager()
            notifier.send_email(email_subject, email_body, recipients)


def get_user():
    first = ""
    last = ""
    email1 = ""
    email2 = ""
    while not re.match("[A-za-z]+", first):
        first = input("What is your first name?\n> ").title()
    while not re.match("[A-za-z]+", last):
        last = input("What is your last name?\n> ").title()
    while not re.match(EMAIL_REGEX, email1):
        email1 = input("What is your email?\n> ")
    while not re.match(EMAIL_REGEX, email2) or not (email1 == email2):
        email2 = input("Please verify your email?\n> ")
    
    return [first, last, email1]


user_response = ""
while not user_response in ("c", "u", "q"):
    user_response = input("Check flights (c), add user (u), or quit (q)?\n> ").lower()
if user_response == "c":
    spreadsheet = DataManager()
    flight_data = spreadsheet.flight_data
    user_data = spreadsheet.user_data
    check_iata_codes(flight_data)
    check_flights(flight_data, user_data)
elif user_response == "u":
    new_user = get_user()
    spreadsheet = DataManager()
    user_data = spreadsheet.user_data
    user_data.append(new_user)
    spreadsheet.update_spreadsheet(update_data=user_data, data_type="user")

else:
    print(f"Goodbye!")

