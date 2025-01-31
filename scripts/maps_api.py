from dotenv import load_dotenv
from os import getenv
import requests
import csv
import time


def fetch_nearby_places(api_key, location, radius, place_types):
    all_places = []
    print("Fetching Nearby Places... for location:", location)
    for place_type in place_types:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place_type}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for place in results:
                all_places.append(
                    {
                        "name": place.get("name", "Unknown"),
                        "type": place_type,
                        "lat": place["geometry"]["location"]["lat"],
                        "lng": place["geometry"]["location"]["lng"],
                    }
                )
    return all_places


if __name__ == "__main__":
    load_dotenv()
    api_key = getenv("GOOGLE_API_KEY")
    place_types = [
        "restaurant",
        "grocery_or_supermarket",
        "cafe",
        "park",
        "school",
        "hospital",
        "parking",
    ]
    with open("data/HomeHarvest_2025-1-25_10-48-41.csv", mode="r") as file:
        csvFile = csv.reader(file)
        data = []
        for lines in csvFile:
            if lines[29] == "latitude":
                continue
            data.append([lines[0], lines[29], lines[30]])

    c = 0
    for loc in data:
        c += 1
        if c <= 125:
            continue
        location = loc[1] + "," + loc[2]
        radius = 1000

        places = fetch_nearby_places(api_key, location, radius, place_types)

        # print("List of Nearby Places:")
        # for place in places:
        #     print(f"{place['name']} - {place['type']}")

        # Find count of restaurants and other items

        for place_type in place_types:
            count = 0
            for place in places:
                if place["type"] == place_type:
                    count += 1
            loc.append(count)

        with open("data/nearby_places.csv", mode="a", newline="") as file:
            csvFile = csv.writer(file)
            csvFile.writerow(loc)

        time.sleep(1)
