#!/bin/bash

#####
#
#	Created: 1.6.17
#	Author: Dualta O Fionnagain
#	
#	Description: Runs 1D polytropic wind
#		Inputs: Filename, Imagename, Temperature, Mass, Radius
#
#
#####



usage="$(basename "$0") [-h] M, R, T, dir, file \n -- program to calculate polytropic wind"
curdir=$( pwd )

while getopts 'h' option; do
	case "$option" in
		h) echo -e "$usage"
			exit
			;;
		\?) printf "illegal option: -%s\n" "$OPTARG" >&2
			echo -e "$usage" >&2
			exit 1
	esac
done


if [ $# != 5 ]
then
	echo Needs 5 arguments:
	echo Mstar - solar units
	echo Rstar - solar units
	echo Temperature - K 
	echo directory name
	echo filename
	exit
fi

if [ ! -d $curdir/$4 ]
then
	mkdir $4
fi

# Copy all the new values into the code to be run
sed "s/stellar_mass/$1/g;s/stellar_radius/$2/g;s/stellar_temp/$3/g" src/polywind.py > $curdir/polywind.py
sed "s/stellar_mass/$1/g;s/stellar_radius/$2/g;s/stellar_temp/$3/g" src/polywind2.py > $curdir/polywind2.py
sed "s/directory_name/$4/g;s/file_name/$5/g" src/u0guess.py > $curdir/u0guess.py
cp src/extrapolate.py $curdir/extrapolate.py
cp src/plotpolywind.py $curdir/plotpolywind.py

# Run the code
python $curdir/u0guess.py 


# Calculate the distance of terrestrial and martian analogues and print their distances and the data:
rade=$(echo "scale=1; 215.0 / $2" | bc)
radm=$(echo "scale=1; 327.7 / $2" | bc )


echo -e \n ----
echo Earth Analogue Distance: $rade  R_star
echo Mars Analogue Distance: $radm   R_star

echo -e ---- \n

echo -e " Earth Analogue data: \n ---- \n Distance   v (m/s)      rho (norm) " && cat $4/$5.dat | awk '$1 ~ '$rade' '
echo -e "\n ----\n  Mars-Analogue data: \n Distance  v (m/s)       rho(norm)" && cat $4/$5.dat | awk '$1 ~ '$radm' '



