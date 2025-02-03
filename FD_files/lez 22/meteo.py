import sqlite3
from meteostat import Point, Daily
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd


class meteo_fetcher:

    def __init__(self, city_name:str):
        self.city_name= city_name


    def fetch_city_data(self):
        geolocator = Nominatim(user_agent="my_weather_app")
        return geolocator.geocode(self.city_name)
    
    def fetch_meteo_data(self,start:datetime, end:datetime = datetime.now().date()):
        location=self.fetch_city_data()
        city_point = Point(location.latitude, location.longitude, 20)
        start = datetime.combine(start, datetime.min.time())
        end = datetime.combine(end, datetime.min.time())
        data = Daily(city_point, start, end)
        return data.fetch()    
    

    def load_to_sql(self,df:pd.DataFrame, table_name: str):
        conn=sqlite3.connect("meteo.db")
        while True:
            df.to_sql(table_name,con=conn,if_exists="replace")
            break

        return "success"


    