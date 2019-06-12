#!/usr/bin/env python
"""
###############################################
#   Created: 3.10.16
#   Dualta O Fionnagain
#
#   Code to find polytropic wind solution.
#
#   Inputs: M - Stellar Mass
#        r0 - Stellar Radius
#        T0 - Coronal base temperature
#        gamma - polytropic index
###############################################
"""

from __main__ import *
import sys
import numpy as np

#define constants
h = 0.0002
pi = np.pi
kB = float(1.38e-23)
mp = float(1.673e-27)
G = float(6.674e-11)
mu = 0.5
#############CHANGE THESE###################
############################################
M0 = stellar_mass
R0 = stellar_radius
M = 1.989e30 * M0 #mass of the star in kg
r0 = 6.957e8 * R0 #radius of the star in m
T0 = stellar_temp #temperature of the corona
#gamma = 1.0001 #polytropic index
############################################
############################################

######## WRITE INPUT INFORMATION ###########
print('M_star = {}'.format(M0))
print('R_star = {}'.format(R0))
print('T0 = {:.2e} K'.format(T0))
############################################

if len(sys.argv) > 1:
    u0 = float(sys.argv[1])
    filename = "output/polytropic_wind_solar.dat"
    gamma = sys.argv[2]

"""
#some useful parameters

cs0 = math.sqrt((gamma*kB*T0)/(mu*mp))    #sound speed at surface
rc = ((G*M)/(2.*(cs0**2.)))    #crit radius
vesc0 = math.sqrt((2*G*M)/r0)    #escape velocity
c2v = cs0/vesc0    #ratio of velocity to sound speed
"""


def calculate(u0, gamma, rho, filename):
    """
    Main function: Runs the code
    Calls derivs and rk4 functions
    """
    break_ = 0
    y = u0 / r0 #normalised velocity
    T = T0
    x = 1.

    energy = 0.5*u0**2 - (G*M)/r0 + (gamma/(gamma-1))*kB*T0/(mu*mp)
    max_energy = ((5.-(3*gamma))/(gamma-1.)) * G * M/(r0*4)
    maximum_T = (G*M)/(r0) * (mu*mp)/kB * (gamma+1)/(4*gamma)

    if energy < 0:
        print("Error: energy < 0")
        print("Energy: ", energy)
        print("Max Energy: ", max_energy)
        sys.exit()

    if energy > max_energy:
        print("Error: energy > max_energy")
        print("Energy: ", energy)
        print("Max Energy: ", max_energy)
        print("T must be less than: ", maximum_T)
        sys.exit()

    f = open(filename, "w")
    #Call the derivs function here
    for k in range(10000000):

        dyy, numden, break_, radius = derivs(x, y, T, gamma, break_, k)

        #call the rk4 function here
        y = RK4(y, dyy, x, h, T, gamma, break_, k)

        rho1 = float(rho * (u0 / (y*r0))*(1/x)**2)

        if (k == 0) or (k%50 == 0):
            u = y*r0
            f.write("%f %.5e %.5e\n" % (x, u, rho1))

        T = T0 * (rho1/rho)**(gamma-1)
        x = x + h
        if break_:
            return (numden, radius)

    f.close()
    return


"""
------------Derivation Calculation - derivs------------
"""
def derivs(x, y, T, gamma, break_, kcount):
    """
    This function simply finds the derivative of the wind velocity w.r.t. radius.
    This function is called multiple times throughout this script, in the calculate() function and the RK4() function.
    """

    r = r0 * x

    vesc = (2.*G*M/r)**0.5
    num1 = gamma * T * (kB/(mu*mp)) - ((vesc**2.)/4.)

    den1 = (y*r0)**2 - (gamma * kB * T/(mu*mp))
    dydx = (y*r0) * (2./r) * (num1/den1)
    numden = "token" #placeholder string
    radius = x

    if num1 > 0:
        if (kcount%10==0) or (kcount==1):
            print("Em x = ", x, "num1 > 0")
        numden = "num"
        break_ = 1

    if den1 > 0:
        print("Em x = ", x, "den1 > 0")
        numden = "den"
        break_ = 1

    return dydx, numden, break_, radius


"""
-----------Runge Kutta method------------
"""

def RK4(y, dyy, x, h, T, gamma, break_, kcount):

    hh = h * 0.5
    h6 = h/6
    xh = x + hh

    #First iteration
    yt = y + (hh * dyy)

    #Second iteration
    dyt, nul, break_, nul2 = derivs(xh, yt, T, gamma, break_, kcount)
    yt = y + (hh * dyt)

    #Third iteration
    dym, nul, break_, nul2 = derivs(xh, yt, T, gamma, break_, kcount)
    yt = y + h*dym
    dym += dyt

    #fourth iteration
    s = x+h
    dyt, nul, break_, nul2 = derivs(s, yt, T, gamma, break_, kcount)

    #runge-kutta sum
    yout = y + h6 * (dyy + dyt + 2*dym)
    return yout
    #numden = calculate(u0, filename)

"""
Run the main code.
"""

if __name__ == "__main__":
    numden = calculate(u0, filename)

