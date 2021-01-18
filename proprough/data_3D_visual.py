# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:49:08 2021

@author: HPP
"""

import pandas as pd 
import numpy as np
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt


data_prop= pd.read_csv('sim_data_set1.csv',names=['Z','rho','N','D','Dhub','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10','kt','eff'])
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import colors


fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(121, projection='3d')
sc = ax.scatter(data_prop["thrust"], data_prop['vel_ship'], data_prop['N'],
                cmap='gnuplot2')
plt.xlabel('thrust')
plt.ylabel('Speed(metre/sec)')
plt.show()