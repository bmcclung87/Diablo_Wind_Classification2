import pickle
import numpy as np
import pandas as pd

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
    time = [str(item).zfill(4) for item in time]
    dt = [str(d)+t for d,t in zip(date, time)]
    asos_data['str_date']=dt
    asos_data.index = pd.to_datetime(asos_data['str_date'],format='%Y%m%d%H%M').dt.round('60min')
    asos_data.sort_index(axis=0,inplace=True)
    return asos_data

def qc_asos(asos_data):
#    
#    0: Passed gross limits check
#	1: Passed all quality control checks
#	2: Suspect
#	3: Erroneous
#	4: Passed gross limits check , data originate from an NCDC data source
#	5: Passed all quality control checks, data originate from an NCDC data source
#	6: Suspect, data originate from an NCDC data source
#	7: Erroneous, data originate from an NCDC data source
#	9: Passed gross limits check if element is present
    asos_data = asos_data.replace(999,np.nan)
    asos_data = asos_data.replace(999.9,np.nan)
    asos_data.dropna(axis=0,how='any',subset=['Dir'],inplace=True)
    print(type(asos_data['Q'][0]))
    asos_data = asos_data.loc[(asos_data['Q']==1)]
    return asos_data

asos_data = pickle.load(open('../Data/pickles/NCEI_adv/4411667698840.p','rb'))
asos_temp = asos_data.head(20)
asos_data = fix_asos_datetime(asos_data)
asos_data = qc_asos(asos_data)

raws_data = pickle.load(open('../Data/pickles/WRCC_RAWS/Hawkeye_CHAW_QCd.p','rb'))
raws_data = fix_raws_datetime(raws_data)
raws_data.sort_index(axis=0,inplace=True)
raws_start_date = raws_data.index.values[0]
raws_end_date = raws_data.index.values[-1]
raws_ne = raws_data.loc[((raws_data['Dir']>0) & (raws_data['Dir']<=90)) | (raws_data['Dir']==360)]
raws_ne.sort_values(by=['Spd'],ascending=False,inplace=True)
raws_50 = raws_ne[0:50]

asos_subset = asos_data[raws_start_date:raws_end_date]
asos_ne = asos_subset.loc[((asos_subset['Dir']>0) & (asos_subset['Dir']<=90)) | (asos_subset['Dir']==360)]
asos_ne = asos_ne[['Dir','WSpd']]
asos_ne.sort_values(by=['WSpd'],inplace=True,ascending=False)
asos_ne_stats = asos_ne.groupby(by=[asos_ne.index.month]).describe()
asos_50 = asos_ne[0:50]

dates = np.in1d(asos_50.index.values,raws_50.index.values)



