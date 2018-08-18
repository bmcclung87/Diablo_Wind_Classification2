import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import datetime
from datetime import timezone
from mpl_toolkits.basemap import Basemap

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso

radar_dir = '/Users/brandonmcclung/Documents/Dissertation/Radar915/LapWind/'
sites = os.listdir(radar_dir)
for i in range(len(sites)):
    if sites[i]!='.DS_Store':
        filenames = os.listdir(radar_dir+sites[i]+'/')
        file = open(radar_dir+sites[i]+'/'+filenames[0],'rb')
        lines = list(file)
        for j in range(len(lines)):
            if j==8:
                print(lines[j][0:4])
            if lines[j][0:4]=='Elev':
                print('hi')
           
        
        
    