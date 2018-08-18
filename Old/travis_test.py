# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

data = pickle.load(open('../Data/pickles/NCEI_data/NCEI_3.p','rb'))
afid = 4720662 
wbanid = 23202
print(type(data['USAF'][0]))
travis_data = data.loc[(data['WBAN']==wbanid)]
travis_data2 = data.loc[(data['USAF']==str(745160)) & (data['WBAN']==99999)]
travis_data = pd.concat([travis_data,travis_data2],axis=0)
travis_data.index = pd.to_datetime(travis_data['YR--MODAHRMN'],format='%Y%m%d%H%M')

travis_data['SPD'].plot()
travis_spd = travis_data.loc[(travis_data['DIR']>=0) & (travis_data['DIR']<=90),'SPD']
travis_gust = travis_data.loc[(travis_data['DIR']>=0) & (travis_data['DIR']<=90),'GUS']

plt.figure()
plt.plot(travis_gust)

plt.figure()
plt.plot(travis_spd)

travis_data.sort_values(by=['SPD'],inplace=True,ascending=False)
travis_gust.sort_values(inplace=True,ascending=False)
travis_spd.sort_values(inplace=True,ascending=False)
writer = pd.ExcelWriter('output1.xlsx')
travis_data.head(20).to_excel(writer,'Travis AFB')
travis_gust.head(20).to_excel(writer,'Travis AFB Gust NE')
travis_spd.head(20).to_excel(writer,'Travis AFB Spd NE')
writer.save()
travis_data.sort_index(axis=0)
