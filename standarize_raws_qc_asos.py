import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qc_mod import *
import os
import sidereal

#asos_names = ['Napa','Sonoma','Travis']
#for i in range(len(asos_names)):
#    asos_data = pickle.load(open('../Data/pickles/NCEI_adv/'+asos_names[i]+'.p','rb'))
#    asos_data = fix_asos_datetime(asos_data)
#    asos_data = qc_asos(asos_data)
#    pickle.dump(asos_data,open('../Data/pickles/NCEI_adv/'+asos_names[i]+'_QCd.p','wb'))
    
#fix bangor 
bangor_data = pickle.load(open('../Data/pickles/WRCC_RAWS/Bangor_CBGR_QCd.p','rb'))
bangor_data['Date'] = bangor_data['Date'].apply(str)
print(type(bangor_data['Date'][0]))

for i in range(len(bangor_data)):
    date = bangor_data['Date'][i]
    if i<69941:
        yr = date[0:2]
        yr = '19'+yr
        mo = date[2:4]
        day = date[4:6]
        hr = date[6:8]
        mns = date[8:]
    elif (i>=69941) & (i<=78571):
        yr = '2000'
        if i<=76457:
            mo = '0'+date[0:1]
            day = date[1:3]
            hr = date[3:5]
            mns = date[5:]
        else: 
            mo = date[0:2]
            day = date[2:4]
            hr = date[4:6]
            mns = date[6:]
    elif (i>=78571) & (i<=156828):
        yr = '200'+date[0:1]
        mo = date[1:3]
        day = date[3:5]
        hr = date[5:7]
        mns = date[7:]
    else:
        yr = '20'+date[0:2]
        mo = date[2:4]
        day = date[4:6]
        hr = date[6:8]
        mns = date[8:]
    
    
    date_str = yr+'-'+mo+'-'+day+'T'+hr+':'+mns
    print(date_str+ ' '+ str(i))
    d = np.datetime64(date_str,tz='US/Pacific')
    
    if i == 0:
        raws_dates = np.array(d,dtype='datetime64')
    else:
        raws_dates = np.append(raws_dates,d)
        
bangor_data.index = pd.to_datetime(raws_dates)
bangor_data.index.tz_localize('US/Pacific',ambiguous=False).tz_convert('UTC')


#date = pd.to_datetime(bangor_data['Date'],format='%y%M%d%H%m')
#bangor_data.index = date

#raws_data = pickle.load(open('../Data/pickles/WRCC_RAWS/Hawkeye_CHAW_QCd.p','rb'))
#raws_data = fix_raws_datetime(raws_data)
#raws_data.sort_index(axis=0,inplace=True)
#raws_start_date = raws_data.index.values[0]
#raws_end_date = raws_data.index.values[-1]
#
#asos_subset = asos_data[raws_start_date:raws_end_date]
#asos_ne = asos_subset.loc[((asos_subset['Dir']>0) & (asos_subset['Dir']<=90)) | (asos_subset['Dir']==360)]
#asos_ne = asos_ne[['WSpd']]
#temp = asos_ne.groupby(by=[asos_ne.index.month]).describe()
#write = pd.ExcelWriter('ASOS_NE_wind_stats_Sonoma.xlsx')
#temp.to_excel(write,'Sonoma')
#write.save()

#df = temp['WSpd','count']
#plt.figure()
#df.plot(kind='bar',color='b')
#plt.xlabel('Month')
#plt.ylabel('Frequeny')
#plt.title('Napa Frequency of NE Winds during Hawleye POR')




