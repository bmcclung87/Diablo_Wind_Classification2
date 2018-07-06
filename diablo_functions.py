import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import metpy.calc as mpcalc

from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature

#temperature input is celcius, rh is percent
def calc_dewpt(temp,rh):
    dewpt = 243.04*(np.log(rh/100)+((17.625*temp)/(243.04+temp)))/(17.625-np.log(rh/100) - ((17.625*temp)/(243.04+temp)))
    return dewpt

#sndg_data is a data frame with the soudning information, hour is the hour in UTC
def plot_sounding(sndg_data,yr,day,mo,hr,diablo_sounding):
    plt.rcParams['figure.figsize'] = (9, 9)
    skew_evening = SkewT()
    one_sounding = sndg_data.loc[sndg_data[' Hour']==hr]
    T = convert_temperature(one_sounding[' Temp'].values,'F','C')
    rh = one_sounding[' RH'].values
    one_sounding[' Dewpt'] = calc_dewpt(T,rh)
    one_sounding = one_sounding.dropna(subset = (' Temp', ' Dewpt'),how='all').reset_index(drop=True)
    
    T = convert_temperature(one_sounding[' Temp'].values,'F','C') * units.degC
    p = one_sounding[' Pres'].values * units.hPa
    Td = one_sounding[' Dewpt'].values * units.degC
    wind_speed = one_sounding[' Spd'].values * units.knots
    wind_dir = one_sounding[' Dir '].values * units.degrees
    u, v = mpcalc.get_wind_components(wind_speed, wind_dir)
    skew_evening.plot(p,T,'r')
    skew_evening.plot(p,Td,'g')
    skew_evening.plot_barbs(p,u,v)
    skew_evening.plot_dry_adiabats()
    skew_evening.plot_moist_adiabats()
    skew_evening.plot_mixing_lines()
    skew_evening.ax.set_ylim(1000, 100)        
    plt.title('OAK Sounding: '+ str(int(mo)) + '/' + str(int(day)) + '/' + str(int(yr)) +': ' +str(int(hr))+' UTC' )
    plt.savefig('../Images/20180703/'+diablo_sounding+'/OAK_sounding_eve_'+ str(int(mo)) + '_'+str(int(day)) + '_' + str(int(yr)) +'_' +str(int(hr))+'UTC.png')
    plt.close()
    return one_sounding

#function to get the soundings for the morning and afternoon for a specific RAWS 
#site with significant diablo wind observations 
def plot_RAWS(raws_site,pickle_dir):
    all_soundings = pickle.load(open(pickle_dir+'OAK_master.p','rb'))
    diablo_days = pickle.load(open(pickle_dir+raws_site+'_diablo_day.p','rb'))
    diablo_index = diablo_days.index.values

    #for each diablo day at a given RAWS site (i.e. HWKC)
    for q in range(len(diablo_index)):
        print(q)
        
        #get the day month and year
        j=diablo_index[q]
        day = diablo_days['Day'][j]
        mo = diablo_days['Month'][j]
        yr = diablo_days['Year'][j]
        
        #get all of the sounding data for that day (morning and evening)
        sndg_data = all_soundings.loc[(all_soundings['Year']==yr) & \
                                  (all_soundings[' Month']==mo) & \
                                  (all_soundings[' Day']==day)]
      
        #get the different hours of the day
        hours = [np.min(sndg_data[' Hour']), np.max(sndg_data[' Hour'])]
        #for each sounding make the plots, concatenate all nan dropped soundings 
        for k in range(len(hours)):
            if hours[k]<=float(6) and hours[k]<=float(18):
                if q==0 or j==32362:
                    evg_soundings = plot_sounding(sndg_data, yr,day,mo,hours[k],raws_site)
                else:
                    evg_soundings = pd.concat([evg_soundings,plot_sounding(sndg_data,yr,day,mo,hours[k],raws_site)])
                
            if hours[k]<=float(23) and hours[k]>=float(7):
                if q==0:
                    mng_soundings = plot_sounding(sndg_data,yr,day,mo, hours[k],raws_site)
                else:
                    mng_soundings = pd.concat([mng_soundings,plot_sounding(sndg_data,yr,day,mo,hours[k],raws_site)])
    
    pickle.dump(evg_soundings,open('../Data/pickles/'+raws_site+'_T_Td_wd_evg_RAWS_diablo.p','wb'))
    pickle.dump(mng_soundings,open('../Data/pickles/'+raws_site+'_T_Td_wd_mng_RAWS_diablo.p','wb'))
    
#function takes in the string of the season and the directory where all of the 
#sounding data is stored and returns the data for that season    
def get_OAK_season(season,pickle_dir):
    all_soundings = pickle.load(open(pickle_dir+'OAK_master.p','rb'))
    
    if season=='Fall':
        return all_soundings.loc[(all_soundings['Month']>=9) &
                                 (all_soundings['Month']<=11)]
    
    if season=='Winter':
        return all_soundings.loc[(all_soundings['Month']>=12) &
                                 (all_soundings['Month']<=2)]
    if season=='Spring':
        return all_soundings.loc[(all_soundings['Month']>=3) &
                                 (all_soundings['Month']<=5)]
    if season=='Summer':
        return all_soundings.loc[(all_soundings['Month']>=6) &
                                 (all_soundings['Month']<=8)]
            
#function takes in a list of the RAWS sites, then returns the days in a dataframe structure
def get_diablo_wind_days(raws_sites,pickle_dir):
    for i in range(len(raws_sites)):
        if i==0:
            diablo_days = pickle.load(open(pickle_dir+raws_sites[i]+'_diablo_day.p','rb'))
        else:
            df = pickle.load(open(pickle_dir+raws_sites[i]+'_diablo_day.p','rb'))
            diablo_days = pd.concat([diablo_days,df])
            diablo_days = diablo_days.drop_duplicates()
            
    return diablo_days

#season=string,raws_sites=string_list,pickle_dir=string
def get_diablo_season(season,raws_sites,pickle_dir):
    diablo_days = get_diablo_wind_days(raws_sites,pickle_dir)
    if season=='Fall':
        return diablo_days.loc[(diablo_days['Month']==9) &\
                               (diablo_days['Month']==10) &\
                               (diablo_days['Month']==11)]
    if season=='Winter':
        return diablo_days.loc[(diablo_days['Month']==12) &\
                               (diablo_days['Month']==1) &\
                               (diablo_days['Month']==2)]
    if season=='Spring':
        return diablo_days.loc[(diablo_days['Month']==3) &\
                               (diablo_days['Month']==4) &\
                               (diablo_days['Month']==5)]
    if season=='Summer':
        return diablo_days.loc[(diablo_days['Month']==6) &\
                               (diablo_days['Month']==7) &\
                               (diablo_days['Month']==8)]


    
        
    