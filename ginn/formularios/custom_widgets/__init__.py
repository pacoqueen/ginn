#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2020  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

import gi
gi.require_version("Gtk", '3.0')
from gi import pygtkcompat
import os

try:
    from gi import pygtkcompat
except ImportError:
    pygtkcompat = None
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject

if pygtkcompat is not None:
    pygtkcompat.enable()
    pygtkcompat.enable_gtk(version='3.0')
    import gtk
    import gobject

from .velocimetro import Velocimetro
from .starhscale import StarHScale
from .marquee_label import MarqueeLabel
from .cellrendererautocomplete import CellRendererAutoComplete
# Registro la clase como un widget Gtk
gobject.type_register(StarHScale)
gobject.type_register(Velocimetro)
gobject.type_register(MarqueeLabel)
gobject.type_register(CellRendererAutoComplete)

__all__ = ["Velocimetro", "StarHScale", "MarqueeLabel",
           "CellRendererAutoComplete", "Mapamundi"]

