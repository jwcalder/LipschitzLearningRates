#%%
#Demo of graph-based semi-supervised learning on the
#two moons dataset.
import numpy as np
import graphlearning as gl
import matplotlib.pyplot as plt

from joblib import Parallel, delayed
import multiprocessing
import utils.domains as domains
import utils.kernels as kernels

#%% Setup the experiment
def aronsson(X):
    return np.absolute(X[:,0])**(4/3) - np.absolute(X[:,1])**(4/3)

def graph_scale(n):
    return (1/n)**(1/4)

def boundary_scale(n):
    return (1/n)**(1/4)

num_verts = [2**e  for e in range(12,17)]
num_cores = 10
use_singular_weights = False
use_grid = False
num_trials = 5
parallel = False

Omega = domains.neumann_triangle()
eta = kernels.singular()


if use_grid:
    num_trials = 1
    
#%% Definition of one trial
def trial(T):
    #Draw data randomly        
    X = Omega.sample(n,use_grid)

    #Build a graph
    h = graph_scale(n)
    W = gl.eps_weight_matrix(X,h,f=eta)*2/h
    if not gl.isconnected(W):
        print("Not connected!")
 
    #
    b_delta = boundary_scale(n)
    I = Omega.boundary_mask(X, b_delta)

    #Aronsson function
    u_aronsson = aronsson(X)

    #Boundary values
    g = u_aronsson[I]

    #Lipschitz extension
    u = gl.lip_extension(W,I,g,tol=1e-7,prog=False,T=1e5,weighted=use_singular_weights)

    #Error
    err = np.max(np.absolute(u-u_aronsson))

    #Print to screen
    print('%d,%d,%f,%f'%(n,T,h,err),flush=True)

#%% main loop
print('Number of Points,Trial Number,Graph Bandwidth,Error')
for n in num_verts:
    #Number of cores for parallel processing
    if parallel:
        num_cores = min(multiprocessing.cpu_count(),num_cores)
        Parallel(n_jobs=num_cores)(delayed(trial)(T) for T in range(num_trials))
    else:
        for i in range(num_trials):
            trial(i)

   

