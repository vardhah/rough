import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
import pandas as pd
import torch
import numpy as np
import matplotlib.pyplot as plt

HIDDEN1_UNITS=256
HIDDEN2_UNITS=128
HIDDEN3_UNITS=64
HIDDEN4_UNITS=32

class cnn():
    def __init__(self, data_file,state_size=4,action_size=3,Testing=False):
     self.testing=Testing
     self.data= pd.read_csv(data_file)
     self.data['action']=(self.data['action']+2)/4
     self.data['cos_theta_old']=(self.data['cos_theta_old']+1)/2
     self.data['cos_theta']=(self.data['cos_theta']+1)/2
     self.data['sin_theta']=(self.data['sin_theta']+1)/2
     self.data['sin_theta_old']=(self.data['sin_theta_old']+1)/2
     self.data['theta_dot']=(self.data['theta_dot']+8)/16
     self.data['theta_dot_old']=(self.data['theta_dot_old']+8)/16
     #print('data is:',self.data)
     self.model = Net(state_size, action_size).float()
     self.optim = Adam(self.model.parameters(), lr=0.03)
     self.criterion= nn.MSELoss()
     
    def train(self,epoch) :
     batch_size=32
     data_len=self.data.shape[0]
     print('Size of data:',data_len)
     loss_track=[]
     running_loss = 0.0
     x=self.data[['action',"cos_theta_old","sin_theta_old","theta_dot_old"]].values
     y=self.data[["cos_theta","sin_theta","theta_dot"]].values
     for epo in range(epoch):
       for i in range(int(data_len)):
        rand_ids = np.random.randint(0, data_len, batch_size)
        #print("ids are ",rand_ids)
        self.optim.zero_grad()
        inputs, labels = x[rand_ids],y[rand_ids]
        #print("Inputs are:",inputs)
        #print("labels are:",labels)
        inputs=torch.from_numpy(inputs)
        labels=torch.from_numpy(labels).float()
        #print("type of imput",type(inputs))
        
        # forward + backward + optimize
        outputs = self.model(inputs.float())
        loss = self.criterion(outputs, labels)
        #print('loss is:',loss)
        loss.backward()
        self.optim.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.8f' %(epo + 1, i + 1, running_loss))
            loss_track.append(running_loss)
            running_loss = 0.0
     plt.figure()       
     plt.plot(loss_track,label='loss')
     plt.grid()
     plt.title('Displacement Value on stream of image data')
     plt.legend(loc="upper left")
     plt.show()
     
    def predict(self,data):
         data[0]=(data[0]+2)/4
         data[1]=(data[1]+1)/2
         data[2]=(data[2]+1)/2
         data[3]=(data[3]+8)/16
         test_data=torch.from_numpy(data).float()
         out=self.model(test_data)     
         return out.detach().numpy()
         
        
class Net(nn.Module):
    def __init__(self, state_size, action_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(state_size, HIDDEN1_UNITS)
        self.fc2 = nn.Linear(HIDDEN1_UNITS, HIDDEN2_UNITS)
        self.fc3 = nn.Linear(HIDDEN2_UNITS, HIDDEN3_UNITS)
        self.fc4 = nn.Linear(HIDDEN3_UNITS, HIDDEN4_UNITS)
        self.fc5 = nn.Linear(HIDDEN4_UNITS, action_size)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)
        x = F.relu(x)
        x = self.fc5(x)
        return x

