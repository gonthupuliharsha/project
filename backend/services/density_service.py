import pandas as pd
from utils.distance_utils import calculate_distance

facilities_df = pd.read_csv("../dataset/facilities.csv")

def facility_density(lat, lon, facility_type, radius=3):

    count = 0

    for _, row in facilities_df.iterrows():

        if row["amenity"] != facility_type:
            continue

        dist = calculate_distance(
            lat,
            lon,
            row["lat"],
            row["lon"]
        )

        if dist <= radius:
            count += 1

    return count