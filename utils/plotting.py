import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(fname, encoding = 'utf-8'):

    df = pd.read_csv(fname, encoding = encoding)
    n_all = df['Number of Points'].values
    h_all = df['Graph Bandwidth'].values
    err_all = df['Error'].values
    n = np.unique(n_all)
    h = -np.sort(-np.unique(h_all))
    err = np.zeros(len(n))
    i=0
    for nval in n:
        err[i] = np.mean(err_all[n_all==nval]) 
        i+=1
    return n,h,err

def single_plot(n, h, err, legend_loc='right'):
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.sans-serif": ["Helvetica"],
        "font.size": 12})
    styles = ['^-','o-','d-','s-','p-','x-','*-']
    
    plt.figure()
    
    delta = (np.log(n)/n)**(1/2)
    p = np.polyfit(np.log(delta[2:]),np.log(err[2:]),1)
    plt.loglog(delta,err,styles[0],label=r'$h_n\sim\delta_n, \eta=1, r=%.2f$'%max(p[0],0))
    
    plt.xlim(1.02*np.max(delta),0.98*np.min(delta))
    plt.xlabel(r'$\delta_n$',fontsize=18)
    plt.ylabel('Error',fontsize=18)
    plt.legend(loc=legend_loc,fontsize=14)
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='both', axis='both', linestyle='--')

def make_plot(base_file_name,legend_loc='right'):

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.sans-serif": ["Helvetica"],
        "font.size": 12})
    styles = ['^-','o-','d-','s-','p-','x-','*-']

    #eta=1
    n,h1,err1 = load_data('results/' + base_file_name + '_gscale1.csv')
    n,h2,err2 = load_data('results/' + base_file_name + '_gscale2.csv')
    n,h3,err3 = load_data('results/' + base_file_name + '_gscale3.csv')

    delta = (np.log(n)/n)**(1/2)
    
    plt.figure()

    #eta=1
    p = np.polyfit(np.log(delta),np.log(err1),1)
    plt.loglog(delta,err1,styles[0],label=r'$h_n\sim\delta_n, {\rm rate}\sim \delta_n^{\,%.2f}$'%max(p[0],0))

    p = np.polyfit(np.log(delta),np.log(err2),1)
    plt.loglog(delta,err2,styles[1],label=r'$h_n\sim\delta_n^{2/3}, {\rm rate}\sim \delta_n^{\,%.2f}$'%max(p[0],0))

    p = np.polyfit(np.log(delta),np.log(err3),1)
    plt.loglog(delta,err3,styles[2],label=r'$h_n\sim\delta_n^{1/2}, {\rm rate}\sim \delta_n^{\,%.2f}$'%max(p[0],0))

    plt.xlim(1.02*np.max(delta),0.98*np.min(delta))
    plt.xlabel(r'$\delta_n$',fontsize=18)
    plt.ylabel('Error',fontsize=18)
    plt.legend(loc=legend_loc,fontsize=14)
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='both', axis='both', linestyle='--')
    plt.savefig('figures/' + base_file_name + '_plot.pdf')

