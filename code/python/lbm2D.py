#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2017 - 2018 Université de Lorraine & Luleå tekniska universitet
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

import sys, os
import errno
import numpy as np
from os import makedirs
from os.path import isfile, join, exists
from shutil import copyfile
from datetime import datetime
from time import strftime
import getopt
import timeit

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                              CSV files
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')

def appendCSVfile(dir,filename,data):
    # data is a list of lists
    # each list is written to a row
    # no check is made on data consistency
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'a') as csv:
        for row in data:
            line = ''
            for v,value in enumerate(row):
                if v>1:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                                 Log files
#===============================================================================#

def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print('\n')

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print('===============================================================================================\n')

def writeTitleSecToLogFile(logFileFullPath,mode,title,toScreen):
    writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a',title,toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S'),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Platform: ' + platform(),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)

def writeErrorToLogFile(logFileFullPath,mode,exc,err,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
        log.write('                                     AN ERROR OCCURED\n')
        log.write('\n')
        log.write('                                -------------------------\n')
        log.write('\n')
        log.write(str(exc) + '\n')
        log.write(str(err) + '\n')
        log.write('\n')
        log.write('Terminating program\n')
        log.write('\n')
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
    if toScreen:
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')
        print('                                     AN ERROR OCCURED\n')
        print('\n')
        print('                                -------------------------\n')
        print('\n')
        print(str(exc) + '\n')
        print(str(err) + '\n')
        print('\n')
        print('Terminating program\n')
        print('\n')
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')

#===============================================================================#
#                                 Input file
#===============================================================================#
def parseInput(fileFullpath,keywords,keywordSep,commentSep,valueSep):
    with open(fileFullpath,'r') as f:
        lines = f.readlines()
    inputs = {}
    for key in keywords:
        for line in lines:
            if key in line:
                if 'int' in line.replace('\n','').split(commentSep)[0].split(keywordSep)[1]:
                    inputs[key] = int(line.replace('\n','').split(commentSep)[0].split(keywordSep)[0].split(valueSep)[1].replace(' ',''))
                elif 'float' in line.replace('\n','').split(commentSep)[0].split(keywordSep)[1]:
                    inputs[key] = float(line.replace('\n','').split(commentSep)[0].split(keywordSep)[0].split(valueSep)[1].replace(' ',''))
                elif 'bool' in line.replace('\n','').split(commentSep)[0].split(keywordSep)[1]:
                    inputField = line.replace('\n','').split(commentSep)[0].split(keywordSep)[0].split(valueSep)[1].replace(' ','')
                    if 'true' in inputField or 'TRUE' in inputField or 'True' in inputField:
                        inputs[key] = True
                    else:
                        inputs[key] = False
                else:
                    inputs[key] = line.replace('\n','').split(commentSep)[0].split(valueSep)[1].replace(' ','')
                break
    return inputs

#===============================================================================#
#===============================================================================#
#                              LBM functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                           Weights and velocities
#===============================================================================#

def simpleLBMwv(D,Q):
    params = {}
    if D==2:
        if Q==9:
            params['ws'] = [4.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/36.0,1.0/36.0,1.0/36.0,1.0/36.0]
            params['c'] = [[0,0],
                              [1,0],
                              [0,1],
                              [-1,0],
                              [0,-1],
                              [1,1],
                              [-1,1],
                              [-1,-1],
                              [1,-1]]
    return params


#===============================================================================#
#===============================================================================#
#                                    MAIN
#===============================================================================#
#===============================================================================#
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
        print('Error: output directory not provided.')
        sys.exit(2)

    try:
        makedirs(outdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    logfilepath = join(outdir,datetime.strftime('%Y-%m-%d') + '_' + datetime.strftime('%H-%M-%S') + '_2DLBM-simulation' + '.log')

    skipLineToLogFile(logfilepath,'w',True)
    writeLineToLogFile(logfilepath,'a','=====================================================================================',True)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','2D Lattice Boltzmann Method with D2Q9 lattice and Zou/He boundary conditions',True)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Rectangular channel with obstacle',True)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Luca Di Stasio, 2017-2018',True)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','=====================================================================================',True)
    skipLineToLogFile(logfilepath,'a',True)

    logindent = '    '

    # read input file and assign data to variables
    inputFullPath=join(inputdir,inputfile)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Reading input file ' + inputFullPath + ' and assigning data to variables ...',True)
    keys = ['lx','ly','isObstacle','xObstacle','yObstacle','rObstacle','uMax','Re','Tmax','Tsave']
    inputData = parseInput(inputFullPath,keys,'#','##','=')
    writeLineToLogFile(logfilepath,'a','... done.',True)

    # check if input variables exists otherwise throw an error
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Checking if input variables are set ...',True)
    for key in keys:
        if key not in inputData:
            writeErrorToLogFile(logfilefullpath,'a','UNDEFINED INPUT DATA', key + ' is not defined. Error: check the input file for missing data. Terminating program.',True)
            sys.exit(2)
    writeLineToLogFile(logfilepath,'a','... done.',True)

    # set general flow properties
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Setting general flow properties ...',True)
    if inputData['isObstacle']:
        inputData['nu'] = inputData['uMax']*2.0*inputData['rObstacle']/inputData['Re'] # kinematic viscosity
    else:
        inputData['nu'] = inputData['uMax']*inputData['ly']/inputData['Re']            # kinematic viscosity
    inputData['omega'] = 1.0/(3*inputData['nu']+0.5)                                   # relaxation parameter
    writeLineToLogFile(logfilepath,'a','... done.',True)

    # define D2Q9 lattice constants
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','Defining D2Q9 lattice weights, velocities and pairs of opposite velocities ...',True)
    LBMparams = simpleLBMwv(2,9)
    opposites = [1,4,5,2,3,8,9,6,7]
    writeLineToLogFile(logfilepath,'a','... done.',True)

    # summarize simulation parameters
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','SIMULATION PARAMETERS',True)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a','                    Number of cells in x-direction lx = ' + str(inputData['lx']),True)
    writeLineToLogFile(logfilepath,'a','                    Number of cells in y-direction ly = ' + str(inputData['ly']),True)
    writeLineToLogFile(logfilepath,'a','Maximum velocity of Poiseuille flow at the inlet uMax = ' + str(inputData['uMax']),True)
    writeLineToLogFile(logfilepath,'a','                                   Reynolds number Re = ' + str(inputData['Re']),True)
    writeLineToLogFile(logfilepath,'a','                               Kinematic viscosity nu = ' + str(inputData['nu']),True)
    writeLineToLogFile(logfilepath,'a','                           Relaxation parameter omega = ' + str(inputData['omega']),True)
    writeLineToLogFile(logfilepath,'a','                      Total number of iterations Tmax = ' + str(inputData['Tmax']),True)
    writeLineToLogFile(logfilepath,'a','        Cycle time of saving to file operations Tsave = ' + str(inputData['Tsave']),True)
    if inputData['isObstacle']:
      writeLineToLogFile(logfilepath,'a','Obstacle is present:')
      writeLineToLogFile(logfilepath,'a','    Coordinate of obstacle''s center in x-direction xObstacle = ' + str(inputData['xObstacle']),True)
      writeLineToLogFile(logfilepath,'a','    Coordinate of obstacle''s center in x-direction yObstacle = ' + str(inputData['yObstacle']),True)
      writeLineToLogFile(logfilepath,'a','                                 Obstacle''s radius rObstacle = ' + str(inputData['rObstacle']),True)
    else:
      writeLineToLogFile(logfilepath,'a','Obstacle is NOT present',True)

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
