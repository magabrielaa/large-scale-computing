# Import required libraries
import rasterio
import numpy as np
import time

###########################################################################
#######                 (A) Serial code at 50x dataset              #######
###########################################################################

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

# Tile arrays to simulate additional data (50x)
red = np.tile(red, 50)
nir = np.tile(nir, 50)

# NDVI calculation
ndvi = (nir - red) / (nir + red)

# Print time elapsed
time_elapsed = time.time() - t0
print(f'Computation time for serial CPU implementation at 50x datasize: {time_elapsed} seconds')

###########################################################################
#######                (B) Serial code at 100x dataset              #######
###########################################################################

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

# Tile arrays to simulate additional data (100x)
red = np.tile(red, 100)
nir = np.tile(nir, 100)

# NDVI calculation
ndvi = (nir - red) / (nir + red)

# Print time elapsed
time_elapsed = time.time() - t0
print(f'Computation time for serial CPU implementation at 100x datasize: {time_elapsed} seconds')


###########################################################################
#######                (C) Serial code at 150x dataset              #######
###########################################################################

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

# Tile arrays to simulate additional data (150x)
red = np.tile(red, 150)
nir = np.tile(nir, 150)

# NDVI calculation
ndvi = (nir - red) / (nir + red)

# Print time elapsed
time_elapsed = time.time() - t0
print(f'Computation time for serial CPU implementation at 150x datasize: {time_elapsed} seconds')