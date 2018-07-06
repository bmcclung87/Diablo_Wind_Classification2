import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import julian
import datetime
from datetime import timezone

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from scipy.constants import convert_temperature
from MesoPy import Meso

key = 'b1c91e501782441d97ac056e2501b5b0'
m = Meso(token=key)
stations = m.metadata(stid='BBEC1')
print(stations)

