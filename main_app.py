import json
from city_iata import FlightSearch
from flight_data import FlightData

class Main:
    def __init__(self):
        pass
    
    def iata_find(self, cities):
        self.iata = FlightSearch(cities)
        city_codes = self.iata.get_names()
        return city_codes

    def flight_find(self,user,stops,cities):
        self.iata = FlightSearch(cities)
        token = self.iata._get_new_token()
        flight_data = FlightData(token,user,stops)
        return flight_data

    def get_flight_data(self):
        with open("flight_data.json") as data:
            content = json.load(data)
        return content
    
    def pricing(self, contents, user_price):
        flight_info = []
        for data in contents:
            if float(data["price"]) <= user_price:
                flight = {
                    "price" : "",
                    "data" : [value for value in data["airport_codes"] ]
                }
                flight["price"] = data["price"]
                flight_info.append(flight)

        return flight_info
