import requests
import json
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import pymongo
from pymongo import MongoClient

# Geolocator object to get latitude and longitude from city name
geolocator = Nominatim(user_agent="Air-Quality")

# API key for the Air Quality Open Data Platform
API_KEY = '128d5dfbee02521f1ef91d6cf86024717e64bedf'
MongoUrl='mongodb://localhost:27017/'


def get_aqi():
    # Get city input from user
    print("Getting city input from user...")
    while True:
        try:
            city = input("Enter the name of a city: ")
            state = input("Enter State (Two Letters): ")
            location = f"{city}, {state}"
            location = geolocator.geocode(location)
            lat = location.latitude
            long = location.longitude
            break
        except GeocoderUnavailable:
            print("Invalid Entry")

    # Get data from API
    print("Getting data from API...")
    response = requests.get(f'https://api.waqi.info/feed/geo:{lat};{long}/?token={API_KEY}').json()
    print(response)

    # Check if there is an air quality station in the city
    if 'aqi' in response['data']:
        aqi = response['data']['aqi']
    else:
        # Find the nearest air quality station
        print("Finding nearest air quality station...")
        stations_response = requests.get(f'https://api.waqi.info/map/bounds/?token={API_KEY}&latlng={lat},{long},10').json()
        nearest_station = None
        min_distance = float('inf')
        for station in stations_response['data']:
            station_lat = radians(station['lat'])
            station_lon = radians(station['lon'])
            dlat = station_lat - radians(lat)
            dlon = station_lon - radians(long)
            a = sin(dlat / 2) ** 2 + cos(radians(lat)) * cos(station_lat) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371 * c
            if distance < min_distance:
                nearest_station = station
                min_distance = distance

        # Retrieve data from nearest station
        print("Retrieving data from nearest station...")
        response = requests.get(f'https://api.waqi.info/feed/geo:{nearest_station["lat"]};{nearest_station["lon"]}/?token={API_KEY}').json()
        aqi = response['data']['aqi']

    # Print AQI
    print(f'The AQI in {city} is {aqi}')
client = MongoClient(MongoUrl)
db = client['HackKean']
collection = db['Air Quality Information']



get_aqi()

