# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

from scipy.stats import linregress

def get_stats(asos,raws):
    #remove nans
    d = {'ASOS':asos, 'RAWS':raws}
    df = pd.DataFrame(data=d,index=np.arange(len(asos)))
    df.dropna(axis=0,how='any',inplace=True)
    #print(len(df))
    if len(df)!=0:
        stats = linregress(df['ASOS'],df['RAWS'])
    else:
        stats = np.ones(5)*-9999
        df['ASOS'] = np.ones(99)*-9999
        df['RAWS'] = np.ones(99)*-9999
    return df,stats

def fix_raws_datetime(raws_data):
    
    for i in range(len(raws_data)):
        #for each date that is applicable in the RAWS data 
        #convert the date to the 
        #appropriate time format for the asos observations
        mo,day,yr = raws_data['Date'].values[i].split('/')
        hr,mns = raws_data['Time'].values[i].split(':')
        if int(mo)<=9:
            mo='0'+mo   
        if int(day)<=9:
            day ='0'+day   
        if int(hr)<=9:
            hr='0'+hr   
        if (int(yr)>=0 and int(yr)<=18):
            yr='20'+yr   
        else:
            yr='19'+yr
        
        #build the appropriate datetime string for searching the asos data 
        date_str = yr+'-'+mo+'-'+day+'T'+hr+':'+mns
        d = np.datetime64(date_str)
        if i == 0:
            raws_dates = np.array(d,dtype='datetime64')
        else:
            raws_dates = np.append(raws_dates,d)
            
    raws_data.index = raws_dates
    return raws_data

def fix_asos_datetime(asos_data):
    date = asos_data['Date'].values
    time = asos_data['HrMn'].values
    for i in range(len(asos_data)):
        if i%1000==0:
            print(str(i)+'/'+str(len(asos_data)))
        if len(str(time[i]))< 3:
            str_time = '00' + str(time[i])
        elif len(str(time[i]))<4:
            str_time = '0' + str(time[i])
        else:
            str_time = str(time[i])
            
        if i==0:
            dt = np.array(str(date[i])+str_time)
        else:
            dt = np.append(dt,str(date[i])+str_time)
    asos_data['str_date']=dt
    asos_data.index = pd.to_datetime(asos_data['str_date'],format='%Y%m%d%H%M').dt.round('60min')
    asos_data.sort_index(axis=0,inplace=True)
    return asos_data

data_dir = '../Data/Advanced_NCEI_Data/dat/'
data_files = os.listdir(data_dir)
print(data_files)

for i in range(len(data_files)):
    asos_data  = pd.read_csv(data_dir+data_files[i],delim_whitespace=True,low_memory=False)
    asos_data = fix_asos_datetime(asos_data)
    pickle.dump(asos_data,open('../Data/pickles/NCEI_adv/'+data_files[i][0:-7]+'.p','wb'))

#sname = 'Hawkeye_CHAW'
#raws_max = pd.read_excel('Excel_Write_Outs/NE_RAWS_max20.xlsx',sheet_name = sname)
#raws_max = fix_raws_datetime(raws_max)
#raws_max_dates = raws_max['Date'].drop_duplicates()
#raws_max_dates = raws_max_dates.index.date
#
#asos_data = pickle.load(open('../Data/pickles/NCEI_adv/8316857698839.p','rb'))
#asos_data.replace(999,np.nan,inplace=True)
#asos_data.replace('999',np.nan,inplace=True)
#asos_data.replace(999.9,np.nan,inplace=True)
#asos_dates = asos_data.index.date
#asos_data['DateTime_date'] = asos_dates
#temp_asos = asos_data.head(30)
#
#raws_ob_data = pickle.load(open('../Data/pickles/WRCC_RAWS/Hawkeye_CHAW_QCd.p','rb'))
#raws_ob_dates = raws_ob_data.index.date
#raws_ob_data['DateTime_date'] = raws_ob_dates
#temp_raws = raws_ob_data.head(30)
#
#for i in range(len(raws_max_dates)):
#    if i==0:
#        asos_max_obs = asos_data.loc[(asos_data['DateTime_date']==raws_max_dates[i])]
#        raws_max_obs = raws_ob_data.loc[(raws_ob_data['DateTime_date']==raws_max_dates[i])]
#    else:
#        asos_max_obs = pd.concat([asos_max_obs,\
#                                  asos_data.loc[(asos_data['DateTime_date']==raws_max_dates[i])]])
#        raws_max_obs = pd.concat([raws_max_obs,\
#                                  raws_ob_data.loc[(raws_ob_data['DateTime_date']==raws_max_dates[i])]])
#    
#mask = np.in1d(asos_max_obs.index.values,raws_max_obs.index.values)
#asos_max_obtimes = asos_max_obs.index[mask]
#asos_max_obs = asos_max_obs.loc[asos_max_obtimes].drop_duplicates(subset=['str_date'])
#raws_max_obs = raws_max_obs.loc[asos_max_obs.index]
#
#
#df,stats = get_stats(asos_max_obs['WSpd'].values,raws_max_obs['Spd'].values)
#slope, intercept, r_value, p_value, std_err = stats[0],stats[1],stats[2],stats[3],stats[4]
#plt.figure()
#plt.scatter(asos_max_obs['WSpd'].values,raws_max_obs['Spd'].values)
#plt.plot(asos_max_obs['WSpd'].values,intercept+slope*asos_max_obs['WSpd'].values,'r')
#plt.xlabel('ASOS Wind Speed (m/s)')
#plt.ylabel('RAWS Wind Speed (m/s)')
#plt.title('Hawkeye RAWS vs Napa Co Airport ASOS')





