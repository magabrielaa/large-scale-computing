# Import required libraries
import rasterio
import numpy as np
import time

# Start time:
t0 = time.time()

# Import bands as separate images; in /project2/macs30113 on Midway2
band4 = rasterio.open(
      '/project2/macs30113/landsat8/LC08_B4.tif') #red
band5 = rasterio.open(
      '/project2/macs30113/landsat8/LC08_B5.tif') #nir

# Convert nir and red objects to float64 arrays
red = band4.read(1).astype('float64')
nir = band5.read(1).astype('float64')

# NDVI calculation
ndvi = (nir - red) / (nir + red)

# Print time elapsed
time_elapsed = time.time() - t0
print(f'Computation time for serial CPU implementation: {time_elapsed} seconds')