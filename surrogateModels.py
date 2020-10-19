# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:20:36 2020

@author: HPP
"""
import gym
import pandas as pd 
import numpy as np
#from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
#from smt.surrogate_models import RBF
from CNN import cnn

csvfile = "Pendulum-v0_dummy.csv"  #file name
#data= pd.read_csv(csvfile)
neuralnet=cnn(csvfile)
neuralnet.train(1)

#data= pd.read_csv(csvfile)
#print("Shape of data:",data.shape[0])
#len_data=data.shape[0]
#x=data['action'].values
#y=data[["cos_theta","sin_theta","theta_dot"]].values
#for i in range(len_data):
#    print("input is:",x[i],"Output is:",y[i])


#sm = RBF(d0=5)
#sm.set_training_values(x, y)
#sm.train()
env = gym.make('Pendulum-v0')
env.reset() 

pend_gym= []
pend_sm=[]
obs_old=np.zeros(3,)
for _ in range(1000):
    #env.render()
    #select a random action in range of permissible action (+2 to -2)
    action=env.action_space.sample()
    action=action.astype('double')
    #print("type of action:",type(action))
    obs,reward,done,_=env.step(action) # take a random action and observe the state of system 
    y_predict = neuralnet.predict(np.concatenate((action,obs_old),axis=0))
    pend_gym.append(obs)
    pend_sm.append(y_predict)
    obs_old=obs
    
df_gym=pd.DataFrame(pend_gym,columns=['cos','sin','theta_dot'])
df_sm=pd.DataFrame(pend_sm,columns=['cos','sin','theta_dot'])
df_sm['cos']=(df_sm['cos']*2)-1
df_sm['sin']=(df_sm['sin']*2)-1
df_sm['theta_dot']=(df_sm['theta_dot']*16)-8

plt.plot(df_gym["theta_dot"],label='from gym')
plt.plot(df_sm["theta_dot"],label='from sm')
plt.grid()
plt.title('Displacement Value on stream of image data')
plt.xlabel('image_frame_number')
plt.ylabel('Disp Value')
plt.legend(loc="upper left")
plt.show()

plt.figure()
plt.plot(df_gym["cos"],label='from gym')
plt.plot(df_sm["cos"],label='from sm')
plt.grid()
plt.title('Displacement Value on stream of image data')
plt.xlabel('image_frame_number')
plt.ylabel('Disp Value')
plt.legend(loc="upper left")
plt.show()

plt.figure()
plt.plot(df_gym["sin"],label='from gym')
plt.plot(df_sm["sin"],label='from sm')
plt.grid()
plt.title('Displacement Value on stream of image data')
plt.xlabel('image_frame_number')
plt.ylabel('Disp Value')
plt.legend(loc="upper left")
plt.show()

