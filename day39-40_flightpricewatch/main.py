#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from dateutil import parser
from datetime import datetime

spreadsheet = DataManager()
spreadsheet_data = spreadsheet.data

need_iata_code = False
for row in spreadsheet_data:
    if row[1] == "":
        need_iata_code = True

if need_iata_code:
    iata_lookup = FlightSearch()
    for i in range(1, len(spreadsheet_data)):
        spreadsheet_data[i][1] = iata_lookup.get_iata_code(spreadsheet_data[i][0])
    spreadsheet.update_spreadsheet(spreadsheet_data)

price_finder = FlightData()
bargain_flights = []
for i in range(1, len(spreadsheet_data)):
    flight_data = price_finder.get_cheapest_flight(spreadsheet_data[i][1])
    price = flight_data["price"]
    if price < int(spreadsheet_data[i][2]):
        spreadsheet_data[i][2] = price
        bargain_flights.append(flight_data)
if len(bargain_flights) > 0:
    spreadsheet.update_spreadsheet(spreadsheet_data)

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
    notifier = NotificationManager()
    notifier.send_email(email_subject, email_body)

