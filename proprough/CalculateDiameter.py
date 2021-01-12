# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:06:17 2021

@author: HPP


Normal jet ski : 950 lbs 
kawasaki Ultra jet ski : 1890 lbs
Yamaha boat engine : 25 HP@5500 rpm
  link : https://www.schockboats.com/new-models/2020-yamaha-high-thrust-25hp-25-shaft-27843708b 
         https://www.basspro.com/shop/en/solas-amita-3-blade-yamaha-25-60-hp-aluminum-propeller?hvarAID=shopping_googleproductextensions&ds_e=GOOGLE&ds_c=Shop%7CGeneric%7CAllProducts%7CHigh%7CSSCCatchAll&gclid=Cj0KCQiArvX_BRCyARIsAKsnTxM9utVkPXKtl_CnxYkKYgKNestyzFchjFm3t5vSriYGa8ITf0vO_M8aAjsyEALw_wcB&gclsrc=aw.ds
"""


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

hp=0;lbf=0;            # for unit 
thrust_required=250    # from CFD simulation of CAD design
rpm=200                # from selection of motor/engine
kt=0.25                # Domain knowledge ( need more understanding why 0.25 is common)

# fluid density 
density=1000


## No editing below 

def meter_inch(meter):
    return 39.37*meter

def hp_n(hp):
    return 745*hp

def lbf_n(lbf):
    return 4.45*lbf

def coeff_thrust(thrust,density,rpm,dia):
    rps= rpm/60 
    return thrust/(density* (rps**2)*(dia**4))
 
    
def plotdnt(thrust,density,rpm):
    d= np.arange(0.5,10,0.05, dtype='double') 
    rps=rpm/60
    kt_array= thrust/(density* np.power(rps, 2)*np.power(d, 4))
    boolArr = kt_array < 1
    kt_n=kt_array[boolArr]
    d_n=d[boolArr]  
    plt.plot(d_n,kt_n)
    selected_dia=findD(kt,thrust,density,rpm)
    plt.scatter(selected_dia,kt,color='r',label='selected point')
    plt.xlabel("Diameter")
    plt.ylabel("Thrust coefficient")
    plt.legend()
    plt.title("Thrust coefficient vs Diameter")
    
def findD(kt,thrust,density,rpm):
    rps=rpm/60
    d4=np.power( thrust/(kt*density* (rps**2)) ,0.25)
    return d4


# Thrust, vel,rpm, Diameter, density => design(CoD) 
    
if __name__ == '__main__':
   if hp==1: 
       thrust=hp_n(thrust_required)
   elif lbf==1:
       thrust=lbf_n(thrust_required)
   else:
       thrust=thrust_required
   diameter=findD(kt,thrust,density,rpm)
   plotdnt(thrust,density,rpm)
   print("Diameter is:",diameter)