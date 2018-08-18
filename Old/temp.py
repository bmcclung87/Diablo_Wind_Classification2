import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

files = os.listdir('../Data/pickles/NCEI_adv/')
for i in range(len(files)):
    data = pickle.load(open('../Data/pickles/NCEI_adv/'+files[i],'rb')) 
    plt.figure(i)
    data.plot(subplots=True)
    plt.savefig('../Images/20180806/'+files[i][0:-2]+'.png')
    
    
