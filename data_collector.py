# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:50:22 2020

@author: HPP
"""


#import numpy as np
import os
import csv
import gym
import numpy as np
import torch 

print(torch.__version__) 
data_file='Pendulum-v0_dummy.csv'
csv_file = os.path.join(data_file)
openedfile=open(csv_file, 'w')
csv_writer = csv.writer(openedfile)
csv_writer.writerow(['action','cos_theta_old','sin_theta_old','theta_dot_old','cos_theta','sin_theta','theta_dot'])
env = gym.make('Pendulum-v0')
obs_old=np.zeros(3,)
 
for i in range(200):
  env.reset()
  print('iteration number:',i)   
  for _ in range(1000):
    #env.render()
    #select a random action in range of permissible action (+2 to -2)
    action=env.action_space.sample()
    obs,reward,done,_=env.step(action) # take a random action and observe the state of system 
    # obs gives three values=> [cos(theta),sin(theta),theta_dot] range +-(1,1,8)
    csv_writer.writerow([round(action[0],3),round(obs_old[0],3),round(obs_old[1],3),round(obs_old[2],3),round(obs[0],3),round(obs[1],3),round(obs[2],3)])
    #print(" obs:",obs,"obs_old",obs_old)
    obs_old=obs

    

env.close()
openedfile.close()
