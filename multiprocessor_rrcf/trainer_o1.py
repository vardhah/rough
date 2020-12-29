import numpy as np
import pandas as pd
from rcf import RCTree
import matplotlib.pyplot as plt
import pickle
import dill
import time

train_data=pd.read_csv('r_train_small.csv')

print("Data loaded")
train_np_data=train_data.values


X=train_data.values


print("Shape of X:",X.shape)

print("Total data points are:",train_np_data.shape[0])
print("Total data Size:",train_np_data.shape[0] ,",",train_np_data.shape[1])
n=X.shape[0]
d=X.shape[1]
print("n is:",n)
print("d is:",d)

i=0
forest = []
# Specify forest parameters
num_trees = 100
tree_size = 64
sample_size_range = (n//tree_size,tree_size)

start=time.time()
while len(forest) < num_trees:
    # Select random subsets of points uniformly from point set
    #ixs = np.random.choice(n, size=sample_size_range,replace=False)
    # Add sampled trees to forest
    trees = RCTree(X)
    forest.append(trees)
    #print("created forest", i)
    i+=1
    #print("length of forest:",len(forest))
end=time.time()
print("Time elapsed:",end-start)


avg_disp = pd.Series(0.0, index=np.arange(n))
index = np.zeros(n)
for tree in forest: 
    disp = pd.Series({leaf : tree.disp(leaf)
                       for leaf in tree.leaves})
    avg_disp[disp.index] += disp
    np.add.at(index, disp.index.values, 1)
avg_disp /= index
print("Length of average disp:",len(avg_disp))

plt.plot(avg_disp)
#plt.hlines(25,1,1100,'r')
plt.grid()
plt.show()
print("Max disp: ",avg_disp.max())
#print('Avg disp:',avg_disp)

#for all test points:
#t_cnt=0
#num_test_points=Y.shape[0]
peak_val=avg_disp.max()

disp_val=avg_disp.tolist()
