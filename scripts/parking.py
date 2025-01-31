import requests
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from os import getenv


def geocode_address(address):
    geolocator = Nominatim(user_agent="address_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Could not geocode address: {address}")


def find_parking_nearby(lat, lng, api_key, radius=1000):
    print("Sending request to Google Maps API...")
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=parking&key={api_key}"
    response = requests.get(places_url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            parking_places = []
            for place in data["results"]:
                parking_places.append(
                    {
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": place.get("rating", "No rating"),
                    }
                )
            return parking_places
        else:
            raise ValueError(f"Places API failed: {data['status']}")
    else:
        raise ConnectionError("Failed to connect to Places API")


if __name__ == "__main__":
    load_dotenv()
    GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
    address = "440 Terry Ave N, Seattle, WA 98109"

    try:
        lat, lng = geocode_address(address)
        parking_places = find_parking_nearby(lat, lng, GOOGLE_API_KEY)
        sorted_parking_spots = sorted(
            parking_places, key=lambda x: x["rating"], reverse=True
        )
        top_10_parking_spots = sorted_parking_spots[:10]
        print(f"Parking places near '{address}':\n")
        for i, place in enumerate(top_10_parking_spots, start=1):
            print(f"{i}. Name: {place['name']}")
            print(f"   Address: {place['address']}")
            print(f"   Rating: {place['rating']}\n")

    except Exception as e:
        print(f"Error: {e}")
