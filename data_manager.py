# import json
from  data_base import User_info

class DataManager:
    def __init__(self, name):
        user = User_info.query.filter_by(user_name=name).first()
        self.city_go = user.from_country
        self.city_arrive = user.to_country
        self.to_iata = user.to_iata
        self.from_iata = user.from_iata
        self.nonstop = user.nonstop
        self.going_date = user.travel_date
        self.arrival_date = user.depature_date
        self.price = user.price