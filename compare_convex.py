#%% import pkgs
import numpy as np
import graphlearning as gl
import matplotlib.pyplot as plt

import utils.domains as domains
import utils.kernels as kernels

#%% setup domains
fixed_verts = np.array([[0,0.5],[1,0.5]])

square = domains.square(fixed_verts=fixed_verts)
circle = domains.circle(r=0.5, m=[0.5,0.5], fixed_verts=fixed_verts)
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

num_verts = [2**e  for e in range(9,12)]

use_singular_weights = False
use_grid = False
num_trials = 2
parallel = False

#%% Definition of one trial
def trial(T, n):
    #Draw data randomly        
    X_0 = square.sample(n, use_grid)
    X_1, w_idx = circle.winnow(X_0)

    #Build a graph
    h = graph_scale(n)
    W_0 = gl.eps_weight_matrix(X_0,h,f=eta)*2/h
    W_1 = gl.eps_weight_matrix(X_1,h,f=eta)*2/h
    
    
    if not gl.isconnected(W_0) or not gl.isconnected(W_1):
        print("Not connected!")

    #Aronsson function
    u_aronsson_0 = aronsson(X_0)
    u_aronsson_1 = aronsson(X_1)

    #Boundary values
    I_0 = [X_0.shape[0]-2, X_0.shape[0]-1]
    I_1 = [X_1.shape[0]-2, X_1.shape[0]-1]
    
    g_0 = u_aronsson_0[I_0]
    g_1 = u_aronsson_1[I_1]

    #Lipschitz extension
    u_0 = gl.lip_extension(W_0,I_0,g_0,tol=1e-7,prog=False,T=1e5,weighted=True)
    u_1 = gl.lip_extension(W_1,I_1,g_1,tol=1e-7,prog=False,T=1e5,weighted=True)
    
    u_err =  np.linalg.norm(u_0[w_idx] - u_1, ord=np.inf)
    print('Error in solutions:',)

    #Error
  #  err = np.max(np.absolute(u-u_aronsson))

    #Print to screen
    print('%d,%d,%f'%(n,T,h),flush=True)
    
    return {'u_errs':u_err}

class logger():
    def __init__(self):
        self.logs = {}
    
    def update(self, vals):
        for key in vals:
            if key in self.logs:
                self.logs[key].append(vals[key])
            else:
                self.logs[key] = [vals[key]]


log = logger()

for n in num_verts:
    for i in range(num_trials):
        vals = trial(i, n)
        log.update(vals)