#!/usr/bin/perl

=begin commment
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

=cut

=head1 NAME

simplee - simple program

=head1 SYNOPSIS

    simple [OPTION]... FILE...

    -v, --verbose  use verbose mode
    --help         print this help message

Where I<FILE> is a file name.

Examples:

    simple /etc/passwd /dev/null

=head1 DESCRIPTION

This is as simple program.

=head1 AUTHOR

Me.

=cut

use strict;
use warnings;

use Getopt::Long qw(:config auto_help);
use Pod::Usage;

exit main();

sub main {

    # Argument parsing
    my $verbose;
    GetOptions(
        'verbose'  => \$verbose,
    ) or pod2usage(1);
    pod2usage(1) unless @ARGV;
    my (@files) = @ARGV;

    foreach my $file (@files) {
        if (-e $file) {
            printf "File $file exists\n" if $verbose;
        }
        else {
            print "File $file doesn't exist\n";
        }
    }

    return 0;
}
