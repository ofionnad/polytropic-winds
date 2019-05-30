#!/usr/bin/env python
"""
Author: Dualta O Fionnagain
Date: 5.10.16
Updated: 15.11.16 - made this script work with polywind.py code to automate shooting method for polytropc wind solution.

To Run:
    Change velocty guesses (from umin --> umax, with nguess increments, to fit the wind.

"""
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import polywind as pw
import extrapolate as ex
import polywind2 as pw2
import plotpolywind as pltwnd

sns.set()
sns.set_context('paper')
sns.set_style("whitegrid", {'xtick.major.size': '6.0',
                            'xtick.minor.size': '4.0', 'ytick.major.size': '6.0',
                            'ytick.minor.size': '4.0', 'xtick.direction': u'in',
                            'ytick.direction': u'in', 'xtick.color': '0.05'})

############# code parameters ########################
n_guess = 80    #resolution of shooting search
n_runs = 5     #number of times to run shooting search
#####################################

############# wind parameters ######################
umin = 1.0     #start of shooting velocity search (in m/s)
umax = 1.0e4  #end of shooting velocity search (in m/s)
### NOTE: wider search range for u0 works better than a narrow one
gamma = float(gamma_parameter)
rho0 = float(1.0e5)

filename = "output/directory_name/file_name.dat"
final_image = "output/directory_name/file_name.png"
#plottitle = 'starname - g=1.05 T=1.89MK'
#####################################

for j in range(n_runs):
    u_0 = np.linspace(umin, umax, n_guess)
    xstop = np.array(n_guess)
    pos = np.zeros(n_guess)
    print("Run number: ", j+1)

    for x in range(n_guess-1):
        outputstring = pw.calculate(u_0[x], gamma, rho0, filename)
        pos[x] = outputstring[1]
        if outputstring[0] == "den":
            uini = u_0[x]
            index = x
            break
    #repeat the process above with a smaller range, closer to the critical point.
    umin = u_0[index-1]
    umax = u_0[index+1]

    plt.figure(j)
    plt.plot(u_0, pos, 'x')
    plt.plot(u_0, pos)
    #plt.grid()
    plt.minorticks_on()
    plt.plot(uini, outputstring[1], 'o')
    plt.pause(0.05)
    plt.title("Run: %i" %j)
    plt.xlabel("velocity (m/s)")
    plt.ylabel(r'distance ($R_*$)')


print("\n Extrapolating across critical point ... .. \n")
ex.extrapolation(uini, rho0, filename)
ex.extrapolation(uini, rho0, filename)


plt.close('all')

print('\n \n Solving the wind... ... ...\n \n')
pw2.postwind(uini, gamma, rho0, filename)

print('\n \n Plotting ...\n \n')
pltwnd.plotwind(filename, final_image, outputstring[1])

