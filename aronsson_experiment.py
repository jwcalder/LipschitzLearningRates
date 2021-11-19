import numpy as np
import graphlearning as gl
import matplotlib.pyplot as plt

import sys,getopt
from joblib import Parallel, delayed
import multiprocessing
from utils import domains
from utils import kernels

#%% Setup the experiment
def aronsson(X):
    return np.absolute(X[:,0])**(4/3) - np.absolute(X[:,1])**(4/3)

# scales
def graph_scale(n):
    return (1/n)**(1/4)

def boundary_scale(n):
    return (1/n)**(1/4)

#Print help
def print_help():
    
    print('========================================================')
    print('Convergence rate experiments for Lipschitz learning ')
    print('========================================================')
    print('                                                        ')
    print('Options:')
    print('   -h (--help): Print help.') 
    print('   -D (--domain=): Domain (Options=box,triangle,star, default=box).')
    print('   -b (--bandwidth=): Graph bandwidth exponent b in form h=delta^b (default=1).')
    print('   -d (--dilate_bc): Dilate boundary points by graph bandwidth.')
    print('   -s (--singular_kernel): Use a singular kernel for weights (default=False).')
    print('   -g (--use_grid): Replace iid sequence with a grid.')
    print('   -t (--num_trials=): Number of trials to run (default=10).')
    print('   -p (--parallel): Use parallel processing over the trials.')
    print('   -c (--num_cores=): Number of cores to use in parallel processing (default=1).')


#Parameters
num_verts = [2**e  for e in range(12,17)]
num_cores = 1
domain = 'box'
bandwidth_exp = 1.0
dilate_bc = False
singular_kernel = False
use_grid = False
num_trials = 10
parallel = False

# domain and kernel
Omega = domains.neumann_triangle()
eta = kernels.singular()

#Read command line parameters
try:
    opts, args = getopt.getopt(sys.argv[1:],"hD:b:dsgt:pc:",["help","domain=","bandwidth=","dilate_bc","singular_kernel","use_grid","num_trials=","parallel","num_cores="])
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print_help()
        sys.exit()
    elif opt in ("-D", "--domain"):
        domain = arg
    elif opt in ("-b", "--bandwidth"):
        bandwidth_exp = float(arg)
    elif opt in ("-d", "--dilate_bc"):
        dilate_bc = True
    elif opt in ("-s", "--singular_kernel"):
        singular_kernel = True
    elif opt in ("-g", "--use_grid"):
        use_grid = True
    elif opt in ("-t", "--num_trials"):
        num_trials = int(arg)
    elif opt in ("-p", "--parallel"):
        parallel = True
    elif opt in ("-c", "--num_cores"):
        num_cores = int(arg)

#Set num_trials=1 for grid
if use_grid:
    num_trials = 1
    
#print('Domain = '+domain)
#print('bandwidth = delta^%.2f'%bandwidth_exp)
#print('Dilate BC = ',dilate_bc)
#print('Singular Kernel = ',singular_kernel)
#print('Use Grid = ',use_grid)
#print('Number of trials = %d'%num_trials)
#print('Parallel = ',parallel)
#print('num_cores = %d'%num_cores)

%% Definition of one trial
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
    u = gl.lip_extension(W,I,g,tol=1e-7,prog=False,T=1e5,weighted=singular_kernel)

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

   

