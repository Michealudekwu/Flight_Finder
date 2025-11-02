import requests
from data_manager import DataManager
import json

class FlightData:
    def __init__(self, token, name, stops):
        self.token = token
        self.name = name
        self.stops = stops
        self.nonstop_found = True 
        if self.stops == "yes":
            self.stops = "true"
        elif self.stops == "no":
            self.stops = "false"

        self.find_cheapest_flight()

    def find_cheapest_flight(self):
        data = DataManager(self.name)
        from_iata = data.from_iata
        to_iata = data.to_iata
        start_str = data.going_date
        end_str = data.arrival_date

        FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            # print(f"Getting flights with {self.stops}")
            response = self.response(to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT, headers, self.stops)
            self.step_over(response)

        except ValueError as error:
            if self.stops == "true":
                self.nonstop_found = False
            print(f"Getting flights from {from_iata.upper()}...TO...{to_iata.upper()}\nNO DIRECT FLIGHTS FOUND: {error}")
            try:
                if self.stops == "false":
                    response = self.response(to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT, headers, "true")
                else:
                    response = self.response(to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT, headers, "false")
                self.step_over(response)
            except ValueError as error:
                print(f"Still no flights found from {from_iata.upper()}...TO...{to_iata.upper()}. Reason: {error}")

    def response(self, to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT,headers,stops):
        parameters = {
            "originLocationCode": from_iata,
            "destinationLocationCode": to_iata,
            "departureDate": start_str,
            "returnDate": end_str,
            "adults": 1,
            "nonStop": stops,
            "currencyCode": "USD"
        }

        for params, value in parameters.items():
            print(f"{params} : {value}")

        response = requests.get(url=FLIGHT_ENDPOINT, params=parameters, headers=headers)

        if response.status_code != 200:
            print("API ERROR RESPONSE:", response.text)
            raise ValueError(f"API error: {response.status_code} - {response.text}")

        data = response.json().get("data", [])

        if not data:
            raise ValueError("No flight data returned.")

        return data

    def step_over(self, req):
        flight_info = []

        for ind,flight in enumerate(req):
            data = {
                "id" : ind,
                "price" : "",
                "segments" : "",
                "airport_codes": [] 
            }
            data["price"] = flight["price"]["total"]

            segments = flight["itineraries"][0]["segments"]
            for segs in segments:
                ports = {
                    "departure_airport_code" : "",
                    "inbound_date" : "",
                    "inbound_time" : "",
                    "arrival_airport_code" : "",
                    "outbound_date" : "",
                    "outbound_time" : "",
                    "planes" : ""
                }
                ports["planes"] = f"{segs['carrierCode']+segs['number']}"
                ports["departure_airport_code"] = segs["departure"]["iataCode"]
                ports["outbound_date"] = segs["departure"]["at"].split("T")[0]
                ports["outbound_time"] = segs["departure"]["at"].split("T")[1]

                ports["arrival_airport_code"] = segs["arrival"]["iataCode"]
                ports["inbound_date"] = segs["arrival"]["at"].split("T")[0]
                ports["inbound_time"] = segs["arrival"]["at"].split("T")[1]

                data["airport_codes"].append(ports)
            
            flight_info.append(data)


        with open("flight_data.json", "w") as file:
            json.dump(flight_info, file, indent=4)
