import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def clean_numeric(x):
    """Cleans string values containing numbers (with commas, etc.)
    and converts them into floats."""
    if isinstance(x, str):
        return pd.to_numeric(x.replace(",", ""), errors="coerce")
    return x


def compute_ideal_best_worst(weighted_data, impacts):
    """
    Computes the ideal best and ideal worst for each column based on the impact.
    If impact == 1 (beneficial), ideal best = max, ideal worst = min.
    If impact == -1 (cost), ideal best = min, ideal worst = max.
    """
    ideal_best = []
    ideal_worst = []
    for j in range(weighted_data.shape[1]):
        if impacts[j] == 1:
            ideal_best.append(np.max(weighted_data[:, j]))
            ideal_worst.append(np.min(weighted_data[:, j]))
        else:
            ideal_best.append(np.min(weighted_data[:, j]))
            ideal_worst.append(np.max(weighted_data[:, j]))
    return np.array(ideal_best), np.array(ideal_worst)


def topsis(data, weights, impacts):
    """
    Applies TOPSIS to the given 2D NumPy array `data`, with
    corresponding `weights` and `impacts`.
    """
    # 1) Min-max normalization
    scaler = MinMaxScaler()
    norm_data = scaler.fit_transform(data)

    # 2) Multiply by the weights (rent is fixed, other weights are normalized among themselves)
    weighted_data = norm_data * weights

    # 3) Determine ideal best and worst
    ideal_best, ideal_worst = compute_ideal_best_worst(weighted_data, impacts)

    # 4) Calculate distances
    distance_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # 5) Relative closeness
    denominator = distance_best + distance_worst
    denominator[denominator == 0] = 1e-9
    scores = distance_worst / denominator
    return scores


def rank_apartments(
    bedrooms,
    bathrooms,
    zipcode,
    max_price,
    w_rent,
    w_sqft,
    w_crime,
    w_parking,
    w_neighbor,
):
    """
    :param bedrooms:  int
    :param bathrooms: int
    :param zipcode:   int
    :param max_price: float
    :param w_rent:    fixed weight for rent_price
    :param w_sqft:    weight (0-1) for sqft
    :param w_crime:   weight (0-1) for crime_score
    :param w_parking: weight (0-1) for parking
    :param w_neighbor:weight (0-1) for Neighbourhood Amenities
    """
    data = pd.read_csv("D:/CS/GitHub/RentQuest/data/final_dataset.csv")

    # Sum up neighborhood amenities
    data["Neighbourhood Amenities"] = data[
        ["restaurant", "grocery", "cafe", "park", "school", "hospital"]
    ].sum(axis=1)

    # Clean numeric columns
    numeric_columns = [
        "rent_price",
        "sqft",
        "crime_score",
        "parking",
        "Neighbourhood Amenities",
    ]
    for col in numeric_columns:
        data[col] = data[col].apply(clean_numeric)

    # --------------------------------------------------------
    # Filter logic:
    # For bedrooms: if user says 4, we do (beds >= 4). Otherwise (beds == bedrooms).
    # For bathrooms: same logic. Adjust if you want bathrooms always exact.
    # --------------------------------------------------------
    if bedrooms == 4:
        bed_condition = data["beds"] >= 4
    else:
        bed_condition = data["beds"] == bedrooms

    if bathrooms == 2.0:
        bath_condition = data["bath"] >= 2.0
    else:
        bath_condition = data["bath"] == bathrooms

    filtered_data = data[
        bed_condition
        & bath_condition
        & (data["zip_code"] == zipcode)
        & (data["rent_price"] <= max_price)
    ].copy()

    # If none match, return empty
    if filtered_data.empty:
        return pd.DataFrame()

    # Drop rows with NaNs in relevant columns
    criteria = [
        "rent_price",
        "sqft",
        "crime_score",
        "parking",
        "Neighbourhood Amenities",
    ]
    filtered_data.dropna(subset=criteria, inplace=True)
    if filtered_data.empty:
        return pd.DataFrame()

    data_topsis = filtered_data[criteria].to_numpy()

    # --------------------------------------------------------
    # Normalize only the user-input weights for sqft, crime, parking, neighbor
    # w_rent is fixed, not normalized
    # --------------------------------------------------------
    other_sum = w_sqft + w_crime + w_parking + w_neighbor
    if other_sum == 0:
        normalized_sqft = 0
        normalized_crime = 0
        normalized_parking = 0
        normalized_neighbor = 0
    else:
        normalized_sqft = w_sqft / other_sum
        normalized_crime = w_crime / other_sum
        normalized_parking = w_parking / other_sum
        normalized_neighbor = w_neighbor / other_sum

    weights = np.array(
        [
            w_rent,
            normalized_sqft,
            normalized_crime,
            normalized_parking,
            normalized_neighbor,
        ]
    )

    # Impacts for each criterion:
    # rent_price: cost (-1), sqft: benefit (+1), crime_score: cost (-1)
    # parking: benefit (+1), Neighbourhood Amenities: benefit (+1)
    impacts = np.array([-1, 1, -1, 1, 1])

    # Single-row check
    if len(filtered_data) == 1:
        filtered_data["TOPSIS_Score"] = 1.0
        filtered_data["Rank"] = 1
        return filtered_data

    # Calculate TOPSIS scores
    scores = topsis(data_topsis, weights, impacts)
    filtered_data["TOPSIS_Score"] = scores
    filtered_data["Rank"] = filtered_data["TOPSIS_Score"].rank(
        ascending=False, method="min"
    )

    return filtered_data.sort_values("Rank")


if __name__ == "__main__":
    # Fixed weight for rent
    w_rent = 0.4

    # Get user input for other weights
    w_sqft = float(input("Square footage weight (0-1): "))
    w_crime = float(input("Crime Score weight (0-1): "))
    w_parking = float(input("Parking weight (0-1): "))
    w_neighbor = float(input("Neighbourhood Amenities weight (0-1): "))

    # Get user input for property filters
    bedrooms = int(input("Required number of bedrooms: "))
    bathrooms = int(input("Required number of bathrooms: "))
    zipcode = int(input("Desired zipcode: "))
    max_price = float(input("Maximum rent price: "))

    # Call the ranking function
    result = rank_apartments(
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
    print(result)
    # Show results
    if result.empty:
        print("No apartments match the criteria.")
    else:
        print(
            result[
                [
                    "full_street_line",
                    "rent_price",
                    "beds",
                    "bath",
                    "sqft",
                    "TOPSIS_Score",
                    "Rank",
                ]
            ].head(10)
        )
