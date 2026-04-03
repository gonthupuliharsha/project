import rasterio
import pandas as pd
import numpy as np

# Open the clipped population raster
src = rasterio.open("vizag_population.tif")

band = src.read(1)

rows, cols = band.shape

data = []

for row in range(rows):
    for col in range(cols):

        population = band[row, col]

        if population > 0:  # ignore empty cells
            lon, lat = src.xy(row, col)

            data.append([lat, lon, population])

df = pd.DataFrame(data, columns=["latitude", "longitude", "population"])

df.to_csv("vizag_population.csv", index=False)

print("Population CSV created successfully!")