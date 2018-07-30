import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

names = ['CHAW','CSRS','CKNO','CSTO','CBGR','CPIK','CLIN','CKON','CBOO','CSEC']
file = '../Data/RAWS_monthly.xlsx'

for n,str in enumerate(names):
    data = pd.read_excel(file,sheet_name=str)
    maxGust = data['MaxGust']
    plt.figure(2*n)
    plt.plot(maxGust)
    plt.title(str+' Monthly Max Gust')
    plt.ylabel('Max Gust (mph)')
    plt.xlabel('Months since ' + data['Date'][0])
    plt.ylim([0,100])
    plt.xlim([0,len(maxGust)])
    plt.savefig('../Images/20180717/'+str+'_preQC.png')
    
    maxGust_QCd = maxGust.loc[(maxGust<100) | (maxGust>0)] #mph
    qcd_indices = maxGust_QCd.index.values
    maxGust_QCd_removed = maxGust.loc[(maxGust>=100) | (maxGust<=0)]
    removed_indices = maxGust_QCd_removed.index.values
    
    print(type(removed_indices))
    for i in range(len(qcd_indices)):
        if ~np.isin(qcd_indices[i],removed_indices):
            if i==0:
                diff = np.abs(maxGust_QCd[qcd_indices[i]]-maxGust[qcd_indices[i]+1])
                if diff>50:
                    removed_indices = np.append(removed_indices,qcd_indices[i])
            elif i==len(qcd_indices):
                diff = np.abs(maxGust[qcd_indices[i]-1]-maxGust_QCd[qcd_indices[i]])
                if diff>50:
                    removed_indices = np.append(removed_indices,qcd_indices[i])
            else:
                w1 = maxGust[qcd_indices[i]-1]
                w2 = maxGust_QCd[qcd_indices[i]]
                if (qcd_indices[i]+1) < len(maxGust):
                    w3 = maxGust[qcd_indices[i]+1]
                else:
                    w3=0
                if w1<=w2:
                    if (w2-w1)>=50:
                        removed_indices = np.append(removed_indices,qcd_indices[i])
                else:
                    if (w1-w2)>=50:
                        removed_indices = np.append(removed_indices,qcd_indices[i])
                if w2<=w3:
                    if (w3-w2)>=50:
                        removed_indices = np.append(removed_indices,qcd_indices[i])
                else:
                    if (w2-w3)>=50:
                        removed_indices = np.append(removed_indices,qcd_indices[i])
                    
    if str=='CSRS' or str=='CPIK' or str=='CBOO':
        if str=='CPIK':
            qc_threshold=100
        else:
            qc_threshold=25
        removed_indices = np.unique(np.append(removed_indices,np.arange(0,qc_threshold)))
    for i in range(len(removed_indices)):
        print(i)
        maxGust[removed_indices[i]]=np.nan
    
    pickle.dump(data['Date'][removed_indices],open('../Data/pickles/WRCC_RAWS/'+str+'qcd_mo.p','wb'))
    
    plt.figure(2*n+1)
    plt.plot(maxGust)
    plt.title(str+' Monthly Max Gust w/ QC')
    plt.ylabel('Max Gust (mph)')
    plt.xlabel('Months since ' + data['Date'][0])
    plt.ylim([0,100])
    plt.xlim([0,len(maxGust)])
    plt.savefig('../Images/20180717/'+str+'_postQC.png')
    
    
    
    
    