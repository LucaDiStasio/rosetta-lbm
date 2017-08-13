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

from os.path import join
from datetime import datetime
from time import strftime

def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hi:d:w:s:p:',['help','Help',"inputfile", "input","inpdir", "inputdirectory", "idir","workdir", "workdirectory", "wdir","abqonly","preonly"])
    except getopt.GetoptError:
        print('runAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                   ABAQUS PARAMETRIC SIMULATION')
            print(' ')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2017')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('runAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file for abaqus only> -p <preprocessor>')
            print(' ')
            print('Mandatory arguments:')
            print('-i <input deck>')
            print('-d <input directory>')
            print(' ')
            print('Optional arguments:')
            print('-w <working directory>')
            print('-s <status file>')
            print('-p <preprocessor only>')
            print(' ')
            print('Default values:')
            print('-w <working directory>                ===> same as input directory')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-i", "--inputfile", "--input"):
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
                subparts = parts[0].split('_')
                logfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
            else:
                inputfile = arg + '.csv'
                subparts = arg.split('_')
                logfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
        elif opt in ("-d", "--inpdir", "--inputdirectory", "--idir"):
            if arg[-1] != '/':
                inputdir = arg
            else:
                inputdir = arg[:-1]
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]
        elif opt in ("-s", "--abqonly"):
            statusfile = arg
            abqonly = True
        elif opt in ("-p", "--preonly"):
            preonly = True

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'workdir' not in locals():
        workdir = inputdir
    if 'abqonly' not in locals():
        abqonly = False
    if 'preonly' not in locals():
        preonly = False

    if __name__ == "__main__":
        main(sys.argv[1:])
