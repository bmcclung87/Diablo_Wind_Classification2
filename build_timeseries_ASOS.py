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


def plot_timeseries(data):
    wind_spd = data['spd'].values
    max = data['max'].values
    wind_dir = data['dir'].values
    temp = data['temp'].values
    dewpt = data['dewpt'].values
    rh = data['rh'].values
    slp = data['slp'].values

    plt.rcParams['figure.figsize'] = (16, 9)
    fig = plt.figure()
    plt.subplot(411)
    plt.plot(wind_spd, 'b', label='Speed')
    plt.plot(max, 'r', label='Max')
    plt.legend(loc=2)
    plt.ylabel('Wind Speed (kts)')
    plt.subplot(412)
    plt.plot(wind_dir)
    plt.ylabel('Wind Direction (deg)')
    plt.subplot(413)
    plt.plot(temp, 'r', label='Temperature')
    plt.plot(dewpt, 'g', label='Dew Point')
    plt.legend(loc=2)
    plt.ylabel('Temperature (F)')
    plt.subplot(414)
    plt.plot(rh)
    plt.ylabel('Relative Humidity %')
    plt.xlabel('# Obs')

    fig.suptitle(locs[i].upper() + ' Time Series: ' + str(mo) + '/' + str(day) + '/' + str(yr))
    plt.savefig('images/' + locs[i].upper() + '_Time Series_' + str(mo) + '_' + str(day) + '_' + str(yr) + '.pdf')
    plt.close()


dir = 'sfc_data/ASOS_data/'
locs = ['kapc','kdvo','ksts']

mo = 10
day = 2
yr = 1995

for i in range(len(locs)):
    filename = dir+locs[i]+'.dat'
    data = pd.read_csv(filename, delim_whitespace=True)
    data = data.loc[(data['year']==yr) & (data['day']==day) & (data['month']==mo)]
    plot_timeseries(data)

dir = 'sfc_data/RAWS_data/'


for i in range(len(locs)):
    filename =dir+'rw_allyr_'+locs[i]+'.dat'
    data = pd.read_csv(filename, delim_whitespace=True)
    data = data.loc[(data['year'] == yr) & (data['day'] == day) & (data['month'] == mo)]
    plot_timeseries(data)

print('end of script')