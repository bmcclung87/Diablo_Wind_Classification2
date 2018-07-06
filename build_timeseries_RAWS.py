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

def build_pd(stn_id):
    key = 'b1c91e501782441d97ac056e2501b5b0'
    m = Meso(token=key)
    time = m.timeseries(stid=stn_id, start='199801010000', end='201801010000')
    ob = time['STATION'][0]
    temp = np.expand_dims(np.array(ob['OBSERVATIONS']['air_temp_set_1'], dtype=np.float),axis=1)
    wind_dir = np.expand_dims(np.array(ob['OBSERVATIONS']['wind_direction_set_1'], dtype=np.float),axis=1) * units.degrees
    wind_spd = np.expand_dims(np.array(ob['OBSERVATIONS']['wind_speed_set_1'], dtype=np.float),axis=1) * 1.9438445
    wind_max = np.expand_dims(np.array(ob['OBSERVATIONS']['peak_wind_speed_set_1'], dtype=np.float),axis=1) * 1.9438445
    u, v = mpcalc.get_wind_components(wind_spd, wind_dir)
    rel_hum = np.expand_dims(np.array(ob['OBSERVATIONS']['relative_humidity_set_1'],dtype=np.float),axis=1)

    dates = ob['OBSERVATIONS']['date_time']
    years = float(dates[0][0:4])
    months = float(dates[0][5:7])
    hours = float(dates[0][8:10])
    days = float(dates[0][11:13])

    for i in range(len(dates)-1):
        years = np.vstack((years,float(dates[i+1][0:4])))
        months = np.vstack((months,float(dates[i+1][5:7])))
        days = np.vstack((days,float(dates[i+1][8:10])))
        hours = np.vstack((hours,float(dates[i+1][11:13])))

    minutes = np.expand_dims(np.ones(len(hours))*55.0,axis=1)
    cols = ['Year','Month','Day','Hour','Minutes','Temp','RH','Dir','Spd','Max','U','V']
    data = np.hstack((years,months,days,hours,minutes,temp,rel_hum,wind_dir,wind_spd,wind_max,u,v))
    data = pd.DataFrame(data=data,columns=cols)
    pickle.dump(data,open('pickles/'+stn_id+'_20yr_RAWS.p','wb'))
    return data

def plot_RAWS(data,stn_id,file):
    cols = ['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Temp', 'RH', 'Dir', 'Spd', 'Max', 'U', 'V']
    xlabels, xindices = get_xlabels(data)
    plt.rcParams['figure.figsize'] = (16, 9)
    plt.figure()
    plt.subplot(411)
    plt.plot(data['Spd'])
    plt.xticks(xindices,xlabels)
    plt.ylabel('Total Wind Speed (kts)')
    plt.subplot(412)
    plt.plot(data['U'])
    plt.xticks(xindices, xlabels)
    plt.ylabel('U-Comp (kts)')
    plt.axhline(linewidth=1, color='k')
    plt.subplot(413)
    plt.plot(data['V'])
    plt.xticks(xindices, xlabels)
    plt.axhline(linewidth=1, color='k')
    plt.ylabel('V-Comp (kts)')
    plt.subplot(414)
    plt.plot(data['Max'])
    plt.xticks(xindices, xlabels)
    plt.ylabel('Max Gust (kts)')
    plt.xlabel('Time (MO-YR)')
    plt.suptitle(stn_id+ ' RAWS Time Series')
    plt.savefig(file+stn_id+ '_RAWS_Full_Wind_Time_Series.png')
    plt.savefig(file+stn_id+'_RAWS_Full_Wind_Time_Series.pdf')
    plt.close()

def get_xlabels(data):
    dt = datetime.date(int(data['Year'][0]),int(data['Month'][0]),int(data['Day'][0]))
    start_yr = np.min(data['Year'])
    end_yr = np.max(data['Year'])
    jan_ind = data.loc[ (data['Year']>=start_yr) & (data['Year']<=end_yr) & (data['Month']==1) & (data['Day']==1) & (data['Hour']==1)]
    indices = list(jan_ind.index.values)
    years = np.arange(start_yr,end_yr,1)
    ind1 = np.isin(jan_ind['Year'],years)
    print(ind1)


    if indices[0]!=0:
        indices = np.append(0,indices)
    if indices[-1]!=len(data['Year'])-1:
        indices = np.append(indices,len(data['Year'])-1)
    labels = []
    for i in range(len(indices)):
        dt = datetime.date(int(data['Year'][indices[i]]),int(data['Month'][indices[i]]),int(data['Day'][indices[i]]))
        labels = np.append(labels,dt.strftime("%m-%y"))

    return labels,indices

#locs = ['ATLC1','BBEC1','BKSC1','HWKC1','KELC1','KNXC1','NBRC1','OVYC1','RSAC1']

northbay_locs = ['BBEC1','OVYC1','NBRC1','NVHC1','WDAC1']
intmtn_locs = ['BKSC1','KNXC1','KELC1','ATLC1','RSAC1','HWKC1','LKRC1','BNVC1','OAAC1']
southbay_locs = ['PLEC1','ONOC1','OKSC1','LTRC1','PIBC1','LVMC1','VAQC1','LVFC1']
reno_locs = ['BNGC1','RRRC1','CISC1','SETC1','RNYC1','DOGC1','SMDC1','TADC1', 'DUCC1','HLLC1','STUC1','PKCC1','SLEC1']

for i in range(4):
    if i==0:
        locs = northbay_locs
        file = 'images/northbay/'
    if i==1:
        locs = intmtn_locs
        file = 'images/mtn/'
    if i==2:
        locs = southbay_locs
        file = 'images/southbay/'
    if i==3:
        locs = reno_locs
        file = 'images/reno/'

    for j in range(len(locs)):
        print(locs[j])
        build_pd(locs[j])

print('the end')