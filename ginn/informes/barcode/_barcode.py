#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005, 2006 Francisco José Rodríguez Bogado,                   #
#                                                    Diego Muñoz Escalante.   #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the             #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
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
# - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2004-2005 Free Software Foundation
#
# FILE:
# barcodes/Base.py
#
# DESCRIPTION:
"""
"""
#
from reportlab.lib import colors  # @UnusedImport
from reportlab.graphics.shapes import *  # @UnusedWildImport
try:
    import Image  # @Reimport ¿?
    import ImageDraw    ## Del PIL    
except ImportError:
    from PIL import Image  # Pillow
    from PIL import ImageDraw


class InvalidBarcode(StandardError):
    pass


class Barcode:
    mapping = {}
    chars = []
    validLengths = []
    lineWidth = 1.44 # points (.02")
    lineHeight = 18 # (.125")
    spacing = ''
    start = ''
    stop = ''
    defaultIncludeText = True

    encodingMap = {
                 # Stroke?, X Multiplier, Y Multiplier
        '0': (False, 1, 1),
        '1': (True, 1, 1),
    }


    def checkdigit(self, value):
        """
        Returns the checkdigit encoding for the given value
        """
        return ''

    def calculateLineHeight(self, width):
        return self.lineHeight

    def _buildBinary(self, value):
        """
        Returns a string of 0s (no line) and 1s (line).
        Note that, depending on the barcode type,
        a single bar could be multiple
        """

        if self.validLengths and len(value) not in self.validLengths:
            raise InvalidBarcode, 'Barcode is not a valid length: Should be one of %s' % self.validLengths

        value = str(value)
        rv = self.start + self.spacing

        first = True
        for ch in value + self.checkdigit(value):
            if first:
                first = False
            else:
                rv += self.spacing
            try:
                rv += self.mapping[ch]
            except KeyError:
                raise InvalidBarcode, 'Barcode cannot contain "%s" character.' % ch

        return rv + self.spacing + self.stop


    ###
    ###
    ###
##    def generate(self, value, stream=None,
##                             format='eps', includeText=None, textSize=7, dpi=300):
    def generate(self, value, stream=None,
                             formato='eps', includeText=None, textSize=14, dpi=300,
                 lineWidth = 1.2, lineHeight = 36):
        """
        Generates the requested bar code either via a stream or as the
        requested object type.

        @param value:     The string to convert to a barcode
        @param stream:    Optional argument of file name as a string, or any
                                        open file style object.
        @param formato: The formato in which the output should be generated.
                                    Valid file formats include pdf, eps, svg and
                                    will require the stream argument be provided.
                                    Valid object formats include
                                    rldrawing (ReportLab Drawing object will be returned,
                                    No stream argument is required).
        @param includeText: Boolean.    If true then human readable text will
                                                be printed centered under the barcode.
        @param textSize: The point size of the human readable text.
        @param dpi: The dots per inch at which the bitmap should be generated.

        @return: None or a formato dependent object.    Valid return values::
                        eps : None
                        pdf : None
                        svg : None
                        rl    : ReportLab Drawing
        @rtype: misc
        """

        assert (formato in ('rl','pil') or stream is not None)

        d = self._generateDrawing(value, includeText, textSize, dpi)

        #
        # Process formats that return value instead of write to a file
        #
        if formato == 'rl':
            return d

        #
        # A stream is required for the remaining formats
        #
        if not hasattr(stream, 'write'):
            closeFile = True
            stream = open(stream,'w')
        else:
            closeFile = False

        if formato == 'pdf':
            from reportlab.graphics import renderPDF
            renderPDF.drawToFile(d, stream, 'GNUe')
        elif formato == 'eps':
            from reportlab.graphics import renderPS
            renderPS.drawToFile(d, stream)
        elif formato == 'svg':
            from reportlab.graphics import renderSVG
            renderSVG.drawToFile(d, stream)
##        elif formato in ('png','tiff'):
##            from reportlab.graphics import renderPM
##            renderPM.drawToFile(d, stream,formato.upper(), dpi=dpi)
##        elif formato in ('pil',):
##            from reportlab.graphics import renderPM
##            return renderPM.drawToPIL(d, dpi=dpi)


#
# This code *should* be replaced with calls to renderPM
# but that appears broken in the .debs
#
        ##
        ## Raster-based output using PIL
        ##
        elif formato in ('png','tiff','ppm','xbm'):

            code = value     ##
        
            lineWidth = int(lineWidth * dpi/72+.5)     # 300dpi
            lineHeight = int(lineHeight * dpi/72+.5)    # 300dpi
            # Special case for PostNet
            lineHeight2 = int(lineHeight * .45+.5)

            # Create a new monochrome image with a white backgint
            image = Image.new('1',(int(len(code)*lineWidth+.5),
                 int(lineHeight+.5)), 1)
            draw = ImageDraw.Draw(image)
            offs = 0
            for ch in code:
                if ch == '1':
                    draw.rectangle((offs,0,offs+lineWidth-1,lineHeight),
                                                    outline=0, fill=0)
                # Special case for PostNet
                elif ch == '2':
                    draw.rectangle((offs,0,offs+lineWidth-1,lineHeight2),
                                                    outline=0, fill=0)
                offs += lineWidth

            image.save(stream, formato)

        if closeFile:
            stream.close()

##    def _generateDrawing(self, value, includeText=None, textSize=7, dpi=300):
    def _generateDrawing(self, value, includeText=None, textSize=14, dpi=300):
        """
        Generates a ReportLab Drawing object used by the renderers in generate()

        @param value:     The string to convert to a barcode
        @param includeText: Boolean.    If true then human readable text will
                                                be printed centered under the barcode.

        @param textSize: The point size of the human readable text.
        @param dpi: The dots per inch at which the bitmap should be generated.

        @return: ReportLab Drawing
        @rtype: misc
        """

        if includeText is None:
            includeText = self.defaultIncludeText
        code = self._buildBinary(value)
        lineWidth = self.lineWidth
        try:
            spaceWidth = self.spaceWidth
        except:
            spaceWidth = lineWidth

        width = 0
        for ch in code:
            stroke, xmul, ymul = self.encodingMap[ch]
            if stroke:
                width += lineWidth*xmul
            else:
                width += spaceWidth*xmul

        lineHeight = self.calculateLineHeight(width)

        d = Drawing(width+1,lineHeight+(includeText and ( textSize+2 ) or 1 ))

        if includeText:
            y = textSize + 1
        else:
            y = 0

        # Draw each bar
        x = 0
        for ch in code:
            stroke, xmul, ymul = self.encodingMap[ch]
            dx = lineWidth*xmul
            dy = lineHeight*ymul
            if stroke:
                # So we won't cut off half the first bar...
                if not x:
                    x = dx/2.0

                d.add(Line(x+dx/2, y, x+dx/2, y+dy, strokeColor=colors.black,strokeWidth=dx))

                x += dx
            else:
                x += spaceWidth*xmul

        # Draw the text
        if includeText:
            d.add(String(x/2.0, (textSize/2.0) - 2, value, fontSize=textSize, fontName="Courier",fillColor=colors.black,textAnchor="middle"))
##            d.add(String(x/2.0, textSize/2.0, value, fontSize=textSize, fontName="Courier",fillColor=colors.black,textAnchor="middle"))

        return d

    # Line height is .15 * barcode width, but at least .25"
    # This is used by Code39, Interleaved 2 of 5, etc
    def _calculate15(self, width):
        return max(18, .15 * width)
