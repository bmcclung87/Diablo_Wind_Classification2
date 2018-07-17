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
import json
import urllib
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso
TOKEN = 'b1c91e501782441d97ac056e2501b5b0'

#startdate,enddate,stid are strings
def load_hourly_asos(stid, startdate, enddate,
                     varlist=['air_temp', 'wind_speed','wind_direction','wind_gust','dew_point_temperature','relative_humidity']):
    loadvars = [var for var in varlist]
    #build the arguments for the API pull
    args = {'start': startdate,
            'end': enddate,
            'obtimezone': 'UTC',
            'vars': ','.join(loadvars),
            'stids': stid,
            'token': TOKEN
            }
    #use the url library to retrieve the data
    apiString = urllib.parse.urlencode(args)
    web_service_url = "http://api.mesowest.net/v2/stations/timeseries"
    full_url = web_service_url + '?' + apiString

    # Open the URL and convert the returned JSON into a dictionary
    web = urllib.request.urlopen(full_url)
    response = json.loads(web.read())

    # Check to make sure all desired variables were retrieved
    # for v in varlist:
    #     if v + '_set_1' not in list(response['STATION'][0]['OBSERVATIONS'].keys()):
    #         raise ValueError('"{}" not available for station {}!'.format(v, stid))

    # Get our times and measurements from the full returned dictionary
    date_time = response['STATION'][0]['OBSERVATIONS']['date_time']
    site_data = {v: response['STATION'][0]['OBSERVATIONS'][v + '_set_1'] for v in varlist}
    df = pd.DataFrame(index=date_time,data=site_data)
    df.index = pd.to_datetime(df.index)
    return df

#use mesopy to get the asos meta_data
m = Meso(token=TOKEN)
stations=m.metadata(bbox=[-123.021397,37.03180,-120.173988,38.810713])
N_sta_in = stations['SUMMARY']['NUMBER_OF_OBJECTS']

#obtain the data using the function and the urllib and mesowest api.  dump it into pickle files for each station
for n,x in enumerate(stations['STATION']):
    if x['PERIOD_OF_RECORD']['start'] is not None:
        if x['PERIOD_OF_RECORD']['start'][0:4]=='1970':
            sta_id = x['STID']
            print(sta_id)
            print(str(n)+ "/"+str(N_sta_in))
            first = x['PERIOD_OF_RECORD']['start'][0:4]+x['PERIOD_OF_RECORD']['start'][5:7]+x['PERIOD_OF_RECORD']['start'][8:10]+'0000'
            last = x['PERIOD_OF_RECORD']['end'][0:4]+x['PERIOD_OF_RECORD']['end'][5:7]+x['PERIOD_OF_RECORD']['end'][8:10]+'0000'
            if sta_id !='KMCC' and sta_id!='KMER' and sta_id!='KMHR':
                df = load_hourly_asos(sta_id,'199701010000',last)
                pickle.dump(df,open('pickles/ASOS_Mesowest_'+sta_id+'.p','wb'))


print('the end')