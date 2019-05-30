# 1D HD Stellar Winds

This code is used to calculate the winds from stars using the shooting method.
This is a fairly basic method where you iterate over a range of base velocities to see which one passes through the critical point.

Once the critical point is foung the wind can be solved


## Example


To run an example of the sun simply:
`./df-1d-polywind.sh 1.0 1.0 1.0e6 sun-1MK sun-1MK`

This will simulate a 1D wind for a 1 solar mass, 1 solar radius star with a base wind temperature of 1 million kelvin.
