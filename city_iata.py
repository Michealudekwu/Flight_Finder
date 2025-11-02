import os
import requests
from dotenv import load_dotenv
load_dotenv()

class FlightSearch:

    def __init__(self, city_names):
        self.API_KEY = os.getenv("API_KEY")
        self.API_SECRET = os.getenv("API_SECRET")
        self.cities_list = city_names
        self.get_token = self._get_new_token()
        self.iata = self.get_names()

    def get_names(self):
        code_names = []
        server = "https://test.api.amadeus.com/v1"
        req = "/reference-data/locations/cities"
        IATA_ENDPOINT = f"{server}{req}"
        auth = {
            "Authorization" : f"Bearer {self.get_token}",
            "access_token" : self.get_token
        }

        for city in self.cities_list:
            parameters = {
                "keyword" : f"{city}"
            }

            response = requests.get(url=IATA_ENDPOINT, params=parameters, headers=auth)
            iata = response.json()["data"]
            code_names.append(iata[0]["iataCode"])

        return code_names


    def _get_new_token(self):
        TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.API_KEY,
            "client_secret": self.API_SECRET
        }

        response = requests.post(url=TOKEN_ENDPOINT, data=body, headers=header)

        return response.json()["access_token"]
