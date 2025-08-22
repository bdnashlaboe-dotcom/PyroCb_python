"""
Created on Tue Aug 19 16:16:18 2025

@author: blaken
"""

import numpy as np
import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import math
import wrf

def wrf_out_read (dir, time):
    mins= time % 60
    hrs = math.floor(time / 60)
    wrfout = Dataset('{}wrfout_d01_0001-01-01_{:02d}:{:02d}:00'.format(dir, hrs, mins)) #Format of the name of the output file must be corrected accordingly
    return wrfout

def relax_zone_remover (input, sr):
    output = input
    for _ in range(sr):
        output = np.delete(output, -1, 0)
        output = np.delete(output, -1, 1)
    return output
def fire_perimeter_plot(xf, yf, lfn, color):
    #removing the relaxation zones of the level-set function
    lfn_reinit = relax_zone_remover(lfn, sr)
    xf = relax_zone_remover(xf, sr)
    yf = relax_zone_remover(yf, sr)
    #Plotting the fire perimeter
    ax.contour(xf, yf, lfn_reinit, 0, colors='r')
    ax.plot([], [], color=color, label='Fire Line ($\phi>0)$')

def wind_plot (data, xcoords, ycoords, field_1, field_2, height_value, color):
    u = wrf.getvar(data, field_1, timeidx=wrf.ALL_TIMES, method='cat', meta=False)
    v = wrf.getvar(data, field_2, timeidx=wrf.ALL_TIMES, method='cat', meta=False)
    u = u[height_value, :, :]
    v = v[height_value, :, :]
    # quiver formats (starting coordinate X, starting coordinate Y, U direction, V direction)
    wf = plt.quiver(xcoords[::8,::8], ycoords[::8,::8], u[::8,::8], v[::8,::8], color = color, scale = 8, scale_units = 'xy', pivot = 'tail', width = 0.002)
    return wf


out_time = 12 #Output time to plot in minutes
sr = 4 #sub-grid ratio

#wrfout files with reinit
outs_folder = '/home/blaken/WRF-SFIRE/test/em_fire/'
wrfouts_reinit = wrf_out_read(outs_folder, out_time)

#reading coordiantes
x = wrf.getvar(wrfouts_reinit, 'XLONG', timeidx=wrf.ALL_TIMES, method='cat', meta=False) / 1000   #converting coordinates to km
y = wrf.getvar(wrfouts_reinit, 'XLAT', timeidx=wrf.ALL_TIMES, method='cat', meta=False) / 1000
xf = wrf.getvar(wrfouts_reinit, 'FXLONG', timeidx=wrf.ALL_TIMES, method='cat', meta=False) / 1000   #converting coordinates to km #xf and yf indicate fire grid x and y
yf = wrf.getvar(wrfouts_reinit, 'FXLAT', timeidx=wrf.ALL_TIMES, method='cat', meta=False) / 1000

#reading data to single array
lfn = wrf.getvar(wrfouts_reinit, 'LFN', timeidx=wrf.ALL_TIMES, method='cat', meta=False)    #Level-set values
hgt = wrf.getvar(wrfouts_reinit, 'HGT', timeidx=wrf.ALL_TIMES, method='cat', meta=False)   #Terrain height

w = wrf.getvar(wrfouts_reinit, "W", timeidx=0)

# Gather geopotential height (Z)
ph = wrf.getvar(wrfouts_reinit, "PH", timeidx=0) 
phb = wrf.getvar(wrfouts_reinit, "PHB", timeidx=0) 

z = (ph + phb)/ 9.81

#what height do we want the vertical wind plot?
desired_height_m = 4000  #this is in meters

w_at_height = wrf.interplevel(w, z, desired_height_m)

fig = plt.figure()
ax = plt.subplot2grid((1,1), (0,0))

fire_perimeter_plot(xf, yf, lfn, color='red')
#Plotting the vertical wind
contour_plot = ax.contourf(x, y, w_at_height, cmap = 'bwr', levels = np.linspace(-20 ,40, 41))
cbar = fig.colorbar(contour_plot, ax=ax, orientation = 'vertical', pad = 0.05)
#cbar = plt.colorbar()
#cbar.set_label('Terrain Height (m)')

#find our horizontal wind level
z_level = z[6, :, :] #the level is one below (starts at 0), input the wf level 
print(f'Approximate horizontal wind level {z_level}')

#plotting the wind arrows
wf = wind_plot(wrfouts_reinit, x, y, 'ua', 'va', 6, 'k') #the second to last in the parenthesis will be our u/v vertical level
plt.quiverkey(wf, 0.7, 0.9, U=5, label=r'$5 \frac{m}{s}$', labelpos='E', coordinates='figure', color = 'k')

ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')

plt.ylabel('Y (km)')
plt.xlabel('X (km)')
plt.title('Shear fire perimeter after 12 minutes')
plt.legend()
plt.xlim(0, 5)
plt.xticks(np.arange(0, 30, 5))
plt.ylim(0, 5)
plt.yticks(np.arange(0, 30, 5))
#plt.savefig("wind_perimeter_plot.png", dpi=300)
plt.show()
plt.close()
