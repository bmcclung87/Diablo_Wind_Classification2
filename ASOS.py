# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt


data_dir = '../Data/NCEI_data/dat/'
filenames = os.listdir(data_dir)
#writer = pd.ExcelWriter('ASOS_output.xlsx')
for file in filenames:
    print(file)
    if file != '6005137692938dat.txt':
        data = pd.read_csv(data_dir+file,delim_whitespace=True,\
                       na_values=['*','**','***','****','*****'],low_memory=False)
        data.index = pd.to_datetime(data['YR--MODAHRMN'],format='%Y%m%d%H%M')
        remove_cols = ['YR--MODAHRMN','CLG','SKC','L','M','H','VSB','MW','MW.1',\
                   'MW.2','MW.3','AW','AW.1','AW.2','AW.3','W','SD']
        data.drop(labels=remove_cols,axis=1)
        test_data = data.head(20)
        data.sort_index(axis=0)
        pickle.dump(data,open('../Data/pickles/NCEI_data/'+file[0:-7]+'.p','wb'))
#        data = pickle.load(open('../Data/pickles/NCEI_data/'+file[0:-7]+'.p','rb'))
        
        #plot the time series
#        data.sort_index(axis=0)
#        plt.figure()
#        f, (ax1,ax2) = plt.subplots(2,sharex=True,sharey=True)
#        ax1.plot(data['GUS'])
#        ax1.set_title('Wind Gust (mph)')
#        ax2.plot(data['SPD'])
#        ax2.set_title('Wind Speed (mph)')
#        f.savefig('../Images/20180725/qc_asosplot_'+file[0:-7]+'.png')
#        plt.close()
#        
#        #save the top 30 wind events in a excel file
#        data.sort_values(by=['SPD'],inplace=True,ascending=False)
#        data.head(30).to_excel(writer, file[0:-7]+'_spdsort')
#        data.sort_values(by=['GUS'],inplace=True,ascending=False)
#        data.head(30).to_excel(writer,file[0:-7]+'_gustsort')
        
        
#writer.save() 
        
       
    
    
#   
