# LipschitzLearningRates
The code in this repository reproduces the experimental results on convergence rates for k-nearest neighbor graph Laplacians from our paper 

Bungert, Calder, and Roith. [Uniform Convergence Rates for Lipschitz Learning on Graphs](https://arxiv.org/abs/). arXiv, 2021.

The Python package [GraphLearning](https://github.com/jwcalder/GraphLearning) is required to run the experiments. Install with
```
pip install graphlearning
```
The script `aronsson_experiment.py` runs convergence rate experiments, to see the usage run
```
python aronsson_experiment.py -h
```
The bash script `all_experiments.sh` contains the commands for running all experiments from our paper. The results of the experiments are saved in .csv files in the results folder. To generate the plots and figures from the paper run
```
python generate_plots.py
```
All figures are saved in the figures folder.
