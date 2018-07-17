import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import datetime
from datetime import timezone
from mpl_toolkits.basemap import Basemap
from diablo_functions import *

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso

key = 'b1c91e501782441d97ac056e2501b5b0'
m = Meso(token=key)
PGE_stnids = pd.read_excel('/Users/brandonmcclung/Documents/Dissertation/fire_list.xlsx',sheet_name='PGE_Sites')
PGE_stnids = PGE_stnids.dropna(how='all')
PGE_stnids = PGE_stnids['id']

RAWS_stnids = pd.read_excel('/Users/brandonmcclung/Documents/Dissertation/fire_list.xlsx',sheet_name='RAWS_Sites')
RAWS_stnids = RAWS_stnids.dropna(how='all')
RAWS_stnids = RAWS_stnids['id']

for n,x in enumerate(PGE_stnids):
    print(x)
    stations = m.metadata(stid=x)
    if n==0:
        lat = stations['STATION'][0]['LATITUDE']
        lon = stations['STATION'][0]['LONGITUDE']
        elev = stations['STATION'][0]['ELEVATION']
    else:
        lat = np.append(lat,stations['STATION'][0]['LATITUDE'])
        lon = np.append(lon,stations['STATION'][0]['LONGITUDE'])
        elev = np.append(elev,stations['STATION'][0]['ELEVATION'])

for n,x in enumerate(RAWS_stnids):
    print(x)
    stations = m.metadata(stid=x)
    if n>599:
        build_pd(x)
    if n==0:
        lat1 = stations['STATION'][0]['LATITUDE']
        lon1 = stations['STATION'][0]['LONGITUDE']
        elev1 = stations['STATION'][0]['ELEVATION']
    else:
        lat1 = np.append(lat1,stations['STATION'][0]['LATITUDE'])
        lon1 = np.append(lon1,stations['STATION'][0]['LONGITUDE'])
        elev1 = np.append(elev1,stations['STATION'][0]['ELEVATION'])


fig = plt.figure(figsize=(8, 8))
mp = Basemap(projection='lcc', resolution='h',
            width=4E5, height=4E5, 
            lat_0=37.7749, lon_0=-122.4194,)
mp.shadedrelief()
mp.drawcoastlines()
mp.drawstates()

# Map (long, lat) to (x, y) for plotting
x, y = mp(lon, lat)
x1,y1 = mp(lon1, lat1)

plt.plot(x, y, 'ok', markersize=5,label='PGE')
plt.plot(x1,y1,'or',markersize=5,label='RAWS')
plt.legend()
plt.title('Mesonet Locations')
plt.savefig('../Images/PGE_map.pdf')
plt.show()       

        
