#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:25:43 2018

@author: brandonmcclung
"""

import pandas as pd
import numpy as np
import pickle
import os






#'../Data/AF_data/fireweather_2017.csv'
#af_data = pd.read_csv('../Data/AF_data/fireweather_2017.csv')
#pickle.dump(af_data,open('../Data/AF_data/asos_test.p','wb'))
#num_rec = len(af_data)
#num_rec_per_file = 1e6
#num_files = int(np.ceil(num_rec/num_rec_per_file))
#for i in range(num_files-1):
#    print([int(i*1e6), int((i+1)*1e6)])
#    pickle.dump(af_data[int(i*num_rec_per_file):int((i+1)*num_rec_per_file)],open('../Data/AF_data/asos_test_'+str(i)+'.p','wb'))
#    
#    if i+1 == (num_files-1):
#        print('last of file')
#        print(len(af_data)-(i+1)*1e6)
#        pickle.dump(af_data[int((i+1)*num_rec_per_file):-1],open('../Data/AF_data/asos_test_'+str(i+1)+'.p','wb'))
#test_af = pickle.load(open('../Data/AF_data/asos_test_44.p','rb'))