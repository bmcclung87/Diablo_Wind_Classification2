import numpy as np
import pandas as pd
import os
import re
import pickle
      

ASOS_dir = '../Data/NCEI_data/'
data_dir = ASOS_dir+'dat/'
stn_dir = ASOS_dir+'stn/'

filenums = []
afids = []
wbans = []
names = []
lats = []
lons = []
elevs = []

stn_files = os.listdir(stn_dir)
for s_file in stn_files:
    file_num = s_file[0:-7] #str
    fh = open(stn_dir+s_file,'r')
    loc_data = fh.readlines()
    space_start = []
    space_end = []
    
    for m in re.finditer(' ',loc_data[1]):
        space_start.append(m.start())
        space_end.append(m.end())
        
    for j in loc_data[2:]:
        afid = j[0:space_start[0]][0:6]
        wbanid = j[0:space_start[0]][7:]
        name = j[space_end[0]:space_start[1]]
        lat = float(j[space_end[3]:space_start[4]])
        lon = float(j[space_end[4]:space_start[5]])
        elev = float(j[space_end[5]:-1])
        
    filenums = np.append(filenums,file_num)
    afids = np.append(afids,afid)
    wbans = np.append(wbans,wbanid)
    names = np.append(names,name)
    lats = np.append(lats,lat)
    lons = np.append(lons,lon)
    elevs = np.append(elevs,elev)

data = {'File#': filenums,'AFID':afids,'WBAN':wbans,'Name':names,'Lat':lats,'Lon':lons,'Elev':elevs} 
df = pd.DataFrame(data=data,index=filenums)
pickle.dump(df,open('../Data/pickles/ASOS_meta.p','wb'))
write = pd.ExcelWriter('ASOS_meta.xlsx')
df.to_excel(write,'Sheet1')
write.save()


