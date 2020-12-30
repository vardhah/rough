import numpy as np
import pandas as pd
from rcf import RCTree
from pathos.multiprocessing import ProcessingPool as Pool
from functools import partial
import matplotlib.pyplot as plt
import multiprocessing
import time



tree = [None] * 100
forest=None 

def f(i,x):
	return RCTree(x) 

def dispf(i):
	return pd.Series({leaf : forest[i].disp(leaf) for leaf in forest[i].leaves}).sort_index()

#if __name__ == '__main__':
def main():
 #initialisation(number of tree)
 num_trees = 100
 global tree
 global forest
 #Data loading and reshaping
 train_data=pd.read_csv('r_train_small.csv')
 train_np_data=train_data.values[0:100]
 X=train_data.values
 print("Shape of X:",X.shape)
 print("Total data Size:",train_np_data.shape[0] ,",",train_np_data.shape[1])
 n=X.shape[0]
 d=X.shape[1]
 print("n is:",n)
 print("d is:",d)

 #Initialisation of variables used in code
 #tree = [None] * num_trees
 i=0
 forest = []
 num_processor=multiprocessing.cpu_count()
 print("number of available processor:",multiprocessing.cpu_count())
 data_list =list(range(0, num_trees))
 

 start=time.time()
 
 #creation of initial forest
 prod_f=partial(f, x=X)
 with Pool(processes=num_processor) as pool:
        tree=pool.map(prod_f, data_list)
 print(len(tree))
 for i in range(num_trees):
    forest.append(tree[i])
 #print("length of forest:",len(forest),forest)
 end=time.time()
 print("time elapsed for tree creation is:",end-start)



 

 start=time.time()
 avg_disp = pd.Series(0.0, index=np.arange(n))
 for t in forest: 
    disp1 = pd.Series({leaf : t.disp(leaf)
                       for leaf in t.leaves}).sort_index()
    avg_disp += disp1
 end=time.time()
 print("elapsed time1:",end-start) 
 peak_val=avg_disp.max()
 

 for i in range(50):
  new_testpoint=train_np_data[(100+i)]
  point_disp=0
  ttrees=0
  for tree in forest:
    tree.insert_point(new_testpoint,index=5986+i)
    ttrees+=1
  for tree in forest: 
    disp =  tree.disp(5986+i)                   
    point_disp += disp
  point_disp=point_disp/len(forest)
  disp_val.append(point_disp)
  print('-->New point disp:',point_disp)
  if point_disp<peak_val:
    for tree in forest: 
     tree.forget_point(index=5986+i)
    print("removed point")
    cnt+=1 
 else:
    print("point accepted in tree") 
    peak_val=point_disp
    cntt+=1   



if __name__ == '__main__':
	
	main()