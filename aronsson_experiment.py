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

#Print help
def print_help():
    
    print('========================================================')
    print('Convergence rate experiments for Lipschitz learning ')
    print('========================================================')
    print('                                                        ')
    print('Options:')
    print('   -h (--help): Print help.') 
    print('   -D (--domain=): Domain (Options=square, neumann_triangle, neumann_star, default=box).')
    print('   -n (--num_verts_range=): Range for number of vertices in the form 2^a up to 2^(b-1) (default: a,b=12,17).')
    print('   -b (--bandwidth=): Graph bandwidth constant a and exponent b in form h= a*delta^b (default: a,b=1,1).')
    print('   -d (--dilate_bc): Dilate boundary points by graph bandwidth.')
    print('   -s (--singular_kernel): Use a singular kernel for weights.')
    print('   -g (--use_grid): Replace iid sequence with a grid.')
    print('   -t (--num_trials=): Number of trials to run (default=10).')
    print('   -p (--parallel): Use parallel processing over the trials.')
    print('   -c (--num_cores=): Number of cores to use in parallel processing (default=1).')
    print('   -v (--verbose): Verbose mode.')


#Parameters
num_verts = [2**e  for e in range(12,17)]
num_cores = 1
domain = 'square'
bandwidth_exp = 1.0
bandwidth_constant = 1.0
dilate_bc = False
singular_kernel = False
use_grid = False
num_trials = 10
parallel = False
verbose = False

# domain and kernel
Omega = domains.neumann_triangle()
eta = kernels.singular()

#Read command line parameters
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hD:b:dsgt:pc:n:v",
                               ["help","domain=","bandwidth=","dilate_bc",
                                "singular_kernel","use_grid","num_trials=",
                                "parallel","num_cores=","num_verts_range=","verbose"])
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print_help()
        sys.exit()
    elif opt in ("-D", "--domain"):
        domain = arg
        Omega = getattr(domains, domain)()
    elif opt in ("-b", "--bandwidth"):
        bandwidth_constant = float(arg.split(',')[0])
        bandwidth_exp = float(arg.split(',')[1])
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
    elif opt in ("-n", "--num_verts_range"):
        num_verts_min = int(arg.split(',')[0])
        num_verts_max = int(arg.split(',')[1])
        
        num_verts = [2**e  for e in range(num_verts_min, num_verts_max)]
    elif opt in ("-v", "--verbose"):
        verbose = True

#Set num_trials=1 for grid
if use_grid:
    num_trials = 1

#Always dilate boundary conditions on square
if domain == 'square':
    dilate_bc = True
    
## Definition of one trial
def trial(T, n):
    #Draw data randomly        
    X = Omega.sample(n,use_grid)

    #Build a graph
    delta = (np.log(n)/n)**(1/2)
    h = bandwidth_constant * delta**bandwidth_exp
    W = gl.eps_weight_matrix(X,h,f=eta)*2/h
    if not gl.isconnected(W):
        print("Not connected!")
 
    #Boundary indices
    if dilate_bc:
        bdy_idx = Omega.boundary(X,h)
    else:
        bdy_idx = Omega.boundary(X,0)

    #Boundary values
    bdy_val = aronsson(X[bdy_idx,:])

    #Lipschitz extension
    u = gl.lip_extension(W,bdy_idx,bdy_val,tol=1e-4,prog=verbose,T=1e5,weighted=singular_kernel)

    #Error
    err = np.max(np.absolute(u-aronsson(X)))

    #Print to screen
    print('%d,%d,%f,%f'%(n,T,h,err),flush=True)

## main loop
print('Number of Points,Trial Number,Graph Bandwidth,Error')
for n in num_verts:
    #Number of cores for parallel processing
    if parallel:
        num_cores = min(multiprocessing.cpu_count(),num_cores)
        Parallel(n_jobs=num_cores)(delayed(trial)(T, n) for T in range(num_trials))
    else:
        for i in range(num_trials):
            trial(i, n)

   

