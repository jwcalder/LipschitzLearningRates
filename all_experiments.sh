#!/bin/bash
#========================================================
#Convergence rate experiments for Lipschitz learning 
#========================================================
#                                                        
#Options:
#   -h (--help): Print help.
#   -D (--domain=): Domain (Options=square, neumann_triangle, neumann_star, default=box).
#   -n (--num_verts_range=): Range for number of vertices in the form 2^a up to 2^(b-1) (default: a,b=12,17).
#   -b (--bandwidth=): Graph bandwidth constant a and exponent b in form h= a*delta^b (default: a,b=1,1).
#   -d (--dilate_bc): Dilate boundary points by graph bandwidth.
#   -s (--singular_kernel): Use a singular kernel for weights.
#   -g (--use_grid): Replace iid sequence with a grid.
#   -t (--num_trials=): Number of trials to run (default=10).
#   -p (--parallel): Use parallel processing over the trials.
#   -c (--num_cores=): Number of cores to use in parallel processing (default=1).
#   -v (--verbose): Verbose mode.

#All experiments with iid sequence
#python3 aronsson_experiment.py -D neumann_star -b 3,1                 -t 100 -p -c 20     | tee results/aronsson_star_gscale1.csv
#python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666          -t 100 -p -c 20     | tee results/aronsson_star_gscale2.csv
#python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5            -t 100 -p -c 20     | tee results/aronsson_star_gscale3.csv

#python3 aronsson_experiment.py -D neumann_star -b 3,1          -d     -t 100 -p -c 20     | tee results/aronsson_star_dilateBC_gscale1.csv
#python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666   -d     -t 100 -p -c 20     | tee results/aronsson_star_dilateBC_gscale2.csv
#python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5     -d     -t 100 -p -c 20     | tee results/aronsson_star_dilateBC_gscale3.csv

#python3 aronsson_experiment.py -D square       -b 3,1                 -t 100 -p -c 20     | tee results/aronsson_square_gscale1.csv
#python3 aronsson_experiment.py -D square       -b 1.1,0.6666          -t 100 -p -c 20     | tee results/aronsson_square_gscale2.csv
#python3 aronsson_experiment.py -D square       -b 0.65,0.5            -t 100 -p -c 20     | tee results/aronsson_square_gscale3.csv

#python3 aronsson_experiment.py -D square       -b 3,1             -s  -t 20  -p -c 20     | tee results/aronsson_square_singular_gscale1.csv
#python3 aronsson_experiment.py -D square       -b 1.1,0.6666      -s  -t 20  -p -c 20     | tee results/aronsson_square_singular_gscale2.csv
#python3 aronsson_experiment.py -D square       -b 0.65,0.5        -s  -t 20  -p -c 20     | tee results/aronsson_square_singular_gscale3.csv

python3 aronsson_experiment.py -D neumann_star -b 3,1          -s     -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_singular_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666   -s     -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_singular_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5     -s     -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_singular_gscale3.csv

python3 aronsson_experiment.py -D neumann_star -b 3,1          -d -s  -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_dilateBC_singular_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666   -d -s  -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_dilateBC_singular_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5     -d -s  -t 20  -p -c 20 -n 12,16     | tee results/aronsson_star_dilateBC_singular_gscale3.csv

#All experiments with grid
python3 aronsson_experiment.py -D neumann_star -b 3,1        -g       -t 1                | tee results/aronsson_grid_star_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666 -g       -t 1                | tee results/aronsson_grid_star_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5   -g       -t 1                | tee results/aronsson_grid_star_gscale3.csv

python3 aronsson_experiment.py -D neumann_star -b 3,1        -g -s    -t 1                | tee results/aronsson_grid_star_singular_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666 -g -s    -t 1                | tee results/aronsson_grid_star_singular_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5   -g -s    -t 1                | tee results/aronsson_grid_star_singular_gscale3.csv

python3 aronsson_experiment.py -D neumann_star -b 3,1        -g -d    -t 1                | tee results/aronsson_grid_star_dilateBC_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666 -g -d    -t 1                | tee results/aronsson_grid_star_dilateBC_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5   -g -d    -t 1                | tee results/aronsson_grid_star_dilateBC_gscale3.csv

python3 aronsson_experiment.py -D neumann_star -b 3,1        -g -d -s -t 1                | tee results/aronsson_grid_star_dilateBC_singular_gscale1.csv
python3 aronsson_experiment.py -D neumann_star -b 1.1,0.6666 -g -d -s -t 1                | tee results/aronsson_grid_star_dilateBC_singular_gscale2.csv
python3 aronsson_experiment.py -D neumann_star -b 0.65,0.5   -g -d -s -t 1                | tee results/aronsson_grid_star_dilateBC_singular_gscale3.csv

python3 aronsson_experiment.py -D square       -b 3,1        -g       -t 1            	  | tee results/aronsson_grid_square_gscale1.csv
python3 aronsson_experiment.py -D square       -b 1.1,0.6666 -g       -t 1            	  | tee results/aronsson_grid_square_gscale2.csv
python3 aronsson_experiment.py -D square       -b 0.65,0.5   -g       -t 1                | tee results/aronsson_grid_square_gscale3.csv

python3 aronsson_experiment.py -D square       -b 3,1        -g    -s -t 1                | tee results/aronsson_grid_square_singular_gscale1.csv
python3 aronsson_experiment.py -D square       -b 1.1,0.6666 -g    -s -t 1                | tee results/aronsson_grid_square_singular_gscale2.csv
python3 aronsson_experiment.py -D square       -b 0.65,0.5   -g    -s -t 1                | tee results/aronsson_grid_square_singular_gscale3.csv



