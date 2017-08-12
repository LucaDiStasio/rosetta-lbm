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

function parseDataLine {
  IFS='#' read -a dataPart <<< "$1"
  IFS='=' read -a data <<< "${dataPart[0]}"
  echo $((10#${data[1]}))
}

function checkVarExists {
  if [ -z ${$1+x} ]; then echo $1" is unset"; else echo $1" is set"; fi
}

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
echo ""
echo "Creating output directory "$outputdir" ..."
mkdir -p $outputdir
echo "... done"
echo ""
# read input file and assign data to variables
inputFullPath=$inputdir$inputfile
echo ""
echo "Reading input file "$inputFullPath" and assigning data to variables ..."
while IFS= read -r line; do
  if [[ $line == *"lx"* ]] ; then
    lx = $( parseDataLine $line )
  elif [[ $line == *"ly"* ]] ; then
    ly = $( parseDataLine $line )
  elif [[ $line == *"isObstacle"* ]] ; then
    isObstacle = $( parseDataLine $line )
  elif [[ $line == *"xObstacle"* ]] ; then
    xObstacle = $( parseDataLine $line )
  elif [[ $line == *"yObstacle"* ]] ; then
    yObstacle = $( parseDataLine $line )
  elif [[ $line == *"rObstacle"* ]] ; then
    rObstacle = $( parseDataLine $line )
  elif [[ $line == *"uMax"* ]] ; then
    uMax = $( parseDataLine $line )
  elif [[ $line == *"Re"* ]] ; then
    Re = $( parseDataLine $line )
  elif [[ $line == *"Tmax"* ]] ; then
    Tmax = $( parseDataLine $line )
  elif [[ $line == *"Tsave"* ]] ; then
    Tsave = $( parseDataLine $line )
  fi
done < $inputFullPath
echo "... done."
# check if input variables exists otherwise throw an error


# summarize simulation parameters
echo ""
echo "SIMULATION PARAMETERS"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""


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
