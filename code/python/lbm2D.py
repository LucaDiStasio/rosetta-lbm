#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
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

Tested with Python 2.7 in Ubuntu 14.04

'''

import sys
import errno
from os import makedirs
from os.path import join
from datetime import datetime
from time import strftime
import getopt

def parseInput(fileFullpath,keywords,types,commentSep,valueSep):
    with open(fileFullpath,'r') as f:
        lines = f.readlines()
    inputs = {}
    for key in keywords:
        for line in lines:
            if key in line:
                if 'integer' in types[key]:
                    inputs[key] = int(line.replace('\n','').split(commentSep)[0].split(valueSep)[1].replace(' ',''))
                elif 'float' in types[key]:
                    inputs[key] = float(line.replace('\n','').split(commentSep)[0].split(valueSep)[1].replace(' ',''))
                elif 'boolean' in types[key]:
                    inputField = line.replace('\n','').split(commentSep)[0].split('=')[1].replace(' ','')
                    if 'true' in inputField or 'TRUE' in inputField or 'True' in inputField:
                        inputs[key] = True
                    else:
                        inputs[key] = False
                else:
                    inputs[key] = line.replace('\n','').split(commentSep)[0].split(valueSep)[1].replace(' ','')
                break
    return inputs

def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hd:i:o:',['help','Help',"inputfile", "input","inpdir", "inputdirectory", "idir","outdir", "outdirectory", "odir"])
    except getopt.GetoptError:
        print('runAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('======================================================================================================')
            print(' ')
            print('              2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions')
            print(' ')
            print('                            Rectangular channel with circular obstacle')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2017')
            print(' ')
            print('======================================================================================================')
            print(' ')
            print('Program syntax:')
            print('lbm2D.py -d <input deck> -i <input directory> -o <output directory> -c <number of cpus>')
            print(' ')
            print('Mandatory arguments:')
            print('-d <input deck>                        ==> if extension is not provided, .deck is assumed')
            print('-i <input directory full path>')
            print('-o <output directory full path>')
            print(' ')
            print('optional arguments:')
            print('-c <number of cpus>                        ==> if omitted, serial execution is assumed')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-d", "--inputfile", "--input"):
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
            else:
                inputfile = arg + '.deck'
        elif opt in ("-i", "--inpdir", "--inputdirectory", "--idir"):
            if arg[-1] != '/':
                inputdir = arg
            else:
                inputdir = arg[:-1]
        elif opt in ("-o", "--outdir", "--outdirectory", "--odir"):
            if arg[-1] != '/':
                outdir = arg
            else:
                outdir = arg[:-1]

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit(2)
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit(2)
    if 'outdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit(2)
    # print header to screen
    print('')
    print('=====================================================================================')
    print('')
    print('   2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions')
    print('')
    print('                    Rectangular channel with circular obstacle')
    print('')
    print('                          Luca Di Stasio, 2016-2017')
    print('')
    print('=====================================================================================')
    print('')
    # create output directory if it does not exist
    print('')
    print('Creating output directory ' + outdir + ' ...')
    try:
        makedirs(outdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print('... done')
    print('')
    # read input file and assign data to variables
    inputFullPath=join(inputdir,inputfile)
    print('')
    print('Reading input file ' + inputFullPath + ' and assigning data to variables ...')
    keys = ['lx','ly','isObstacle','xObstacle','yObstacle','rObstacle','uMax','Re','Tmax','Tsave']
    types = {}
    types['lx'] = 'integer'
    types['ly'] = 'integer'
    types['isObstacle'] = 'boolean'
    types['xObstacle'] = 'integer'
    types['yObstacle'] = 'integer'
    types['rObstacle'] = 'integer'
    types['uMax'] = 'float'
    types['Re'] = 'float'
    types['Tmax'] = 'integer'
    types['Tsave'] = 'integer'
    inputData = parseInput(inputFullPath,keys,types,'#','=')
    print('... done.')
    # check if input variables exists otherwise throw an error
    print('')
    print('Checking if input variables are set ...')
    for key in keys:
        if key not in inputData:
            print(key + ' is not defined. Error: check the input file for missing data. Terminating program.')
            sys.exit(2)
    print('... done.')
    # set general flow properties
    print('')
    print('Setting general flow properties ...')
    if inputData['isObstacle']:
        inputData['nu'] = inputData['uMax']*2.0*inputData['rObstacle']/inputData['Re'] # kinematic viscosity
    else:
        inputData['nu'] = inputData['uMax']*inputData['ly']/inputData['Re']            # kinematic viscosity
    inputData['omega'] = 1.0/(3*inputData['nu']+0.5)                                   # relaxation parameter
    print('... done.')
    # define D2Q9 lattice constants
    print('')
    print('Defining D2Q9 lattice weights, velocities and pairs of opposite velocities ...')
    ws = [4.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/36.0,1.0/36.0,1.0/36.0,1.0/36.0]
    c = [[0,0],
         [1,0],
         [0,1],
         [-1,0],
         [0,-1],
         [1,1],
         [-1,1],
         [-1,-1],
         [1,-1]]
    opposites = [1,4,5,2,3,8,9,6,7]
    print('... done.')
    # summarize simulation parameters
    print('')
    print('SIMULATION PARAMETERS')
    print('')
    print('                    Number of cells in x-direction lx = ' + str(inputData['lx']))
    print('                    Number of cells in y-direction ly = ' + str(inputData['ly']))
    print('Maximum velocity of Poiseuille flow at the inlet uMax = ' + str(inputData['uMax']))
    print('                                   Reynolds number Re = ' + str(inputData['Re']))
    print('                               Kinematic viscosity nu = ' + str(inputData['nu']))
    print('                           Relaxation parameter omega = ' + str(inputData['omega']))
    print('                      Total number of iterations Tmax = ' + str(inputData['Tmax']))
    print('        Cycle time of saving to file operations Tsave = ' + str(inputData['Tsave']))
    if inputData['isObstacle']:
      print('Obstacle is present:')
      print('    Coordinate of obstacle''s center in x-direction xObstacle = ' + str(inputData['xObstacle']))
      print('    Coordinate of obstacle''s center in x-direction yObstacle = ' + str(inputData['yObstacle']))
      print('                                 Obstacle''s radius rObstacle = ' + str(inputData['rObstacle']))
    else:
      print('Obstacle is NOT present')

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

if __name__ == "__main__":
    main(sys.argv[1:])
