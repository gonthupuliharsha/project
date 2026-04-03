from services.density_service import facility_density

def calculate_score(lat, lon, population, distance, facility_type):

    # Normalize population
    population_score = population / 5000

    # Facility gap score
    density = facility_density(lat, lon, facility_type)

    if density == 0:
        facility_score = 1
    elif density == 1:
        facility_score = 0.7
    elif density == 2:
        facility_score = 0.4
    else:
        facility_score = 0.1

    # Distance score
    distance_score = 1 / (distance + 1)

    score = (
        0.5 * population_score +
        0.3 * facility_score +
        0.2 * distance_score
    )

    return score