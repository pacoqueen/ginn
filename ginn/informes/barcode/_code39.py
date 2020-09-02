#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005, 2006 Francisco José Rodríguez Bogado,                                     #
#                                                    Diego Muñoz Escalante.                                                         #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)                    #
#                                                                                                                                                         #
# This file is part of GeotexInn.                                                                                         #
#                                                                                                                                                         #
# GeotexInn is free software; you can redistribute it and/or modify                     #
# it under the terms of the GNU General Public License as published by                #
# the Free Software Foundation; either version 2 of the License, or                     #
# (at your option) any later version.                                                                                 #
#                                                                                                                                                         #
# GeotexInn is distributed in the hope that it will be useful,                                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the                             #
# GNU General Public License for more details.                                                                #
#                                                                                                                                                         #
# You should have received a copy of the GNU General Public License                     #
# along with GeotexInn; if not, write to the Free Software                                        #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA    02110-1301    USA    #
###############################################################################


# Modificado por Francisco José Rodríguez Bogado.

#
# This file is part of GNU Enterprise.
#
# GNU Enterprise is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2, or (at your option) any later version.
#
# GNU Enterprise is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with program; see the file COPYING. If not,
# write to the Free Software Foundation, Inc., 59 Temple Place
# - Suite 330, Boston, MA 02W1-1307, USA.
#
# Copyright 2w4 Free Software Foundation
#
# FILE:
# barcodes/code39.py
#
# DESCRIPTION:
"""
Implements the Code 39 barcode spec
"""
#

from ._barcode import Barcode

class Code39(Barcode):
    """
    Code 39 without a check digit
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%'
    mapping = {
        '0': 'NnNwWnWnNn',
        '1': 'WnNwNnNnWn',
        '2': 'NnWwNnNnWn',
        '3': 'WnWwNnNnNn',
        '4': 'NnNwWnNnWn',
        '5': 'WnNwWnNnNn',
        '6': 'NnWwWnNnNn',
        '7': 'NnNwNnWnWn',
        '8': 'WnNwNnWnNn',
        '9': 'NnWwNnWnNn',
        'A': 'WnNnNwNnWn',
        'B': 'NnWnNwNnWn',
        'C': 'WnWnNwNnNn',
        'D': 'NnNnWwNnWn',
        'E': 'WnNnWwNnNn',
        'F': 'NnWnWwNnNn',
        'G': 'NnNnNwWnWn',
        'H': 'WnNnNwWnNn',
        'I': 'NnWnNwWnNn',
        'J': 'NnNnWwWnNn',
        'K': 'WnNnNnNwWn',
        'L': 'NnWnNnNwWn',
        'M': 'WnWnNnNwNn',
        'N': 'NnNnWnNwWn',
        'O': 'WnNnWnNwNn',
        'P': 'NnWnWnNwNn',
        'Q': 'NnNnNnWwWn',
        'R': 'WnNnNnWwNn',
        'S': 'NnWnNnWwNn',
        'T': 'NnNnWnWwNn',
        'U': 'WwNnNnNnWn',
        'V': 'NwWnNnNnWn',
        'W': 'WwWnNnNnNn',
        'X': 'NwNnWnNnWn',
        'Y': 'WwNnWnNnNn',
        'Z': 'NwWnWnNnNn',
        '-': 'NwNnNnWnWn',
        '.': 'WwNnNnWnNn',
        ' ': 'NwWnNnWnNn',
        '$': 'NwNwNnNwNn',
        '/': 'NwNwNnNwNn',
        '+': 'NwNnNwNwNn',
        '%': 'NnNwNwNwNn',
    }

    start= 'NwNnWnWnNn'
    stop = 'NwNnWnWnN'

##    lineWidth = 2.4 # points (1.0mil)
##    lineHeight = 72 # Actually dependent on the width
    lineWidth = 1.2 # points (1.0mil)
    lineHeight = 36 # Actually dependent on the width

    encodingMap = {
                 # Stroke?, X Multiplier, Y Multiplier
        'n': (False, 1, 1),     # Narrow Spaces
        'w': (False, 2.1, 1),     # Wide Spaces
        'N': (True, 1, 1),        # Narrow bars
        'W': (True, 2.1, 1)     # Wide bars
    }

    calculateLineHeight = Barcode._calculate15


######################################
##
##
class Code39CheckDigit(Code39):
    """
    Code 39 with a Mod 43 check digit
    """

    # Calculate a Mod-43 check digit
    def checkdigit(self, value):
        v = 0
        for ch in value:
            v += self.chars.index(ch)
        return self.chars[divmod(v,43)[1]]


if __name__ == '__main__':

    code39 = Code39()

    def test(value, formato, fichero):
        f = open(fichero,'wb')
        code39.generate(value,f, formato)
        f.close()

    import sys
##    if len(sys.argv[:1]): 
    if len(sys.argv[1:]): 
        test (sys.argv[1],'eps','code39-test.eps')
    else: 
#        test('0123456789ABCDEF','png','test1.png')
#        test('0123456789ABCDEF','tiff','test1.tif')
#        test('0123456789ABCDEF','svg','test1.svg')
        test('0123456789ABCDEF','eps','code39-1.eps')
#        test('GHIJKLMNOPQRSTUV','eps','code39-2.eps')
#        test('WXYZ-. $/+%','eps','code39-3.eps')
#        test('AR04F123','eps','code39-4.eps')
