#!/usr/bin/env python
"""
Script to extrapolate polywind across critical point.
"""
import sys
import numpy as np
import pandas as pd

#u0 = 1.19755e4
if len(sys.argv) > 1:
    u0 = float(sys.argv[1])
    filename = "output/polytropic_wind.dat"

def extrapolation(u0, rho0, filename):
    """
    This extrapolates the polytropic wind across the critical point at which it stops in polywind.py.
    """

    df = pd.read_csv(filename, sep=' ', header=None)
    rad = df[0].values
    vel = df[1].values
    rho = df[2].values

    range_extra = 0.01
    radius = []
    velocity = []
    density = []
    for x in range(rad.size):
        if x > (rad.size-3):
            radius.append(rad[x])
            velocity.append(vel[x])
            density.append(rho[x])
    rho1 = rho0*(u0/velocity[1])*(1/(radius[1]+range_extra))**2
    s = (velocity[1]-velocity[0])/(radius[1]-radius[0])
    u1 = velocity[1] + s*range_extra

    x1 = (radius[1]+range_extra)

    with open(filename, "a") as f:
        f.write("%f %f %.5e\n" % (x1, u1, rho1))

    return

if __name__ == '__main__':
    extrapolation(u0, filename)

