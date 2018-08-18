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

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso

def find_diablo_obs(data):
    spd_threshold = 21.7244 #knots (25 mph)

    dir_threshold1 = 315 #degrees
    dir_threshold2 = 135

    rh_threshold = 30 #percent

    #find where the data is within the thresholds, no time dependence (i.e. winds dont have to last 3 hours)
    data_dir = pd.concat([data.loc[data['Dir']>=dir_threshold1],data.loc[(data['Dir']>=0) & (data['Dir']<=dir_threshold2)]])
    data_spd = data_dir.loc[(data_dir['Spd']>=spd_threshold)]
    data_rh = data_spd.loc[(data_spd['RH']<=rh_threshold)]

    #remove duplicate days to get list of days only
    days = data_rh.drop_duplicates(subset = ['Year','Month','Day'],keep='first')[['Year','Month','Day']]

    return data_rh, days




key = 'b1c91e501782441d97ac056e2501b5b0'
m = Meso(token=key)
stn_ids = ['BBEC1','OVYC1','NBRC1','NVHC1','WDAC1','BKSC1','KNXC1','KELC1','ATLC1','RSAC1','HWKC1',\
           'LKRC1','BNVC1','OAAC1','PLEC1','ONOC1','OKSC1','LTRC1','PIBC1','LVMC1','VAQC1','LVFC1',\
           'BNGC1','RRRC1','CISC1','SETC1','RNYC1','DOGC1','SMDC1','TADC1', 'DUCC1','HLLC1','STUC1',\
           'PKCC1','SLEC1']

for i in range(len(stn_ids)):
    print(stn_ids[i])
    filename = 'pickles/'+stn_ids[i]+'_20yr_RAWS.p'
    data = pickle.load(open(filename,'rb'))
    diablo_obs, diablo_days = find_diablo_obs(data)

    #make scatter plot of the data
    plt.figure(i)
    plt.scatter(data['Dir'],data['Spd'],1.5,'k')
    plt.scatter(diablo_obs['Dir'],diablo_obs['Spd'],3,'m',edgecolors='m')
    plt.ylabel('Wind Speed (kts)')
    plt.xlabel('Wind Direction (deg)')
    plt.xticks([0, 45, 90, 135, 180, 225, 270, 315],['0', '45', '90', '135', '180', '225', '270', '315'])
    plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40],['0','5','10','15','20','25','30','35','40'])
    plt.xlim([0, 360])
    plt.ylim([0,40])
    plt.grid(True)
    plt.title(stn_ids[i].upper()+ ' Scatter Plot: Diablo Obs = ' +str(len(diablo_obs)) + ' / Total Obs: '+str(len(data)))
    plt.savefig('images/20180626/scatter_'+stn_ids[i]+'.pdf')
    plt.savefig('images/20180626/scatter_'+stn_ids[i]+'.png')
    plt.close()

    pickle.dump(diablo_obs,open('pickles/'+stn_ids[i]+'_diablo_obs.p','wb'))
    pickle.dump(diablo_days,open('pickles/'+stn_ids[i]+'_diablo_day.p','wb'))
    stations = m.metadata(stid=stn_ids[i])
    pickle.dump([stations['STATION'][0]['LATITUDE'],stations['STATION'][0]['LONGITUDE'],stations['STATION'][0]['ELEV_DEM']],open('pickles/'+stn_ids[i]+'meta.p','wb'))

