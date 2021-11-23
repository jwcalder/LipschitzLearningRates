import numpy as np
import graphlearning as gl
import matplotlib.pyplot as plt
import matplotlib as mpl


plt.rc('text', usetex=True)
plt.rc('font', family='serif')


import sys,getopt
from joblib import Parallel, delayed
import multiprocessing
from utils import domains
from utils import kernels

#%% Setup the experiment
def aronsson(X):
    return np.absolute(X[:,0])**(4/3) - np.absolute(X[:,1])**(4/3)

num_verts_min = 8
num_verts_max = 14

num_verts = [2**e  for e in range(num_verts_min, num_verts_max)]
num_cores = 1
domain = 'neumann_star'
bandwidth_exp = 1.0
bandwidth_constant = 2.5
dilate_bc = False
singular_kernel = False
use_grid = False
num_trials = 10
parallel = False
verbose = False

# domain and kernel
Omega = getattr(domains, domain)()
eta = kernels.singular()

#%% figure
m = (num_verts_max - num_verts_min + 1)//2

dpi = 100
size_single = 300
width = 3 * size_single
height = 2 * size_single

fig, ax = plt.subplots(2, m, figsize = (width/dpi,height/dpi), dpi=dpi)
ax = np.ravel(ax)


#%% loop
for idx, n in enumerate(num_verts):
    #Draw data randomly        
    X = Omega.sample(n,use_grid)

    #Build a graph
    delta = (np.log(n)/n)**(1/2)
    h = bandwidth_constant * delta**bandwidth_exp
    W = gl.eps_weight_matrix(X,h,f=eta)*2/h
    if not gl.isconnected(W):
        print("Not connected!")
 
    #Boundary indices
    bdy_idx = Omega.boundary(X,0)

    #Boundary values
    bdy_val = aronsson(X[bdy_idx,:])

    #Lipschitz extension
    u = gl.lip_extension(W,bdy_idx,bdy_val,tol=1e-5,prog=verbose,T=1e5,weighted=singular_kernel)
    
    ax[idx].scatter(X[:,0],X[:,1],c=u,s=2, cmap='viridis')
    ax[idx].scatter(X[bdy_idx, 0],X[bdy_idx, 1],c='red',s=20, marker = '8')
    
    if domain == 'square':
        ax[idx].set_xlim([0,1])
        ax[idx].set_ylim([0,1])
        plt.xticks(np.arange(0, 1.2, step=0.5)) 
        plt.xticks(np.arange(0, 1.2, step=0.5)) 
        plt.yticks(np.arange(0, 1.2, step=0.5)) 
        plt.yticks(np.arange(0, 1.2, step=0.5)) 
    else:
        ax[idx].set_xlim([-1,1])
        ax[idx].set_ylim([-1,1])
        plt.xticks(np.arange(-1, 1.2, step=0.5)) 
        plt.xticks(np.arange(-1, 1.2, step=0.5)) 
        plt.yticks(np.arange(-1, 1.2, step=0.5)) 
        plt.yticks(np.arange(-1, 1.2, step=0.5)) 
    #Error
    err = np.max(np.absolute(u-aronsson(X)))

    #Print to screen
    print('%d,%f,%f'%(n,h,err),flush=True)

#%% adjust size
plt.draw()
plt.savefig('figures/' + domain + '_solution.pdf')


