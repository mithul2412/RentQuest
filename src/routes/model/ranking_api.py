from flask import Flask, jsonify, request, Blueprint
from src.routes.model import ranking_fn
from src.routes.model import midpoint
import pandas as pd

ranking_bp = Blueprint("ranking", __name__, url_prefix="/ranking")


@ranking_bp.route("/", methods=["GET"])
def ranking_function():
    return jsonify({"message": "Ranking API"})


@ranking_bp.route("/", methods=["POST"])
def ranking_post():
    data = request.json
    zipcode = midpoint.triangulate_and_find_postal_code(
        data["locations"]["house"],
        data["locations"]["office"],
        data["locations"]["friend"],
    )

    bedrooms = int(data["filters"]["bedrooms"].replace("+", ""))
    bathrooms = float(data["filters"]["bathrooms"].replace("+", ""))
    zipcode = int(zipcode["postal_code"])
    max_price = float(data["filters"]["price"].replace("$", "").replace(",", ""))
    w_rent = 0.4
    w_sqft = float(data["weights"]["space"])
    w_crime = float(data["weights"]["safety"])
    w_parking = float(data["weights"]["amenities"])
    w_neighbor = float(data["weights"]["neighborhood"])

    scores = ranking_fn.rank_apartments(
        bedrooms,
        bathrooms,
        zipcode,
        max_price,
        w_rent,
        w_sqft,
        w_crime,
        w_parking,
        w_neighbor,
    )
    final_ranking = {"success": True, "rentals": []}
    fallback_image_url = "/static/images/default_image.jpg"

    for _, row in scores.iterrows():
        image_url = (
            row["primary_photo"]
            if pd.notna(row["primary_photo"])
            else fallback_image_url
        )
        latitude = row["Latitude"] if pd.notna(row["Latitude"]) else 0.0
        longitude = row["Longitude"] if pd.notna(row["Longitude"]) else 0.0
        price = (
            f"${int(row['rent_price']):,.0f}" if pd.notna(row["rent_price"]) else "$0"
        )
        bedrooms = int(row["beds"]) if pd.notna(row["beds"]) else 0
        bathrooms = float(row["bath"]) if pd.notna(row["bath"]) else 0.0
        url = row["property_url"]
        parking_cost = row["parking_cost"]

        final_ranking["rentals"].append(
            {
                "url": url,
                "lat": latitude,
                "lng": longitude,
                "title": (
                    row["full_street_line"]
                    if pd.notna(row["full_street_line"])
                    else "No Title"
                ),
                "price": price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "imageUrl": image_url,
                "address": (
                    f"{row['full_street_line']}, {row['city']}, {row['state']}, {row['zip_code']}"
                    if pd.notna(row["full_street_line"])
                    else "No Address"
                ),
                "parking_cost": parking_cost,
            }
        )

    return jsonify(final_ranking)
