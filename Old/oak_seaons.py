import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import datetime
from datetime import timezone


#read in the data and save them as pickle files
pickle_dir = '/home/disk/hot/bmac87/Documents/Dissertation/Diablo_Wind_Classification/Data/pickles/'
directory = '/home/disk/hot/bmac87/Documents/Dissertation/Diablo_Wind_Classification/Data/OAK/OAK_csv/'
filenames = os.listdir(directory)
seasons = ['Summer','Fall','Winter','Spring']
for i in range(len(filenames)):
    data = pd.read_csv(directory+filenames[i],dtype=np.float64,na_values=[' M','M','M '])
    pickle.dump(data,open(pickle_dir+filenames[i][0:-4]+'.p','wb'))


#filenames[i][0:-4]+'.p'
#pickle_file = 'sOAK_excelme_2012-2018.p'
#data = pickle.load(open(pickle_file,'rb'))

for i in range(len(filenames)):
    pickle_file = filenames[i][0:-4]+'.p'
    print(pickle_file)
    data = pickle.load(open(pickle_file,'rb'))
    if i==0:
        jan_data = data[data[' Month']==1]
        feb_data = data[data[' Month']==2]
        mar_data = data[data[' Month']==3]
        apr_data = data[data[' Month']==4]
        may_data = data[data[' Month']==5]
        jun_data = data[data[' Month']==6]
        jul_data = data[data[' Month']==7]
        aug_data = data[data[' Month']==8]
        sep_data = data[data[' Month']==9]
        oct_data = data[data[' Month']==10]
        nov_data = data[data[' Month']==11]
        dec_data = data[data[' Month']==12]
    else:
        jan_data = pd.concat([jan_data,data[data[' Month'] == 1]])
        feb_data = pd.concat([feb_data,data[data[' Month'] == 2]])
        mar_data = pd.concat([mar_data,data[data[' Month'] == 3]])
        apr_data = pd.concat([apr_data,data[data[' Month'] == 4]])
        may_data = pd.concat([may_data,data[data[' Month'] == 5]])
        jun_data = pd.concat([jun_data,data[data[' Month'] == 6]])
        jul_data = pd.concat([jul_data,data[data[' Month'] == 7]])
        aug_data = pd.concat([aug_data,data[data[' Month'] == 8]])
        sep_data = pd.concat([sep_data,data[data[' Month'] == 9]])
        oct_data = pd.concat([oct_data,data[data[' Month'] == 10]])
        nov_data = pd.concat([nov_data,data[data[' Month'] == 11]])
        dec_data = pd.concat([dec_data,data[data[' Month'] == 12]])

winter_data = pd.concat([dec_data,jan_data,feb_data])
spring_data = pd.concat([mar_data,apr_data,may_data])
summer_data = pd.concat([jun_data,jul_data,aug_data])
fall_data = pd.concat([sep_data,oct_data,nov_data])

pickle.dump(winter_data,open(pickle_dir+'Winter_OAK_soundings.p','wb'))
pickle.dump(spring_data,open(pickle_dir+'Spring_OAK_soundings.p','wb'))
pickle.dump(summer_data,open(pickle_dir+'Summer_OAK_soundings.p','wb'))
pickle.dump(fall_data,open(pickle_dir+'Fall_OAK_soundings.p','wb'))

#for i in range(len(seasons)):
#    print(seasons[i])
#
#    season_data = pickle.load(open('pickles/'+seasons[i]+'_OAK_soundings.p','rb'))
#    cols = season_data.columns
#
#    months = season_data[cols[1]].values
#    days = season_data[cols[2]].values
#    years = season_data[cols[0]].values
#    hours = season_data[cols[3]].values
#    jd = np.zeros(len(months))
#
#    for j in range(len(months)):
#
#        if int(hours[j]>23):
#            hours[j]=0
#        dt = datetime.datetime(year=int(years[j]), month=int(months[j]), day=int(days[j]), hour=int(hours[j]), tzinfo=timezone.utc)
#        jd[j] = julian.to_jd(dt, fmt='jd')
#
#    season_data['JD'] = pd.Series(jd,index=season_data.index)
#    pickle.dump(season_data, open('pickles/'+seasons[i]+'_OAK_soundings.p', 'wb'))

#print(cols)

print('end of script')