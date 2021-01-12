# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:15:15 2021

@author: HPP
"""

import pandas as pd 
import numpy as np
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt


data_prop= pd.read_csv('sim_data_set3.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])
data_prop.head()

profile = ProfileReport(data_prop)
profile.to_file(output_file="profile_data_set2.html")

data_prop.to_csv('data_prop_set3.csv',index=False)
"""
data_prop1= pd.read_csv('sim_data1.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])
data_prop2= pd.read_csv('sim_data2.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])
data_prop3= pd.read_csv('sim_data3.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])
data_prop4= pd.read_csv('sim_data4.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])
data_prop5= pd.read_csv('sim_data5.csv',names=["eff",'rpm','dia','thrust','vel_ship','cd1','cd2','cd3','cd4','cd5','cd6','cd7','cd8','cd9','cd10'])


data_prop=pd.concat([data_prop1, data_prop2,data_prop3,data_prop4,data_prop5])
data_prop.to_csv('data_prop.csv',index=False)
"""

