#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

#
# Copyright (C) 2000-2005 by Yasushi Saito (yasushi.saito@gmail.com)
# 
# Pychart is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# Pychart is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
from pychart import *
import tocslib
data = [[128, 637], [256, 651], [512, 680], [1024, 737], [2048, 851]]

ar = area.T(x_axis = axis.X(label="Hash map size", 
                            tic_interval=lambda x,y: [128,256,512,1024,2048]),
            y_axis = axis.Y(label="Recovery cost(ms)",
                            tic_interval=lambda x,y: (600,700,800,900,1000)),
            x_grid_interval = 2,
            y_range = (0, 1000),
            x_range = (100, 2400),
            legend = None,
            x_coord = log_coord.T())
ar.add_plot(bar_plot.T(data=data, label=None, data_label_format="/o/7{}%d"))
ar.draw()

