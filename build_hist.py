import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import julian
import datetime
from datetime import timezone

dt = datetime.datetime(year=1948,month=1,day=1,hour=13,tzinfo=timezone.utc)
jd = julian.to_jd(dt, fmt='jd')

dir_bins = np.linspace(0,360,37)
speeds = np.linspace(0,40,9)
seasons = ['Summer','Fall','Winter','Spring']
pres_lvl = [925, 850, 700, 500]
cols = ['Year', ' Month', ' Day', ' Hour', ' Hgt', ' Pres', ' Temp', ' Dewpt',
       ' RH', ' Spd', ' Dir ','JD']

for i in range(len(seasons)):
   filename = 'pickles/'+seasons[i]+'_OAK_soundings.p'
   data = pickle.load(open(filename,'rb'))
   for j in range(len(pres_lvl)):
       for k in range(len(speeds)):
           spd_pres_trim = data.loc[ (data[cols[-3]]>=speeds[k]) & (data[cols[5]]>=pres_lvl[j]) & (data[cols[0]]>=1948)]

           dir_data = spd_pres_trim[cols[-2]]
           dir_data = dir_data[~np.isnan(dir_data)]
           dir_hist, bins = np.histogram(dir_data, dir_bins)
           temp_df = pd.DataFrame()
           rh_df = pd.DataFrame()
           for l in range(len(dir_bins)-1):
               dir_bin_trim = spd_pres_trim.loc[ (spd_pres_trim[cols[-2]] >= dir_bins[l]) & (spd_pres_trim[cols[-2]] < dir_bins[l+1])]

               col_heading = str(dir_bins[l])+'-'+str(dir_bins[l+1])

               temp_data = dir_bin_trim[cols[6]]
               temp_data = temp_data[~np.isnan(temp_data)].values
               temp_df[col_heading] = temp_data



               rh_data = dir_bin_trim[cols[8]]
               rh_data = rh_data[~np.isnan(rh_data)].values
               rh_df[col_heading] = rh_data

           width = np.diff(dir_bins)
           center = (dir_bins[:-1]+dir_bins[1:])/2

           plt.figure()
           plt.bar(center,dir_hist,align='center',width=width)
           plt.xlabel('Wind Direction (deg)')
           plt.ylabel('Frequency')
           plt.title(seasons[i] + ', Years: 1948-2018, Wind Speed >= ' +str(int(speeds[k])) + ' kts, for Pressures >= '+str(int(pres_lvl[j]))+' mb')
           plt.savefig('images/OAK_'+seasons[i]+'_'+str(int(pres_lvl[j]))+'mb'+'_'+str(int(speeds[k]))+'kts')
           plt.close()

print(t2_data.shape)
print(hum_data.shape)

print('end of script')