import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle

def wind_qc(spd_data):
    wi_threshold = 4 #mps
    calm_threshold = 1.54333 #mps
    drop_ob = False
    spd_data[np.where(spd_data>=40)]=np.nan
    for i in range(12,len(data)-14):
        d_2 = []
        wi = []
        for j in range(1,12): 
            if j>1:
                wi.append(np.abs(spd_data[(i-j)]-spd_data[i]))
                wi.append(np.abs(spd_data[(i+j)]-spd_data[i]))
        
            if j<=11:
                d_2.append(np.abs(spd_data[(i-j)]-spd_data[(i-j)+2]))
                d_2.append(np.abs(spd_data[(i+j)]-spd_data[(i+j)+2]))
        
        dmax_2 = np.nanmax(d_2)
        if np.sum(dmax_2<wi)>0:
            if np.sum(np.array(wi)>=wi_threshold)>0:
                wi1 = np.abs(spd_data[i]-spd_data[i-1])
                wi2 = np.abs(spd_data[i]-spd_data[i+1])
                if spd_data[i]>=calm_threshold:
                    if wi1>3.08667 and wi2>3.08667:
                        drop_ob=True
                if spd_data[i]<calm_threshold:
                    if wi1>4.11556 and wi2>4.11556:
                        drop_ob=True
        if drop_ob==True:
            spd_data[i]=np.nan
            drop_ob = False
    
    return spd_data
###############################################################################

RAWS_dir = '../Data/WRCC_RAWS/'
pickle_dir = '../Data/pickles/WRCC_RAWS/'
ids = ['CSEC','CKNO','CLIN','CKON','CSRS','CHAW','CBOO','CBGR','CPIK','CSTO']
files = os.listdir(RAWS_dir)
for i in files:
    print(i)
    if i!='.DS_Store':
        data = pd.read_csv(RAWS_dir+i,skiprows=4,delim_whitespace=True,na_values=-9999)
        cols = ['Date','Time','Precip','Spd','Dir','Temp','RH','MaxDir','MaxSpd']
        data.columns = cols
        data.dropna(subset = ['Spd','MaxSpd'],how='all',axis=0,inplace=True)
        pickle.dump(data,open(pickle_dir+i[-9:-4]+'_RAWS.p','wb'))
        
        print(data.shape)
        plt.figure(i)
        plt.plot(data['MaxSpd'])
        plt.title(i)
        spd_data = data['MaxSpd'].values
        qc_data = wind_qc(spd_data)
        plt.figure(i*2)
        plt.plot(qc_data)
        plt.title(i)
    
    
    
    
    