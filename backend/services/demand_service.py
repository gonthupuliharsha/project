import pandas as pd
from utils.distance_utils import calculate_distance
from services.density_service import facility_density

population_df = pd.read_csv("../dataset/population.csv")

def demand_score(lat, lon, facility_type):

    # Get nearest population
    nearest_population = 0
    min_dist = float("inf")

    for _, row in population_df.iterrows():

        dist = calculate_distance(
            lat, lon,
            row["latitude"],
            row["longitude"]
        )

        if dist < min_dist:
            min_dist = dist
            nearest_population = row["population"]

    # Population score
    population_score = nearest_population / 5000

    # Facility scarcity
    density = facility_density(lat, lon, facility_type)

    if density == 0:
        scarcity = 1
    elif density == 1:
        scarcity = 0.7
    elif density == 2:
        scarcity = 0.4
    else:
        scarcity = 0.1

    # Accessibility
    access_score = 1 / (min_dist + 1)

    demand = (
        0.5 * population_score +
        0.3 * scarcity +
        0.2 * access_score
    )

    return demand