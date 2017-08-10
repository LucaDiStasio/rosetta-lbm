#!/bin/bash

: '
=====================================================================================

Copyright (c) 2016 - 2017 Luca Di Stasio
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================================

DESCRIPTION

2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions.
Rectangular channel with circular obstacle.

Tested in Ubuntu 14.04
'

# read terminal and get input directory full path, input filename and output directory full path
inputdir=$1
inputfile=$2
outputdir=$3

echo ""
echo "====================================================================================="
echo ""
echo "   2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions"
echo ""
echo "                    Rectangular channel with circular obstacle"
echo ""
echo "====================================================================================="
echo ""

# create output directory if it does not exist

# read input file and assign data to variables

# check if input variables exists otherwise throw an error
if [ -z ${var+x} ]; then echo "var is unset"; else echo "var is set to '$var'"; fi

# set general flow properties

# define D2Q9 lattice constants

# create mesh

# locate obstacle

# set initial conditions: Poiseuille profile at equilibrium

# main loop (time cycles)

  # calculate macroscopic variables

  # impose macroscopic Dirichlet boundary conditions

  # impose microscopic boundary conditions at the inlet

  # impose microscopic boundary conditions at the outlet

  # collision step

  # bounce-back on the obstacle

  # streaming step

  # save to file
