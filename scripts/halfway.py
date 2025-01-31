import requests
import time


def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1,
    }
    headers = {"User-Agent": "MyGeocodingApp/1.0 (myemail@example.com)"}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    if response.status_code == 403:
        raise ValueError(
            "Access forbidden: Ensure you're following the Nominatim usage policy."
        )
    response.raise_for_status()  # Raise an exception for other HTTP errors
    data = response.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        raise ValueError(f"Could not geocode address: {address}")


def get_postal_code(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "addressdetails": 1,
    }
    headers = {"User-Agent": "MyGeocodingApp/1.0 (myemail@example.com)"}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    if response.status_code == 403:
        raise ValueError(
            "Access forbidden: Ensure you're following the Nominatim usage policy."
        )
    response.raise_for_status()
    data = response.json()
    if data and "address" in data:
        return data["address"].get("postcode", "Postal code not found")
    return "Postal code not found"


def triangulate_and_find_postal_code(address1, address2, address3=None):
    loc1_lat, loc1_lon = geocode_address(address1)
    time.sleep(1)  # Respect rate limits
    loc2_lat, loc2_lon = geocode_address(address2)
    time.sleep(1)

    if address3:
        loc3_lat, loc3_lon = geocode_address(address3)
        time.sleep(1)
        result_lat = (loc1_lat + loc2_lat + loc3_lat) / 3
        result_lon = (loc1_lon + loc2_lon + loc3_lon) / 3
    else:
        result_lat = (loc1_lat + loc2_lat) / 2
        result_lon = (loc1_lon + loc2_lon) / 2

    postal_code = get_postal_code(result_lat, result_lon)

    return {
        "coordinates": (result_lat, result_lon),
        "postal_code": postal_code,
    }


if __name__ == "__main__":
    address_1 = "440 Terry Ave N, Seattle, WA 98109"
    address_2 = "4225 9th Ave NE, Seattle, WA 98105"
    address_3 = "400 Broad St, Seattle, WA 98109"

    print("Using Three Points:")
    result_three_points = triangulate_and_find_postal_code(
        address_1, address_2, address_3
    )
    print(f"Coordinates: {result_three_points['coordinates']}")
    print(f"Postal Code: {result_three_points['postal_code']}")

    print("\nUsing Two Points:")
    result_two_points = triangulate_and_find_postal_code(address_1, address_2)
    print(f"Coordinates: {result_two_points['coordinates']}")
    print(f"Postal Code: {result_two_points['postal_code']}")
