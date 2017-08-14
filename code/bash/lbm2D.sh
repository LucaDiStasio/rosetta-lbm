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

clear

function parseNumberDataLine {
  #IFS='#' read -ra dataPart <<< "$1"
  #IFS='=' read -ra data <<< "${dataPart[0]}"
  string=$1
  numstring="${string//[!0-9]/}"
  #echo $((10#$numstring))
  echo $numstring
}

function parseBooleanDataLine {
  IFS='#' read -a dataPart <<< "$1"
  IFS='=' read -a data <<< "${dataPart[0]}"
  if [[ ${data[1]} == *"true"* ]] ; then
    echo "true"
  else
    echo ""
  fi
}

function checkVarExists {
  if [[ ${!1} ]] ; then
    echo "$1 is set"
  else
    echo "$1 is not set"
    echo "Error detected in input file. Data is missing. Interrupting execution."
    exit
  fi
}

# read terminal and get input directory full path, input filename and output directory full path
if [[ $# < 1 ]] ; then
  echo ""
  echo "Error: no input provided."
  echo ""
  exit
elif [[ $# == 1 ]] ; then
  echo ""
  echo "./lbm2D.sh /input/directory/full/path/with/no/end/slash /input/filename/with/extension /output/directory/full/path"
  echo ""
  exit
else
  inputdir=$1
  inputfile=$2
  outputdir=$3
fi
# print header to screen
echo ""
echo "====================================================================================="
echo ""
echo "   2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions"
echo ""
echo "                    Rectangular channel with circular obstacle"
echo ""
echo "                          Luca Di Stasio, 2016-2017"
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
inputFullPath=$inputdir"/"$inputfile
echo ""
echo "Reading input file "$inputFullPath" and assigning data to variables ..."
while IFS= read -r line; do
  if [[ $line == *"lx"* ]] ; then
    lx=$( parseNumberDataLine $line )
  elif [[ $line == *"ly"* ]] ; then
    ly=$( parseNumberDataLine $line )
  elif [[ $line == *"isObstacle"* ]] ; then
    isObstacle=$( parseBooleanDataLine $line )
  elif [[ $line == *"xObstacle"* ]] ; then
    xObstacle=$( parseNumberDataLine $line )
  elif [[ $line == *"yObstacle"* ]] ; then
    yObstacle=$( parseNumberDataLine $line )
  elif [[ $line == *"rObstacle"* ]] ; then
    rObstacle=$( parseNumberDataLine $line )
  elif [[ $line == *"uMax"* ]] ; then
    uMax=$( parseNumberDataLine $line )
  elif [[ $line == *"Re"* ]] ; then
    Re=$( parseNumberDataLine $line )
  elif [[ $line == *"Tmax"* ]] ; then
    Tmax=$( parseNumberDataLine $line )
  elif [[ $line == *"Tsave"* ]] ; then
    Tsave=$( parseNumberDataLine $line )
  fi
done < $inputFullPath
echo "... done."
# check if input variables exists otherwise throw an error
echo ""
echo "Checking if input variables are set ..."
checkVarExists lx
checkVarExists ly
checkVarExists xObstacle
checkVarExists yObstacle
checkVarExists rObstacle
checkVarExists uMax
checkVarExists Re
checkVarExists Tmax
checkVarExists Tsave
echo "... done."
# set general flow properties
echo ""
echo "Setting general flow properties ..."
nu=`echo "$uMax*2.0*$rObstacle/$Re" | bc -l` # kinematic viscosity
omega=`echo "1.0/(3*$nu+0.5)" | bc -l`       # relaxation parameter
echo "... done."
# define D2Q9 lattice constants
echo ""
echo "Defining D2Q9 lattice constants ..."
ws[0]=`echo "4.0/9.0" | bc -l`
ws[1]=`echo "1.0/9.0" | bc -l`
ws[2]=`echo "1.0/9.0" | bc -l`
ws[3]=`echo "1.0/9.0" | bc -l`
ws[4]=`echo "1.0/9.0" | bc -l`
ws[5]=`echo "1.0/36.0" | bc -l`
ws[6]=`echo "1.0/36.0" | bc -l`
ws[7]=`echo "1.0/36.0" | bc -l`
ws[8]=`echo "1.0/36.0" | bc -l`
echo "... done."
# summarize simulation parameters
echo ""
echo "SIMULATION PARAMETERS"
echo ""
echo "Number of cells in x-direction lx = "$lx
echo "Number of cells in y-direction ly = "$ly
echo "maximum velocity of Poiseuille flow at the inlet uMax = "$uMax
echo "Reynolds number Re = "$Re
echo "total number of iterations Tmax = "$Tmax
echo "cycle time of saving to file operations Tsave = "$Tsave
if [[ $isObstacle ]] ; then
  echo "Obstacle is present:"
  echo "    Coordinate of obstacle's center in x-direction xObstacle = "$xObstacle
  echo "    Coordinate of obstacle's center in x-direction yObstacle = "$yObstacle
  echo "                                 Obstacle's radius rObstacle = "$rObstacle
else
  echo "Obstacle is NOT present"
fi


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
