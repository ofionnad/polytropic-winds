"""
plots the polytropic wind from polywind.py and polywind2.py. 
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


plt.style.use('classic')
#sns.set()
#sns.set_context("paper")
#sns.set_style("whitegrid", {'xtick.major.size': '6.0', 
#                            'xtick.minor.size': '4.0', 'ytick.major.size': '6.0', 
#                            'ytick.minor.size': '4.0', 'xtick.direction': u'in', 
#                            'ytick.direction': u'in', 'xtick.color': '0.05'})

def plotwind(filename, saveimg, crit_point):
    """
    plots the polytropic wind from polywind.py and polywind2.py. 
    """
    x, u, rho = np.loadtxt(filename, delimiter=' ', unpack=True)
    saveimg = str(saveimg)
    #titleimg = str(plottitle)
    v = u/1e3 #convert m/s to km/s
    crit_point = str(crit_point)
    crit_point = crit_point[:4]
    #crit_point += '0000'
    crit_point = float(crit_point)
    index = np.where(x == crit_point)

    plt.figure(4, figsize=(6, 6))
    plt.subplot(211)
    plt.plot(x, v)
    plt.plot(x[index], v[index], 'o', label='critical point')
    #plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.xscale('log')
    plt.yscale('log')
    #plt.grid()
    plt.minorticks_on()
    plt.xlabel(r'$Stellar$ $Radius$ $(R_*)$')
    plt.ylabel('$Velocity$ $u$ $(km/s)$')
    #plt.title('%s' %titleimg)

    plt.subplot(212)
    plt.plot(x, rho)
    plt.plot(x[index], rho[index], 'o')
    plt.yscale('log')
    plt.xscale('log')
    #plt.grid()
    plt.xlabel(r'$Stellar$ $Radius$ $(R_*)$')
    plt.ylabel(r'$Density$ $\rho$')
    plt.tight_layout()
    plt.savefig(saveimg)
    plt.show()
