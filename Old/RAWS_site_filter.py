import pandas as pd
import urllib
import json
import numpy as np

RAWS_sites = pd.read_excel('/Users/brandonmcclung/Documents/Dissertation/fire_list.xlsx',sheet_name='RAWS_Sites')
RAWS_sites.dropna(inplace=True,how='all')
RAWS_sites['lat'] = pd.Series(np.random.randn(len(RAWS_sites)),index=RAWS_sites.index)
RAWS_sites['lon'] = pd.Series(np.random.randn(len(RAWS_sites)),index=RAWS_sites.index)
RAWS_sites['elev'] = pd.Series(np.random.randn(len(RAWS_sites)),index=RAWS_sites.index)
for n,x in enumerate(RAWS_sites['id']):
    print(x)
    
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
    RAWS_sites['lat'][n]=response['STATION'][0]['LATITUDE']
    RAWS_sites['lon'][n]=response['STATION'][0]['LONGITUDE']
    RAWS_sites['elev'][n] = response['STATION'][0]['ELEVATION']
    