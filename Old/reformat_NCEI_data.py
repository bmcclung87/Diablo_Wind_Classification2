import os
import numpy as np
import pandas as pd
import pickle
from datetime import datetime 
#********************************NOTES*****************************************
#01-06   USAF = AIR FORCE CATALOG STATION NUMBER   
#08-12   WBAN = NCDC WBAN NUMBER
#14-25   YR--MODAHRMN = YEAR-MONTH-DAY-HOUR-MINUTE IN GREENWICH MEAN TIME (GMT)
#27-29   DIR = WIND DIRECTION IN COMPASS DEGREES, 990 = VARIABLE, REPORTED AS
#        '***' WHEN AIR IS CALM (SPD WILL THEN BE 000)
#31-37   SPD & GUS = WIND SPEED & GUST IN MILES PER HOUR  
#84-92   TEMP & DEWP = TEMPERATURE & DEW POINT IN FAHRENHEIT 
#94-99   SLP = SEA LEVEL PRESSURE IN MILLIBARS TO NEAREST TENTH 
#107-112   STP = STATION PRESSURE IN MILLIBARS TO NEAREST TENTH
#114-116  MAX = MAXIMUM TEMPERATURE IN FAHRENHEIT (TIME PERIOD VARIES)
#118-120 MIN = MINIMUM TEMPERATURE IN FAHRENHEIT (TIME PERIOD VARIES)
#122-126 PCP01 = 1-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS --
#        THAT IS, THE PRECIP FOR THE PRECEDING 1 HOUR PERIOD
#128-132 PCP06 = 6-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS --
#        THAT IS, THE PRECIP FOR THE PRECEDING 6 HOUR PERIOD
#134-138 PCP24 = 24-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS
#        THAT IS, THE PRECIP FOR THE PRECEDING 24 HOUR PERIOD
#140-144 PCPXX = LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS, FOR 
#        A PERIOD OTHER THAN 1, 6, OR 24 HOURS (USUALLY FOR 12 HOUR PERIOD
#        FOR STATIONS OUTSIDE THE U.S., AND FOR 3 HOUR PERIOD FOR THE U.S.)
#        T = TRACE FOR ANY PRECIP FIELD
#146-147 SD = SNOW DEPTH IN INCHES  
#NO QC FLAGS
#******************************************************************************

#load the text files into a data frame and save as pickle files for easy loading
#ncei_dir = '../Data/NCEI_data/dat/'
#filenames = os.listdir(ncei_dir)
#for i in range(len(filenames)):
#    ncei_data = pd.read_csv(ncei_dir+filenames[i],delim_whitespace=True,low_memory=False, na_values = ['*','**','***','****','*****','******'])
#    pickle.dump(ncei_data,open('../Data/pickles/NCEI_data/NCEI_'+str(i)+'.p','wb'))

pickle_dir = '../Data/pickles/NCEI_data/NCEI_'
for i in range(6):
    print(i)
    
test_NCEI = pickle.load(open('../Data/pickles/NCEI_data/NCEI_0.p','rb'))
remove_cols = ['CLG', 'SKC', 'L',
       'M', 'H', 'VSB', 'MW', 'MW.1', 'MW.2', 'MW.3', 'AW', 'AW.1', 'AW.2',
       'AW.3', 'W']
test_NCEI = test_NCEI.drop(labels=remove_cols,axis=1)
test_NCEI = test_NCEI[0:1000]
dates = test_NCEI['YR--MODAHRMN']
dates = dates.apply(str)
dates = pd.to_datetime(dates,format='%Y%m%d%H%M',utc=True)
test_NCEI['YR--MODAHRMN'] = dates
test_NCEI.rename(columns={'YR--MODAHRMN':'Date'},inplace=True)

#test_dates = dates.values
#for i in range(len(test_dates)):
#    print(i)
#    dates[i] = pd.to_datetime(str(test_dates[i]),format='%Y%m%d%H%M',utc=True)

    
    

    