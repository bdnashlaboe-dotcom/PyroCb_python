"""
Created on Wed Aug 20 11:45:02 2025

@author: blaken
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from wrf import getvar, interplevel, to_np
import cartopy.crs as crs
import cartopy.feature as cfeature

# Import our file at desired time
wrf_file = Dataset('/home/blaken/WRF-SFIRE/test/em_fire/wrfout_d01_0001-01-01_00:18:00')

# Gather the cloud water mixing ratio
qcloud = getvar(wrf_file, "QCLOUD", timeidx=0)
qcloud_data = qcloud.data #take the data out from the object

# Gather geopotential height (Z)
ph = getvar(wrf_file, "PH", timeidx=0) 
ph_data = ph.data
phb = getvar(wrf_file, "PHB", timeidx=0) 
phb_data = phb.data

z = (ph_data + phb_data)/ 9.81

# We have to reshape to match the shape of qcloud
z_reshape = z[:-1, :, :]

# What height do we want the vertical wind plot?
desired_height_m = 5900  #this is in meters

# Find the cloud water mixing ratio at that height
qcloud_at_height = interplevel(qcloud_data, z_reshape, desired_height_m)

# Gather lats and lons for plotting
lats = getvar(wrf_file, "XLAT", timeidx=0)
lons = getvar(wrf_file, "XLONG", timeidx=0)

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
contour_plot = ax.contourf(lons, lats, qcloud_at_height, cmap = 'viridis', levels = np.linspace(0 ,0.0005, 11)) #contourf the vertical wind
cbar = fig.colorbar(contour_plot, ax=ax, orientation = 'vertical', pad = 0.05)
cbar.set_label('Cloud Water Mixing Ratio (kg/kg)')
ax.set_title(f'Cloud Water Mixing Ratio at {desired_height_m}m')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.grid('true')
#plt.savefig("vertical_wind_plot.png", dpi=300)
plt.show()
