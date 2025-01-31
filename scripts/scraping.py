import requests
from bs4 import BeautifulSoup
import csv
import time


def scraping_data():
    with open("data/HomeHarvest_2025-1-25_10-48-41.csv", mode="r") as file:
        csvFile = csv.reader(file)
        url = []
        for lines in csvFile:
            if lines:
                modified_url = lines[0].replace(
                    "realestateandhomes-detail", "rentals/details"
                )
                url.append(modified_url)

    for i in range(79, len(url)):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url[i], headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(20)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        time.sleep(2)
        try:
            beds = (
                soup.find("li", {"data-testid": "property-meta-beds"})
                .find("span", {"data-testid": "meta-value"})
                .text.strip()
            )
        except AttributeError:
            beds = "NA"

        try:
            baths = (
                soup.find("li", {"data-testid": "property-meta-baths"})
                .find("span", {"data-testid": "meta-value"})
                .text.strip()
            )
        except AttributeError:
            baths = "NA"

        try:
            sqft = (
                soup.find("li", {"data-testid": "property-meta-sqft"})
                .find("span", {"data-testid": "meta-value"})
                .text.strip()
            )
        except AttributeError:
            sqft = "NA"

        # Saving the results to a csv file
        with open("data/bed-bath-sq.csv", mode="a", newline="") as file:
            csvFile = csv.writer(file)
            csvFile.writerow([url[i], beds, baths, sqft])
        print(f"Entry {i}: Data scraped from {url[i]}")


if __name__ == "__main__":
    scraping_data()
