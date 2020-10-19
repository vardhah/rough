# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:19:09 2020

@author: HPP
"""

import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
import pandas as pd
import torch
import numpy as np

HIDDEN1_UNITS=256
HIDDEN2_UNITS=128

class rnn():
    def __init__(self, data_file,state_size=4,action_size=3,Testing=False):
     self.testing=Testing
     self.data= pd.read_csv(data_file)
     self.data['theta_dot_old']=self.data['theta_dot_old']/8
     self.data['theta_dot']=self.data['theta_dot']/8
     self.model = Net(state_size, action_size).float()
     self.optim = Adam(self.model.parameters(), lr=0.03)
     self.criterion= nn.MSELoss()
     
    def train(self,epoch) :
     data_len=self.data.shape[0]
     x=self.data[['action',"cos_theta_old","sin_theta_old","theta_dot_old"]].values
     y=self.data[["cos_theta","sin_theta","theta_dot"]].values
     for epo in range(epoch):
       for i in range(data_len):  
        running_loss = 0.0
        self.optim.zero_grad()
        inputs, labels = x[i],y[i]
        inputs=torch.from_numpy(inputs)
        labels=torch.from_numpy(labels).float()
        #print("type of imput",type(inputs))
        
        # forward + backward + optimize
        outputs = self.model(inputs.float())
        loss = self.criterion(outputs, labels)
        loss.backward()
        self.optim.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epo + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
     
    def predict(self,data):
         test_data=torch.from_numpy(data).float()
         out=self.model(test_data)     
         return out.detach().numpy()
         
        
class Net(nn.Module):
    def __init__(self, state_size, action_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(state_size, HIDDEN1_UNITS)
        self.fc2 = nn.Linear(HIDDEN1_UNITS, HIDDEN2_UNITS)
        self.fc3 = nn.Linear(HIDDEN2_UNITS, action_size)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x

