import numpy as np
import pandas as pd
import pickle 
import os
import matplotlib.pyplot as plt
import xlrd
from mpl_toolkits.basemap import Basemap

excel_file = 'Excel_Write_Outs/corr_coeff_NE.xlsx'
xls = xlrd.open_workbook(excel_file, on_demand=True)
sheet_names = xls.sheet_names()
ASOS_meta = pickle.load(open('../Data/pickles/ASOS_meta.p','rb'))
ASOS_names = ASOS_meta['Name']
for n,name in enumerate(ASOS_names):
    ASOS_meta['Name'][n] = name.strip()

df2 = ASOS_meta
df2['r'] = np.ones_like(ASOS_names)*-9999


for i, name in enumerate(sheet_names):
    df = pd.read_excel(excel_file,sheet_name=name)
    r = df.max().max()
    idx = np.where(df2['Name']==name)[0][0]
    df2['r'][idx] = r

lon = df2['Lon'].values
lat = df2['Lat'].values
r = df2['r'].values

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=-119,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')
m.scatter(lon, lat, latlon=True,c=r,cmap='winter_r', edgecolors='k',alpha=1)
plt.colorbar(label='Corr Coef')
plt.clim(0, 1)
plt.title('NE Winds (all speeds) Correlation Coefficient, max = '+str("%.2f" % round(df2['r'].max(),2)))
plt.savefig('../Images/20180730/NE_winds_corr_map.pdf')




    
