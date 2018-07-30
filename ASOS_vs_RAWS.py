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
    stats = linregress(df['ASOS'],df['RAWS'])
    return df,stats

def make_subplots(asos_spd,asos_gust,raws_spd,raws_gust,a_file,r_file):
    
    asos_name = ASOS_meta.loc[a_file[0:-2]]['Name']
    raws_name = r_file[-10:-6]
    
    plt.figure(figsize=(8,8))
    plt.subplot(221)
    plt.scatter(asos_spd,raws_spd)
    plt.xlabel(asos_name.strip()+' ASOS Wind Speed (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Speed (m/s)')
    
    df, stats = get_stats(asos_spd,raws_spd)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats[2],2)))
    
    plt.subplot(222)
    plt.scatter(asos_gust,raws_gust)
    plt.xlabel(asos_name.strip()+' ASOS Wind Gust (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Gust (m/s)')
    
    df, stats = get_stats(asos_gust,raws_gust)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats[2],2)))
    
    plt.subplot(223)
    plt.scatter(asos_spd,raws_gust)
    plt.xlabel(asos_name.strip()+' ASOS Wind Speed (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Gust (m/s)')
    
    df, stats = get_stats(asos_spd,raws_gust)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats[2],2)))
    
    plt.subplot(224)
    plt.scatter(asos_gust,raws_spd)
    plt.xlabel(asos_name.strip()+' ASOS Wind Gust (m/s)')
    plt.ylabel(raws_name.strip()+' RAWS Wind Speed (m/s)')
    
    df, stats = get_stats(asos_gust,raws_spd)
    fit = np.polyfit(df['ASOS'],df['RAWS'],1)
    fit_fn = np.poly1d(fit)
    plt.plot(df['ASOS'],fit_fn(df['ASOS']),'r--')
    plt.text(np.max(df['ASOS'])-5,np.max(df['RAWS'])-1,'r = '+ str("%.2f" % round(stats[2],2)))
    plt.suptitle('NE Winds (All)')
    plt.savefig('../Images/20180729/'+a_file[0:-2]+'_'+r_file[0:-6]+'.pdf')
    plt.close()
    
def fix_raws_datetime(raws_data):
    
    for i in range(len(raws_data)):
        print(str(i)+'/'+str(len(raws_data)))
        
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

def find_obs(asos_data,raws_data,quads,r_file,a_file):
    asos_dates =  asos_data.index.values
    
    #get the dates indices and data for the desired wind quadrant 
    raws_quad_data = raws_data.loc[(raws_data['Dir']>=quads[0]) & (raws_data['Dir']<quads[-1])]
    raws_dates = raws_quad_data.index.values
    mask = np.in1d(asos_dates,raws_dates)
    asos_quad_dates = asos_dates[mask]
    asos_quad_data = asos_data.loc[asos_quad_dates]
    raws_quad_data = raws_quad_data.loc[asos_quad_dates]
    
    print(len(asos_quad_data))
    print(len(raws_quad_data))
    
    return asos_quad_data
    #print(ix)
    
        
#                asos_ob = asos_data[date_str]
#                
#                #get the raws speed and gust information
#                r_spd = raws_quad_data['Spd'][idx[i]]
#                r_gus = raws_quad_data['MaxSpd'][idx[i]]
#                
#                #if an observation exists in the asos data 
#                if asos_ob.shape[0] != 0:
#                    asos_g = asos_ob['GUS'].values
#                    asos_s = asos_ob['SPD'].values
#                    
#                    #if more than one observation was recorded for the specified time,
#                    #take the first one 
#                    if len(asos_s)>1:
#                        print('hey')
#                        print(asos_s)
#                        asos_s = asos_s[0]
#                        asos_g = asos_g[0]
#                    
#                    #add the observation data to the list 
#                    asos_gust = np.append(asos_gust,asos_g) 
#                    asos_spd = np.append(asos_spd,asos_s)
#                    raws_spd = np.append(raws_spd,r_spd)
#                    raws_gust = np.append(raws_gust,r_gus)
#            
#    #convert to ms
#    asos_gust = asos_gust*to_ms
#    asos_spd = asos_spd*to_ms
#    
#    #make the subplots and find the statistical information 
#    make_subplots(asos_spd,asos_gust,raws_spd,raws_gust,a_file,r_file)
    
    
quads = [0,90]
to_ms = .44704
asos_dir = '../Data/pickles/NCEI_data/'
raws_dir = '../Data/pickles/WRCC_RAWS/'
ASOS_meta = pickle.load(open('../Data/pickles/ASOS_meta.p','rb'))
asos_files = os.listdir(asos_dir)
raws_files = os.listdir(raws_dir)

#for a_file in asos_files:
a_file = asos_files[0]
asos_data = pickle.load(open(asos_dir+a_file,'rb'))
#for r_file in raws_files:
r_file=raws_files[0]
print(a_file)
print(r_file)
if r_file!='Bangor_CBGR_QCd.p':
    raws_data = pickle.load(open(raws_dir+r_file,'rb'))
    raws_data = fix_raws_datetime(raws_data)
    temp = find_obs(asos_data,raws_data,quads,r_file,a_file)
   



        
        
        
    
           
            
            
        
