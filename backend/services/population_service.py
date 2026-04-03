import pandas as pd
import numpy as np
from utils.distance_utils import calculate_distance

# Load dataset once
population_df = pd.read_csv("../dataset/population.csv")

# Convert to numpy arrays for faster processing
pop_lat = population_df["latitude"].values
pop_lon = population_df["longitude"].values
pop_val = population_df["population"].values


def get_population(lat, lon):

    min_dist = float("inf")
    population = 0

    for i in range(len(pop_lat)):

        dist = calculate_distance(lat, lon, pop_lat[i], pop_lon[i])

        if dist < min_dist:
            min_dist = dist
            population = pop_val[i]

    return population