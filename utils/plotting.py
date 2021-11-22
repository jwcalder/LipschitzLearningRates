import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(fname):

    df = pd.read_csv(fname)
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

def make_plot(base_file_name,legend_loc='right'):

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.sans-serif": ["Helvetica"],
        "font.size": 12})
    styles = ['^-','o-','d-','s-','p-','x-','*-']

    n,h1,err1 = load_data('results/' + base_file_name + '_gscale1.csv')
    n,h2,err2 = load_data('results/' + base_file_name + '_gscale2.csv')
    #n,h3,err3 = load_data('results/' + base_file_name + '_gscale3.csv')

    n,h1,err1_s = load_data('results/' + base_file_name + '_singular_gscale1.csv')
    n,h2,err2_s = load_data('results/' + base_file_name + '_singular_gscale2.csv')
    #n,h3,err3_s = load_data('results/' + base_file_name + '_singular_gscale3.csv')

    delta = (np.log(n)/n)**(1/2)

    plt.figure()
    #eta=1
    p = np.polyfit(np.log(delta[2:]),np.log(err1[2:]),1)
    plt.loglog(delta,err1,styles[0],label=r'$h_n\sim\delta_n, \eta=1, r=%.2f$'%max(p[0],0))

    p = np.polyfit(np.log(delta[2:]),np.log(err2[2:]),1)
    plt.loglog(delta,err2,styles[1],label=r'$h_n\sim\delta_n^{2/3}, \eta=1, r=%.2f$'%max(p[0],0))

    #p = np.polyfit(np.log(delta),np.log(err3),1)
    #plt.loglog(delta,err3,styles[2],label=r'$h_n\sim\delta_n^{1/2}, \eta=1, r=%.2f$'%max(p[0],0))

    #eta=1/t
    p = np.polyfit(np.log(delta[2:]),np.log(err1_s[2:]),1)
    plt.loglog(delta,err1_s,styles[3],label=r'$h_n\sim\delta_n, \eta(t)=t^{-1}, r=%.2f$'%max(p[0],0))

    p = np.polyfit(np.log(delta[2:]),np.log(err2_s[2:]),1)
    plt.loglog(delta,err2_s,styles[4],label=r'$h_n\sim\delta_n^{2/3}, \eta(t)=t^{-1}, r=%.2f$'%max(p[0],0))

    #p = np.polyfit(np.log(delta[2:]),np.log(err3_s[2:]),1)
    #plt.loglog(delta,err3_s,styles[5],label=r'$h_n\sim\delta_n^{1/2}, \eta(t)=t^{-1}, r=%.2f$'%max(p[0],0))

    plt.xlim(1.02*np.max(delta),0.98*np.min(delta))
    plt.xlabel(r'$\delta_n$',fontsize=18)
    plt.ylabel('Error',fontsize=18)
    plt.legend(loc=legend_loc,fontsize=14)
    plt.tight_layout()
    ax = plt.gca()
    ax.grid(which='both', axis='both', linestyle='--')
    plt.savefig('figures/' + base_file_name + '_plot.pdf')



