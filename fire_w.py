"""
Created on Tue Aug 19 14:27:58 2025

@author: blaken
"""

import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from wrf import getvar, interplevel

wrf_file = Dataset('/home/blaken/WRF-SFIRE/test/em_fire/wrfout_d01_0001-01-01_00:12:00')

# Gather vertical wind (W) at a specific time index
w = getvar(wrf_file, "W", timeidx=0) # timeidx=0 for the first time step, timeidx=-1 for the last, or specify a number

# Gather geopotential height (Z)
ph = getvar(wrf_file, "PH", timeidx=0) 
phb = getvar(wrf_file, "PHB", timeidx=0) 

z = (ph + phb)/ 9.81

#what height do we want the vertical wind plot?
desired_height_m = 4000  #this is in meters

w_at_height = interplevel(w, z, desired_height_m)

#Gather lats and lons for plotting
lats = getvar(wrf_file, "XLAT", timeidx=0)
lons = getvar(wrf_file, "XLONG", timeidx=0)

#plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
contour_plot = ax.contourf(lons, lats, w_at_height, cmap = 'RdBu_r', levels = np.linspace(-20 ,40, 21)) #contourf the vertical wind
cbar = fig.colorbar(contour_plot, ax=ax, orientation = 'vertical', pad = 0.05)
cbar.set_label('Vertical Wind (m/s)')
ax.set_title(f'Vertical Wind at {desired_height_m}m')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.grid('true')
#plt.savefig("vertical_wind_plot.png", dpi=300)
plt.show()
