# -*- coding: utf-8 -*-
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
import urllib
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso
import json

#{'air_temp': 'Celsius',
# 'dew_point_temperature': 'Celsius',
# 'elevation': 'ft',
# 'fuel_moisture': 'gm',
# 'fuel_temp': 'Celsius',
# 'heat_index': 'Celsius',
# 'peak_wind_direction': 'Degrees',
# 'peak_wind_speed': 'm/s',
# 'position': 'ft',
# 'precip_accum': 'Millimeters',
# 'relative_humidity': '%',
# 'snow_interval': 'Millimeters',
# 'solar_radiation': 'W/m**2',
# 'volt': 'volts',
# 'wind_chill': 'Celsius',
# 'wind_direction': 'Degrees',
# 'wind_gust': 'm/s',
# 'wind_speed': 'm/s'}

TOKEN = 'b1c91e501782441d97ac056e2501b5b0'
args = {'start': '199801010000',
            'end': '201801010000',
            'obtimezone': 'UTC',
            'qc': 'on',
            'stids': 'RSAC1',
            'token': TOKEN
            }
#use the url library to retrieve the data
apiString = urllib.parse.urlencode(args)
web_service_url = "http://api.mesowest.net/v2/stations/timeseries"
full_url = web_service_url + '?' + apiString

# Open the URL and convert the returned JSON into a dictionary
web = urllib.request.urlopen(full_url)
response = json.loads(web.read())
date_time = response['STATION'][0]['OBSERVATIONS']['date_time']
varlist = list(response['STATION'][0]['OBSERVATIONS'].keys())
site_data = {v: response['STATION'][0]['OBSERVATIONS'][v] for v in varlist[1:-1]}
df = pd.DataFrame(index=date_time,data=site_data)
df.index = pd.to_datetime(df.index)
#df.sort_values(['wind_gust_set_1'],inplace=True,ascending=False,na_position='last')




#QC = response['STATION'][0]['QC']['wind_gust_set_1']
#indices = [i for i,x in enumerate(QC) if x is not None]
#gust_data = np.array(response['STATION'][0]['OBSERVATIONS']['wind_gust_set_1'])
#gust_data[indices]=np.nan







