#%% import pkgs
import numpy as np
import graphlearning as gl
import matplotlib.pyplot as plt

import utils.domains as domains
import utils.kernels as kernels

#%% setup domains
fixed_verts = np.array([[0,0.5],[1,0.5]])

domain= domains.square(fixed_verts=fixed_verts)

eta = kernels.singular()

#%%
def plot_pts(X, b_idx=None):
    plt.scatter(X[:,0],X[:,1])
    
    if not b_idx is None:
        plt.scatter(X[b_idx,0], X[b_idx,1], color='r')
    
def plt_sol(X, u):
    pass

#%% setup experiment
def aronsson(X):
    return np.absolute(X[:,0])**(4/3) - np.absolute(X[:,1])**(4/3)

# scales
def graph_scale(n):
    return (1/n)**(1/4)

def boundary_scale(n):
    return (1/n)**(1/4)

nums_verts = [2**e  for e in range(9,13)]

use_singular_weights = False
use_grid = False
num_trials = 2
parallel = False

#%% Definition of one trial
def trial(T, n):
    #Draw data randomly        
    X = domain.sample(n, use_grid)

    #Build a graph
    h = graph_scale(n)
    W = gl.eps_weight_matrix(X,h,f=eta)*2/h
    
    
    if not gl.isconnected(W):
        print("Not connected!")

    #Aronsson function
    u_aronsson = aronsson(X)

    #Boundary values
    I = [X.shape[0]-2, X.shape[0]-1]
    
    g = u_aronsson[I]

    #Lipschitz extension
    u = gl.lip_extension(W,I,g,tol=1e-7,prog=False,T=1e5,weighted=True)

    #Error
    err = np.max(np.absolute(u-u_aronsson))

    #Print to screen
    print('%d,%d,%f'%(n,T,h),flush=True)
    
    return {'errs':err}

class logger():
    def __init__(self, num_trials = 0):
        self.logs = {}
        self.num_trials = num_trials
    
    def update(self, vals, trial):
        for key in vals:
            if not key in self.logs:
                self.logs[key] = np.zeros((self.num_trials,1))
            else:
                self.logs[key] = np.hstack((self.logs[key], np.zeros((self.num_trials,0))))
                
            self.logs[key][trial,-1] = vals[key]


log = logger(num_trials = num_trials)

for num_verts in nums_verts:
    for t in range(num_trials):
        vals = trial(t, num_verts)
        log.update(vals, t)
        

