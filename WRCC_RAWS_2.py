import pandas as pd
import numpy as np
import pickle
import os


filenames = os.listdir('../Data/WRCC_RAWS/')
writer = pd.ExcelWriter('output.xlsx')
writer1 = pd.ExcelWriter('NE_output.xlsx')
pickle_dir = '../Data/pickles/WRCC_RAWS/'

for n,file in enumerate(filenames):
    print(file)
    if file !='.DS_Store':
        datafile1 = '../Data/WRCC_RAWS/'+file
        data1 = pd.read_csv(datafile1,skiprows=4,delim_whitespace=True)
        
        cols = ['Date','Time','Precip','Spd','Dir','Temp','RH','MaxDir','MaxSpd']
        data1.columns = cols
        data1.sort_index(axis=0,inplace=True)
        data1.loc[data1['MaxSpd']<=0,'MaxSpd']=np.nan
        data1.loc[data1['Spd']<=0,'MaxSpd']=np.nan
        data1.loc[data1['Spd']<=0,'Spd']=np.nan
        data1.loc[data1['MaxDir']<0,'MaxSpd']=np.nan
        data1['GustRatio']=data1['MaxSpd']/data1['Spd']
        data1.loc[data1['GustRatio']>=15,'MaxSpd']=np.nan
        pickle.dump(data1,open(pickle_dir+file[0:-6]+'_QCd.p','wb'))
        data1.sort_values(by=['MaxSpd'],inplace=True,ascending=False)
        data2 = data1.loc[(data1['MaxDir']>=0) & (data1['MaxDir']<=90)]
        data1.head(20).to_excel(writer,file[0:-6])
        data2.head(20).to_excel(writer1,file[0:-6])
        #data1.loc[np.isnan(data1['MaxSpd'])].to_excel(writer,file[0:-6]+'_qc_dump')
        
writer.save()
writer1.save()


