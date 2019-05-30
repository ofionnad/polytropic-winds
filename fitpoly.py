import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

sns.set()
sns.set_context('paper')
sns.set_style("whitegrid", {'xtick.major.size': '6.0', 
                            'xtick.minor.size': '4.0', 'ytick.major.size': '6.0', 
                            'ytick.minor.size': '4.0', 'xtick.direction': u'in', 
                            'ytick.direction': u'in', 'xtick.color': '0.05'})


filename = sys.argv[1]+".dat"

data = np.loadtxt(filename, delimiter=' ')
r = data[:, 0]
v = data[:, 1]
rho = data[:, 2]

v_cm = v*100.0 

logr = np.log10(r)
logv = np.log10(v_cm)

p = np.poly1d(np.polyfit(logr, logv, 8))

plt.plot(logr, logv)
plt.plot(logr, p(logr))
plt.yscale('log')
plt.xscale('log')

plt.title('velocity profile fit')
plt.xlabel('Log (Rstar)')
plt.ylabel('Log (Velocity m/s)')

plt.show()
