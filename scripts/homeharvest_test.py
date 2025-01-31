from homeharvest import scrape_property
from datetime import datetime

# Generate filename based on current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"HomeHarvest_{current_timestamp}.csv"

properties = scrape_property(
    location="Seattle",
    listing_type="for_rent",
    past_days=999,
)
print(f"Number of properties: {len(properties)}")

properties.to_csv(filename, index=False)
print(properties.head())
