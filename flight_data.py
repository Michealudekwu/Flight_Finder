import requests
import json
import os
from data_manager import DataManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "flight_data.json")


class FlightData:
    def __init__(self, token, name, stops):
        self.token = token
        self.name = name
        self.stops = "true" if stops == "yes" else "false"
        self.nonstop_found = True
        self.flight_info = []

        self.find_cheapest_flight()

    def find_cheapest_flight(self):
        data = DataManager(self.name)
        from_iata = data.from_iata
        to_iata = data.to_iata
        start_str = data.going_date
        end_str = data.arrival_date

        FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = self.call_api(to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT, headers, self.stops)
            self.process_response(response)
        except ValueError as error:
            if self.stops == "true":
                self.nonstop_found = False
            print(f"No direct flights found: {error}")
            # fallback search
            try:
                alt_stops = "false" if self.stops == "true" else "true"
                response = self.call_api(to_iata, from_iata, start_str, end_str, FLIGHT_ENDPOINT, headers, alt_stops)
                self.process_response(response)
            except ValueError as error:
                print(f"Still no flights found: {error}")

        # Save results to JSON safely
        self.save_to_json()

    def call_api(self, to_iata, from_iata, start_str, end_str, endpoint, headers, stops):
        params = {
            "originLocationCode": from_iata,
            "destinationLocationCode": to_iata,
            "departureDate": start_str,
            "returnDate": end_str,
            "adults": 1,
            "nonStop": stops,
            "currencyCode": "USD"
        }

        response = requests.get(url=endpoint, params=params, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"API error {response.status_code}: {response.text}")

        data = response.json().get("data", [])
        if not data:
            raise ValueError("No flight data returned from API.")

        return data

    def process_response(self, flights):
        for ind, flight in enumerate(flights):
            flight_data = {
                "id": ind,
                "price": flight.get("price", {}).get("total", "N/A"),
                "segments": [],
                "airport_codes": []
            }

            segments = flight.get("itineraries", [{}])[0].get("segments", [])
            for seg in segments:
                seg_info = {
                    "planes": f"{seg.get('carrierCode', '')}{seg.get('number', '')}",
                    "departure_airport_code": seg.get("departure", {}).get("iataCode", ""),
                    "outbound_date": seg.get("departure", {}).get("at", "").split("T")[0] if "at" in seg.get("departure", {}) else "",
                    "outbound_time": seg.get("departure", {}).get("at", "").split("T")[1] if "at" in seg.get("departure", {}) else "",
                    "arrival_airport_code": seg.get("arrival", {}).get("iataCode", ""),
                    "inbound_date": seg.get("arrival", {}).get("at", "").split("T")[0] if "at" in seg.get("arrival", {}) else "",
                    "inbound_time": seg.get("arrival", {}).get("at", "").split("T")[1] if "at" in seg.get("arrival", {}) else ""
                }
                flight_data["airport_codes"].append(seg_info)

            self.flight_info.append(flight_data)

    def save_to_json(self):
        try:
            with open(JSON_PATH, "w") as file:
                json.dump(self.flight_info, file, indent=4)
            print(f"Flight data saved to {JSON_PATH}")
        except Exception as e:
            print(f"Error saving flight data: {e}")
