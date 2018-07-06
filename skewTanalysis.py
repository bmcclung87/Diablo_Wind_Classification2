import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import metpy.calc as mpcalc
from diablo_functions import *

from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature

            
################_Main Script_##########################  
pickle_dir = '/Users/brandonmcclung/Desktop/Diablo_Wind_Classification/Data/pickles/'
#'/home/disk/hot/bmac87/Documents/Dissertation/Diablo_Wind_Classification/Data/pickles/'

seasons = ['Fall','Winter','Spring','Summer']
raws_sites = ['STUC1','VAQC1','DUCC1','HLLC1','HWKC1','KNXC1','LTRC1','OKSC1','ONOC1','SLEC1']
fall_soundings = get_OAK_season('Fall',pickle_dir)

             
             
#
##separate morning soundings from the evening soundings
#morning_soundings = fall_soundings.loc[(fall_soundings[' Hour']<=23) & \
#                                      (fall_soundings[' Hour']>=7)]
#
##get wind components
#mng_u,mng_v = mpcalc.get_wind_components(morning_soundings[' Spd'].values*units.knots, \
#                                         morning_soundings[' Dir '].values*units.degrees)
#
##store wind components in df
#morning_soundings['U'] = mng_u
#morning_soundings['V'] = mng_v
#                 
#                 
##separate evening soundings
#evening_soundings = fall_soundings.loc[(fall_soundings[' Hour']<=6) & \
#                                      (fall_soundings[' Hour']<=18)]
#
##get wind components
#evg_u,evg_v = mpcalc.get_wind_components(evening_soundings[' Spd'].values*units.knots, \
#                                         evening_soundings[' Dir '].values*units.degrees)
#
##store wind components in df
#evening_soundings['U'] = evg_u
#evening_soundings['V'] = evg_v
#
#
##height bounds for 850mb pressure levels
#ht_bound = [50,1570]
#
##get u and v component winds for fall 
#fall_u, fall_v = mpcalc.get_wind_components(fall_soundings[' Spd'].values*units.knots, \
#                                         fall_soundings[' Dir '].values*units.degrees)
#fall_soundings['U'] = fall_u
#fall_soundings['V'] = fall_v
#
##get subset of data for levels of interest
#stat_sounding = fall_soundings.loc[(fall_soundings[' Hgt']>=ht_bound[0]) & \
#                                   (fall_soundings[' Hgt']<=ht_bound[1])]
#
#
#stats_all=stat_sounding.describe(percentiles=[.05,.25,.75,.95])
#stats_morning = morning_soundings.describe(percentiles=[.05,.25,.75,.95])
#stats_evening = evening_soundings.describe(percentiles=[.05,.25,.75,.95])
#
#spd_stats = pd.concat([stats_all[' Spd'],stats_morning[' Spd'],stats_evening[' Spd']],axis=1)
#dir_stats = pd.concat([stats_all[' Dir '],stats_morning[' Dir '],stats_evening[' Dir ']],axis=1)
#rh_stats = pd.concat([stats_all[' RH'],stats_morning[' RH'],stats_evening[' RH']],axis=1)
#temp_stats = pd.concat([stats_all[' Temp'],stats_morning[' Temp'],stats_evening[' Temp']],axis=1)
#u_stats = pd.concat([stats_all['U'],stats_morning['U'],stats_evening['U']],axis=1)
#v_stats = pd.concat([stats_all['V'],stats_morning['V'],stats_evening['V']],axis=1)
#
##for i in range(len(diablo_soundings)):
##    if i==0:
##        diablo_days = pickle.load(open(pickle_dir+diablo_soundings[i]+'_diablo_day.p','rb'))
##    else:
##        df = pickle.load(open(pickle_dir+diablo_soundings[i]+'_diablo_day.p','rb'))
##        diablo_days = pd.concat([diablo_days,df])
##diablo_days = diablo_days.drop_duplicates()
##for i in range(len(diablo_days)):
##    yr = diablo_days['Year'][i]
##    mo = diablo_days['Month'][i]
##    day = diablo_days['Day'][i]
##    
##    if i=0:
##        diablo_sdg_data = all_soundings.loc[(all_soundings['Year']==yr) &\
##                                            (all_soundings[' Month']==mo) &\
##                                            (all_soundings[' Day'])]
##    else:
##        df = all_soundings.loc[(all_soundings['Year']==yr) &\
##                                            (all_soundings[' Month']==mo) &\
##                                            (all_soundings[' Day'])]
##        diablo_sdg_data = pd.concat([diablo_sdg_data,df])
##    
#    
#
#
#
#
#
##from the scatter plots, look at those RAWS station with a signifcant number of diablo obs
#
#
##for i in range(len(diablo_soundings)):
##    print(diablo_soundings[i])
##    plot_RAWS(diablo_soundings[i])
#    

    
    
    
    
    
    


    

