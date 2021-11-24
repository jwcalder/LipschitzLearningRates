# :chart_with_downwards_trend: LipschitzLearningRates

<img src="https://user-images.githubusercontent.com/44805883/143242524-56382527-3353-4270-b23a-416d5b14f3e0.png" width="800">


The code in this repository reproduces the experimental results on convergence rates for k-nearest neighbor graph infinity Laplacians from our paper 

Bungert, Calder, and Roith. [Uniform Convergence Rates for Lipschitz Learning on Graphs](https://arxiv.org/abs/). arXiv, 2021.

Feel free to use it and please refer to our paper when doing so.
```
@misc{bungert2021uniform,
      title={Uniform Convergence Rates for Lipschitz Learning on Graphs}, 
      author={Leon Bungert and Jeff Calder and Tim Roith},
      year={2021},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={math.NA}
}
```
## :wrench: Usage

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

## :bulb: Mathematical Models

Our code verifies our convergence proofs for solutions of the graph infinity Laplacian equation

<p align="center">
      <img src="https://latex.codecogs.com/svg.latex?\begin{cases}\max_{y\in\Omega_n}\eta(|x-y|/h_n)(u(y)-u(x))+\min_{y\in\Omega_n}\eta(|x-y|/h_n)(u(y)-u(x)),\;&x\in\Omega_n\setminus\mathcal{O}_n\\u(x)=g(x),\;&x\in\mathcal{O}_n\end{cases}" title="GraphL" />
</p>

on a point cloud <img src="https://latex.codecogs.com/svg.latex?\Omega_n" title="graph"/> with constraint set <img src="https://latex.codecogs.com/svg.latex?\mathcal{O}_n" title="calOn"/> to an *Absolutely Minimizing Lipschitz Extension* on the continuum domain <img src="https://latex.codecogs.com/svg.latex?\Omega" title="domain"/> with constraint set <img src="https://latex.codecogs.com/svg.latex?\mathcal{O}" title="calO"/>, i.e., a solution of

<p align="center">
      <img src="https://latex.codecogs.com/svg.latex?\begin{cases}\operatorname{Lip}_\Omega(u;A)=\operatorname{Lip}_\Omega(u;\partial\,A),\;&\forall\,A\subset\subset\Omega\\u=g,\;&\text{on}\,\mathcal{O},\end{cases}" title="AMLE" />
</p>

where <img src="https://latex.codecogs.com/svg.latex?\operatorname{Lip}_\Omega" title="Lip"/> is the *geodesic* Lipschitz constant.

The relative scaling of the graph bandwidth <img src="https://latex.codecogs.com/svg.latex?h_n" title="bw"/> to the resolution of the graph <img src="https://latex.codecogs.com/svg.latex?\delta_n" title="delta"/>, defined as Hausdorff distance between <img src="https://latex.codecogs.com/svg.latex?\Omega_n" title="graph"/> and <img src="https://latex.codecogs.com/svg.latex?\Omega" title="domain"/> can be set with the `-b` option in `all_experiments.sh`.
