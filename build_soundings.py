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

def calc_dewpt(temp,rh):
    dewpt = 243.04*(np.log(rh/100)+((17.625*temp)/(243.04+temp)))/(17.625-np.log(rh/100) - ((17.625*temp)/(243.04+temp)))
    return dewpt


cols = ['Year', ' Month', ' Day', ' Hour', ' Hgt', ' Pres', ' Temp', ' Dewpt',
       ' RH', ' Spd', ' Dir ','JD']
fall_soundings = pickle.load(open('pickles/Fall_OAK_soundings.p','rb'))
summer_soundings = pickle.load(open('pickles/Summer_OAK_soundings.p','rb'))

mo = 10
day = 2
yr = 1995

if mo>=6 & mo<=8:
    sounding_data = summer_soundings.loc[ (summer_soundings[cols[1]]==mo) & (summer_soundings[cols[0]]==yr) & (summer_soundings[cols[2]]==day)]

if mo>=9 & mo<=11:
    sounding_data = fall_soundings.loc[ (fall_soundings[cols[1]]==mo) & (fall_soundings[cols[0]]==yr) & (fall_soundings[cols[2]]==day)]

T = convert_temperature(sounding_data[cols[6]].values,'F','C')
rh = sounding_data[cols[8]].values
sounding_data[cols[7]] = calc_dewpt(T,rh)
sounding_data = sounding_data.dropna(subset = (' Temp', ' Dewpt'),how='all').reset_index(drop=True)

hours = [np.min(sounding_data[cols[3]]), np.max(sounding_data[cols[3]])]
for i in range(len(hours)):
    one_sounding = sounding_data.loc[sounding_data[cols[3]]==hours[i]]
    T = convert_temperature(one_sounding[cols[6]].values,'F','C') * units.degC
    p = one_sounding[cols[5]].values * units.hPa
    Td = one_sounding[cols[7]].values * units.degC
    wind_speed = one_sounding[cols[-3]].values * units.knots
    wind_dir = one_sounding[cols[-2]].values * units.degrees
    u, v = mpcalc.get_wind_components(wind_speed, wind_dir)

    plt.rcParams['figure.figsize'] = (9, 9)

    skew = SkewT()
    skew.plot(p,T,'r')
    skew.plot(p,Td,'g')
    skew.plot_barbs(p,u,v)

    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    skew.ax.set_ylim(1000, 100)

    plt.title('OAK Sounding: '+ str(mo) + '/' + str(day) + '/' + str(yr) +': ' +str(int(hours[i]))+' UTC' )
    plt.savefig('images/OAK_sounding_'+ str(mo) + '_'+str(day) + '_' + str(yr) +'_' +str(int(hours[i]))+'UTC.pdf')

    plt.show()




print('end of run')