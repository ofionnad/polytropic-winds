#!/usr/bin/env python
"""
#----------------------------------------------
#   Dualta O Fionnagain
#   Created: 4.10.16
#   Polytropic wind solution: After sonic point
#-----------------------------------------------
"""
import sys
import math
import numpy as np
from polywind import RK4
#import matplotlib.pyplot as plt
#from scipy.integrate import ode

#define constants
h = 0.0002
pi = np.pi
kB = 1.38e-23
mp = 1.673e-27
G = 6.674e-11
mu = 0.5

##############CHANGE THESE##################
############################################
M = 1.989e30 * stellar_mass #mass of the star in kg
r0 = 6.957e8 * stellar_radius #radius of the star in m
T0 = stellar_temp #temperature of the corona
#gamma = 1.0001  #polytropic index
############################################
############################################

if len(sys.argv) > 1:
    u0 = float(sys.argv[1])
    filename = 'output/polytropic_wind_solar.dat'


def postwind(u_0, gamma, rho0, file_name):
    """
    Function that runs the polytropic model after the critical point (and extrapolation())
    """


    #Read in last values after extrapolation
    x2, v = np.loadtxt(file_name, delimiter=' ', usecols=(0, 1), unpack=True)
    x1 = float(x2[x2.size - 1])
    u1 = float(v[v.size - 1])
    y = u1 / r0 #normalised velocity after sonic point (u1)
    rho1 = float(rho0 * (u_0/u1) * (1./x1)**2.)
    T = T0 * (rho1/ rho0)**(gamma -1)
    cs = math.sqrt((gamma*kB*T)/(mu*mp))
    rc = ((G*M)/(2.*(cs**2.))) / r0

    print("cs    =   {}\n".format(cs))
    print("r_c    =   {}\n".format(rc))


    f = open(file_name, "a")
    for k in range(10000000):
        dyy = derivs2(x1, y, T, gamma)

        y = RK42(y, dyy, x1, h, T, gamma)

        u = y*r0

        rho1 = float(rho0 * (u_0/u)*(1./x1)**2.)
        #T = T0 * (rho1/rho0)**(gamma-1.)


        if (x1 <= 5) and (k%50 == 0):
            f.write("%f %.5e %.5e\n" % (x1, u, rho1))
        elif (x1 <= 12) and (k%100 == 0):
            f.write("%f %.5e %.5e\n" % (x1, u, rho1))
        elif (x1 > 12) and (k%500 == 0):
            f.write("%f %.5e %.5e\n" % (x1, u, rho1))

        x1 = x1 + h

        if x1 >= 500:
            return

    f.close()



#--------------------------
#   derivatives
#--------------------------

def derivs2(x, y, T, gamma):
    """
    Finds derivatives of velocity wrt radius.
    Like other derivatives function,
    without check for critical point (as this part of code has passed it)
    """
    r = r0 * x

    vesc = (2.*G*M/r)**0.5
    num1 = gamma * T * (kB/(mu*mp)) - ((vesc**2.)/4.)
    den1 = (y*r0)**2 - (gamma * kB * T/(mu*mp))
    dydx = (y*r0) * (2./r) * (num1/den1)

    return dydx

#------------------------
#   runge-kutta method
#------------------------

def RK42(y, dyy, x, h0, T, gamma):
    """
    Standard Runge-Kutta method
    """
    hh = h0 * 0.5
    h6 = h0/6
    xh = x + hh

    #First iteration
    yt = y + (hh * dyy)

    #Second iteration
    dyt = derivs2(xh, yt, T, gamma)

    yt = y + (hh * dyt)

    #Third iteration
    dym = derivs2(xh, yt, T, gamma)
    yt = y + h0*dym
    dym += dyt

    #fourth iteration
    s = x+h0
    dyt = derivs2(s, yt, T, gamma)

    #runge-kutta sum
    yout = y + h6 * (dyy + dyt + 2*dym)
    return yout

#
#   Run the main code
#
if __name__ == "__main__":
    postwind(u0, filename)

