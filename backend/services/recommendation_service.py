import os
import pandas as pd
from utils.distance_utils import calculate_distance

# ✅ ADD THESE (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

population_df = pd.read_csv(
    os.path.join(BASE_DIR, "../../dataset/population.csv")
)

facilities_df = pd.read_csv(
    os.path.join(BASE_DIR, "../../dataset/facilities.csv")
)

def generate_recommendation_zones(facility_type):

    zones = []

    # 🔥 LIMIT DATA (VERY IMPORTANT)
    sample_population = population_df.sample(300)   # only first 300 rows

    for _, row in sample_population.iterrows():

        lat = row["latitude"]
        lon = row["longitude"]
        population = row["population"]

        count = 0

        # 🔥 LIMIT FACILITIES ALSO
        sample_facilities = facilities_df.head(300)

        for _, f in sample_facilities.iterrows():

            if facility_type.lower() not in str(f["amenity"]).lower():
              continue

            dist = calculate_distance(
                lat, lon,
                f["lat"], f["lon"]
            )

            if dist <= 2:
                count += 1
        score = population / (count + 1)
            
        # zone logic
        if population > 30 and count <= 2:
            zone = "green"
        elif population > 20 and count <= 3:
            zone = "yellow"
        elif count >= 4:
            zone = "red"
        else:
            zone = "blue"
        if zone in ['green', 'yellow']:
            zones.append({
                "lat": lat,
                "lon": lon,
                "zone": zone,
                "population": population,
                "score": score
            })

    # Sort zones by score (highest first)
    zones = sorted(zones, key=lambda x: x["score"], reverse=True)
# Return top 20 best zones
    # 🧠 Spread zones across map (GRID BASED)
    grid = {}

    for z in zones:
    # create grid key (approx area)
        key = (round(z["lat"], 2), round(z["lon"], 2))

        if key not in grid:
           grid[key] = []

        grid[key].append(z)

# pick best from each grid
    final_zones = []

    for key in grid:
    # sort each grid by score
        sorted_grid = sorted(grid[key], key=lambda x: x["score"], reverse=True)
        final_zones.append(sorted_grid[0])  # best in that area

# limit results
    return final_zones[:20]