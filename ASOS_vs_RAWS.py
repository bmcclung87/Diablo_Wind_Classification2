# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt

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

def make_subplots(asos_spd,asos_gust,raws_spd,raws_gust,a_file,r_file):
    
    asos_name = ASOS_meta.loc[a_file[0:-2]]['Name']
    raws_name = r_file[-10:-6]
    
    plt.figure(figsize=(10,10))
    plt.subplot(221)
    plt.scatter(asos_spd,raws_spd,s=1)
    plt.xlabel(asos_name.strip()+' ASOS Wind Speed (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Speed (m/s)')
    
    
    df, stats1 = get_stats(asos_spd,raws_spd)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats1[2],2)))
    plt.title('N = '+str(len(df))+'/ Possible: '+str(len(asos_spd)))
    
    plt.subplot(222)
    plt.scatter(asos_gust,raws_gust,s=1)
    plt.xlabel(asos_name.strip()+' ASOS Wind Gust (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Gust (m/s)')
    
    df, stats2 = get_stats(asos_gust,raws_gust)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats2[2],2)))
    plt.title('N = '+str(len(df))+'/ Possible: '+str(len(asos_spd)))
    
    plt.subplot(223)
    plt.scatter(asos_spd,raws_gust,s=1)
    plt.xlabel(asos_name.strip()+' ASOS Wind Speed (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Gust (m/s)')
    
    df, stats3 = get_stats(asos_spd,raws_gust)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats3[2],2)))
    plt.title('N = '+str(len(df))+'/ Possible: '+str(len(asos_spd)))
    
    plt.subplot(224)
    plt.scatter(asos_gust,raws_spd,s=1)
    plt.xlabel(asos_name.strip()+' ASOS Wind Gust (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Speed (m/s)')
    
    df, stats4 = get_stats(asos_gust,raws_spd)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats4[2],2)))
    plt.title('N = '+str(len(df))+'/ Possible: '+str(len(asos_spd)))
    plt.suptitle('SE Winds (All)')
    plt.savefig('../Images/20180730/'+asos_name.strip()+'_'+raws_name.strip()+'_SE.pdf')
    plt.close()
    
    r_array = [stats1[2],stats2[2],stats3[2],stats4[2]]
    return r_array
    
def fix_raws_datetime(raws_data):
    
    for i in range(len(raws_data)):
        print(str(i))
        
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

def find_obs(asos_data,raws_data,quads,r_file,a_file,raws_num,write):
    asos_dates =  asos_data.index.values
    
    #get the dates indices and data for the desired wind quadrant 
    raws_quad_data = raws_data.loc[(raws_data['Dir']>=quads[0]) & (raws_data['Dir']<quads[-1])]
    raws_dates = raws_quad_data.index.values
    mask = np.in1d(asos_dates,raws_dates)
    asos_quad_dates = asos_dates[mask]
    asos_quad_data = asos_data.loc[asos_quad_dates]
    raws_quad_data = raws_quad_data.loc[asos_quad_dates]
    
    if len(asos_quad_data)==len(raws_quad_data):
    
        #convert to ms
        asos_gust = asos_quad_data['GUS'].values*to_ms
        asos_spd = asos_quad_data['SPD'].values*to_ms
        
        raws_gust = raws_quad_data['MaxSpd'].values
        raws_spd = raws_quad_data['Spd'].values
        
        #make the subplots and find the statistical information store the stats in
        #excel file 
        raws_name = r_file[-10:-6]
        r_array = make_subplots(asos_spd,asos_gust,raws_spd,raws_gust,a_file,r_file)
        df = pd.DataFrame.from_dict(data={raws_name:r_array},orient='index')
        return df
    
###############################################################################    
quads = [90,180]
to_ms = .44704
asos_dir = '../Data/pickles/NCEI_data/'
raws_dir = '../Data/pickles/WRCC_RAWS/'
ASOS_meta = pickle.load(open('../Data/pickles/ASOS_meta.p','rb'))
asos_files = os.listdir(asos_dir)
raws_files = os.listdir(raws_dir)

excel_file = 'Excel_Write_Outs/corr_coeff.xlsx'
write = pd.ExcelWriter(excel_file)

for a_file in asos_files:
    asos_data = pickle.load(open(asos_dir+a_file,'rb'))
    asos_name = ASOS_meta.loc[a_file[0:-2]]['Name'].strip()
    print(asos_name)
    raws_num=0
    for r_file in raws_files:
        print(r_file)
        if r_file!='Bangor_CBGR_QCd.p':
            raws_data = pickle.load(open(raws_dir+r_file,'rb'))
            if raws_num==0:
                df = find_obs(asos_data,raws_data,quads,r_file,a_file,raws_num,write)
            else: 
                df1 = find_obs(asos_data,raws_data,quads,r_file,a_file,raws_num,write)
                if df1 is not None:
                    df = pd.concat([df,df1],axis=0)
            raws_num+=1
    if df is not None:
        df.to_excel(write,asos_name)


write.save()      
#        raws_data = fix_raws_datetime(raws_data)
#        pickle.dump(raws_data,open(raws_dir+r_file,'wb'))
        
        
        
   



        
        
        
    
           
            
            
        
