import geopandas as gpd
import rasterio
from rasterio.mask import mask
import json

# Load Visakhapatnam polygon
aoi = gpd.read_file("WorldPop_geometry.json")

# Open WorldPop raster
src = rasterio.open("ind_pop_2022.tif")

# Convert polygon to GeoJSON format
geoms = [json.loads(aoi.to_json())['features'][0]['geometry']]

# Clip population raster
out_image, out_transform = mask(src, geoms, crop=True)

# Save clipped raster
out_meta = src.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

with rasterio.open("vizag_population.tif", "w", **out_meta) as dest:
    dest.write(out_image)

print("Visakhapatnam population extracted successfully!")