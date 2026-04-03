import pandas as pd
import os
from utils.distance_utils import calculate_distance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

facilities_df = pd.read_csv(
    os.path.join(BASE_DIR, "../../dataset/facilities.csv")
)

population_df = pd.read_csv(
    os.path.join(BASE_DIR, "../../dataset/population.csv")
)

def get_population(lat, lon):
    total_pop = 0

    for _, row in population_df.iterrows():
        d = calculate_distance(lat, lon, row["latitude"], row["longitude"])

        if d <= 2:   # 2 KM radius
            total_pop += row["population"]

    return total_pop

def analyze_location(lat, lon, facility_type):

    nearby=[]

    for _,row in facilities_df.iterrows():

        if facility_type not in str(row["amenity"]).lower():
            continue

        d=calculate_distance(lat,lon,row["lat"],row["lon"])

        if d<=2:
            nearby.append({
                "name":row.get("name","Unknown"),
                "lat":row["lat"],
                "lon":row["lon"],
                "distance":round(d,2)
            })

    population=get_population(lat,lon)

    if nearby:
        return {
            "status":"Not Suitable",
            "population":population,
            "reason":"Facility exists nearby",
            "existing_facilities":nearby,
            "suggestions":suggest(lat,lon,facility_type)
        }

    if population<800:
        return {
            "status":"Not Suitable",
            "population":population,
            "reason":"Low population",
            "existing_facilities":[],
            "suggestions":suggest(lat,lon,facility_type)
        }

    return {
        "status":"Suitable",
        "population":population,
        "reason":"Good location",
        "existing_facilities":[],
        "suggestions":suggest(lat,lon,facility_type)
    }

def suggest(lat,lon,facility_type):

    res=[]

    for _,row in population_df.iterrows():

        d=calculate_distance(lat,lon,row["latitude"],row["longitude"])

        if d>4 or row["population"]<500:
            continue

        exists=False

        for _,f in facilities_df.iterrows():

            if facility_type not in str(f["amenity"]).lower():
                continue

            d2=calculate_distance(row["latitude"],row["longitude"],f["lat"],f["lon"])

            if d2<1:
                exists=True
                break

        if not exists:
            res.append({
                "lat":row["latitude"],
                "lon":row["longitude"],
                "population":row["population"]
            })

    return res[:3]