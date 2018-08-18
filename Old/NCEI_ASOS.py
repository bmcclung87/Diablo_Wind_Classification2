import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from mpl_toolkits.basemap import Basemap


import re


NCEI_dir = '../Data/NCEI_data/stn/'
NCEI_dir1 = '../Data/NCEI_data/inv/'

filenames = os.listdir(NCEI_dir)
filenames1 = os.listdir(NCEI_dir1)

lat = []
lon = []
elev = []
afid = []
wbanid = []
for i in range(len(filenames)):
    fh = open(NCEI_dir+filenames[i],'r')
    loc_data = fh.readlines()
    space_start = []
    space_end = []

    for m in re.finditer(' ',loc_data[1]):
        space_start.append(m.start())
        space_end.append(m.end())
        
    for j in loc_data[2:]:
        afid.append((j[0:space_start[0]][0:6]))
        wbanid.append((j[0:space_start[0]][7:]))
        lat.append(float(j[space_end[3]:space_start[4]]))
        lon.append(float(j[space_end[4]:space_start[5]]))
        elev.append(float(j[space_end[5]:-1]))

data = np.concatenate((np.expand_dims(np.array(id).T,axis=1),\
                       np.expand_dims(np.array(wbanid).T,axis=1),\
                       np.expand_dims(np.array(lat).T,axis=1),\
                       np.expand_dims(np.array(lon).T,axis=1),\
                       np.expand_dims(np.array(elev).T,axis=1)),\
                        axis=1)
all_NCEI_ASOS = pd.DataFrame(data=data,columns=['AFID','WBANID','LAT','LON','ELEV'])

fig = plt.figure(figsize=(8, 8))
mp = Basemap(projection='lcc', resolution='h',
            width=4E5, height=4E5, 
            lat_0=37.7749, lon_0=-122.4194,)
mp.shadedrelief()
mp.drawcoastlines()
mp.drawstates()

for i in range(len(all_NCEI_ASOS)):
    x, y = mp(float(all_NCEI_ASOS['LON'][i]), float(all_NCEI_ASOS['LAT'][i]))
    plt.plot(x, y, 'ok', markersize=5,label='NCEI ASOS')

plt.title('NCEI ASOS Locations')
    
        
        
        
    
        
        
   
    
    #loc_data = pd.read_csv(NCEI_dir+filenames[i],delim_whitespace=True,skiprows=[0,1])
    #por_data = pd.read_csv(NCEI_dir1+filenames1[i],delim_whitespace=True,skiprows=[0,1])