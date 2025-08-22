Created on Wed Aug 20 13:05:32 2025

@author: blaken
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from wrf import getvar, interplevel, to_np, vinterp, ALL_TIMES

wrf_file = Dataset('/home/blaken/WRF-SFIRE/test/em_fire/wrfout_d01_0002-01-01_00:18:00')

# Gather the cloud water mixing ratio
qcloud = getvar(wrf_file, "QCLOUD", timeidx=ALL_TIMES)

# Gather geopotential height (Z)
ph = getvar(wrf_file, "PH") 
phb = getvar(wrf_file, "PHB") 

z = (ph + phb)/ 9.81
z_data = z.data

# Gather times
time_coord = getvar(wrf_file, "Times", timeidx=ALL_TIMES) 

# Horizontally average over time
qcloud_avg_height_horizontal = np.mean(qcloud, axis = (1,2)) 
qcloud_avg_height_horizontal_data = qcloud_avg_height_horizontal.data

# Average our height coordinate (maybe not needed)
height_coord = np.mean(z_data[:-1,:,:], axis = (1,2))

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))


line_plot = ax.plot(qcloud_avg_height_horizontal_data, height_coord, color = 'Blue')

ax.set_xlabel("Cloud water mixing ratio (kg/kg)")
ax.set_ylabel("Height (m)")
ax.set_title("Average Cloud Water Mixing ratio by Height")

plt.show()
