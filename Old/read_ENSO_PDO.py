import os
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt 

files = os.listdir('../Data/ENSO/')
print(files)



for i in range(len(files)):
    d = []
    en = []
    fh = open('../Data/ENSO/'+files[i],'r')
    head = files[i][16:-4]
    for lines in fh:
        lines = lines[0:-2]
        lines = lines.split(' ')
        lines = list(filter(None, lines))
        month=1  
        print(lines)
        for j in range(len(lines)-1):
            if j==0:
                yr = lines[j]
            else:
                if (yr!='2018'):
                    en = np.append(en,np.float64(lines[j]))
                    d = np.append(d,yr+str(month).zfill(2))
                else:
                    if month<=7:
                        en = np.append(en,np.float64(lines[j]))
                        d = np.append(d,yr+str(month).zfill(2))
            month+=1
                
    
    if i==0:
        data = {'Date':d,head:en}
        df = pd.DataFrame(data=data)
        df.index = pd.to_datetime(d,format = '%Y%m')
    else:
        data = {head:en}
        df = pd.concat([df,pd.DataFrame(data=data,index=pd.to_datetime(d,format='%Y%m'))],axis=1)
pickle.dump(df,open('../Data/pickles/ENSO_PDO/ENSO_df.p','wb'))
plt.figure(12)
df.plot(subplots=True,)
plt.savefig('../Images/20180806/ENSO_data.pdf')

    

##read PDO data (data is not formatted the same)
#fh = open('../Data/ENSO/'+files[0],'r')
#dates = []
#pdo = []
#for lines in fh:
#    print(lines)
#    lines=lines[0:-2]
#    print(lines)
#    temp = lines.split(',')
#    dates = np.append(dates,temp[0])
#    pdo = np.append(pdo,np.float(temp[1]))
#data = {'Date':dates, 'PDO':pdo}
#df = pd.DataFrame(data=data)
#df.index = pd.to_datetime(dates,format='%Y%m')


#plt.figure(1)
#df.plot()
#plt.savefig('../Images/PDO_plot.png')
#pickle.dump(df,open('../Data/pickles/ENSO_PDO/PDO.p','wb'))
