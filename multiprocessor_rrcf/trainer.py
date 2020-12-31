import numpy as np
import pandas as pd
from rcf import RCTree
from pathos.multiprocessing import ProcessingPool as Pool
from functools import partial
import matplotlib.pyplot as plt
import multiprocessing
import time



def f(i,x):
	return RCTree(x) 

def dispf(trree,index):
	return trree.disp(index)

def insertf(trree,z,index):
   trree.insert_point(z,index)
   return trree

def forgetf(trree,index):
   trree.forget_point(index)
   return trree

#if __name__ == '__main__':
def main():
 #initialisation(number of tree)
 num_trees = 100

 #Data loading and reshaping
 train_data=pd.read_csv('r_train_data.csv')
 train_np_data=train_data.values
 X=train_data.values[0:500]
 print("Shape of X:",X.shape)
 print("Total data Size:",train_np_data.shape[0] ,",",train_np_data.shape[1])
 n=X.shape[0]
 d=X.shape[1]
 print("n is:",n)
 print("d is:",d)


 i=0;cnt=0;cntt=0
 num_processor=multiprocessing.cpu_count()
 print("number of available processor:",multiprocessing.cpu_count())
 data_list =list(range(0, num_trees))
 
#strating reduction process
 
 
 #creation of initial forest(mpu)
 prod_f=partial(f, x=X)
 with Pool(processes=num_processor) as pool:
        trees=pool.map(prod_f, data_list)
 


#Calculating disp value for each leaf in tree(1 cpu) # need to write mpu
 avg_disp = pd.Series(0.0, index=np.arange(n))
 for t in trees: 
    disp = pd.Series({leaf : t.disp(leaf)
                       for leaf in t.leaves}).sort_index()
    avg_disp += disp
 avg_disp /= num_trees
 peak_val=avg_disp.max()
 print("peak disp value is:",peak_val)

 

 for i in range(10):
  new_testpoint=train_np_data[(500+i)]
  ind=500+i
  point_disp=0
  ttrees=0
  
  #inserting a point in a tree(mpu)
  insert_f=partial(insertf, z=new_testpoint,index=ind)
  with Pool(processes=num_processor) as pool:
        trees=pool.map(insert_f, trees)

  #print("trees are:",trees)

  #Find disp of each point (mpu)
  disp_f=partial(dispf,index=ind)
  with Pool(processes=num_processor) as pool:
        disps=pool.map(disp_f, trees)
  point_disp=sum(disps)/num_trees
  print("point disp is:",point_disp)
  
#Forget / Accept points(mpu)
  if point_disp<peak_val:                               #condition for deleting the point from tree
    forget_f=partial(forgetf,index=ind)
    with Pool(processes=num_processor) as pool:
        trees=pool.map(forget_f, trees)
    print("removed point")
    cntt+=1
 else:                                                 # Else accept the point
    print("point accepted in tree") 
    peak_val=point_disp  
    cnt+=1
 print("Removed points:",cnt)  
 print("Accepted points:",cntt)
 
if __name__ == '__main__':
  start=time.time()
  main()
  end=time.time()
  print("time elapsed for tree creation is:",end-start)