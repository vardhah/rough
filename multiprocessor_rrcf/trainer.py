import numpy as np
import pandas as pd
from rcf import RCTree
from pathos.multiprocessing import ProcessingPool as Pool
from functools import partial
import matplotlib.pyplot as plt
import multiprocessing
import time



treek = [None] * 100

def f(i,x):
	global treek 
	treek[i]=RCTree(x)
	return RCTree(x) 

def dispf(i):
	global treek
	#print(tree)
	return pd.Series({leaf : treek[i].disp(leaf) for leaf in treek[i].leaves}).sort_index()

#if __name__ == '__main__':
def main():
 #initialisation(number of tree)
 num_trees = 100
 global tree
 #Data loading and reshaping
 train_data=pd.read_csv('r_train_small.csv')
 train_np_data=train_data.values
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
 print("length of forest:",len(forest))
 end=time.time()
 print("time elapsed for tree creation is:",end-start)


 start=time.time()
 avg_disp = pd.Series(0.0, index=np.arange(n))
 index = np.zeros(n)
 for t in forest: 
    disp = pd.Series({leaf : t.disp(leaf)
                       for leaf in t.leaves})
    avg_disp[disp.index] += disp
    np.add.at(index, disp.index.values, 1)
 avg_disp /= index
 end=time.time()
 print("elapsed time:",end-start)
 

 start=time.time()
 avg_disp1 = pd.Series(0.0, index=np.arange(n))
 for t in forest: 
    disp1 = pd.Series({leaf : t.disp(leaf)
                       for leaf in t.leaves}).sort_index()
    avg_disp1 += disp1
 end=time.time()
 print("elapsed time1:",end-start) 
 
 start=time.time()
 with Pool(processes=num_processor) as pool:
        displist=pool.map(dispf, data_list)  
 #avg_disp1 /= num_trees
 #print("Length of average disp:",len(avg_disp1))
 #print("avg disp is:",avg_disp1)
 end=time.time()
 print("elapsed time1:",end-start) 

 #plt.plot(avg_disp-avg_disp1)
 #plt.hlines(25,1,1100,'r')
 plt.grid()
 plt.show()
 print("Max disp: ",avg_disp.max())

if __name__ == '__main__':
	main()