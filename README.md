# 1D HD Stellar Winds

This code is used to calculate the winds from stars using the shooting method.
This is a fairly basic method where you iterate over a range of base velocities to see which one passes through the critical point.

Once the critical point is foung the wind can be solved


## Example


To run an example of the sun simply:
`./df-1d-polywind.sh 1.0 1.0 1.0e6 sun-1MK sun-1MK`

This will simulate a 1D wind for a 1 solar mass, 1 solar radius star with a base wind temperature of 1 million kelvin.

## Parameters

The code is written so that you can input most parameters from the command line:

Mstar - The mass of the star in solar masses

Rstar - The radius of the star in solar radii

T0 - The base wind temperature in Kelvin

Gamma - The polytropic index, which has to lie between 1 and 5./3. physically
        Note that a value of 1 exactly causes floating underflow errors, so for 'isothermal' wind just use 1.00000001 or something similar.


The wind density has no effect on the solution and just scales the density up and down. This can be set inside u0guess.py
