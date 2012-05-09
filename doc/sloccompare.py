#!/usr/bin/env python
# SLOC Compare
# A tool for visual processing of sloccount(1) output, based on pygame
# Copyright (C) 2003 Josef Spillner <josef@ggzgamingzone.org>
# Published under the GNU GPL

import pygame, pygame.transform, pygame.image
from random import *
from math import *
from pygame.locals import *
from Numeric import *

import sys
import re

RES = array((800, 600))

do_index = 1

def parseslocs(args):
	lines = []
	for arg in args:
		f = file(arg, "r")
		lines.append(f.readlines())
		f.close()

	slocmode = 0
	counter = 0
	sizes = {}
	modules = {}
	oldarg = ""
	for chunk in lines:
		counter = counter + 1
		for line in chunk:
			line = line.rstrip()
			if line[0:5] == "SLOC " or line[0:5] == "SLOC\t":
				slocmode = 1
				sizes[counter] = {}
			elif slocmode == 1 and line == "":
				slocmode = 0
			elif slocmode == 1:
				line = re.sub("\ +", " ", line)
				args = line.split(" ")
				if len(args) == 2:
					languages = args[1].split(",")
					for lang in languages:
						sizes[counter][oldarg].append(lang)
				else:
					languages = args[2].split(",")
					sizes[counter][args[1]] = []
					for lang in languages:
						if not lang == "":
							sizes[counter][args[1]].append(lang)
					oldarg = args[1]
					modules[oldarg] = 1

	for key in sizes.keys():
		for m in modules.keys():
			if not sizes[key].has_key(m):
				sizes[key][m] = ['(none)']

	return sizes

def main():
    pygame.init()
    pygame.display.set_caption("SLOC Compare")

    screen = pygame.display.set_mode(RES, 0, 24)
    water = pygame.Surface((RES[0], RES[1]), 0, 24)

    font = pygame.font.Font(None, 16)

    sizes = parseslocs(sys.argv)

    colors = {}
    colors[1] = (0, 0, 255)
    colors[2] = (255, 0, 255)
    colors[3] = (0, 100, 255)
    colors[4] = (255, 100, 255)
    colors[5] = (0, 200, 255)
    colors[6] = (255, 200, 255)
    colors[7] = (0, 255, 255)
    colors[8] = (255, 255, 255)

    xbase = 0
    for key in sizes.keys():
        xbase = xbase + 1
        xoffset = 0
        sloc = sizes[key]
        keylist = sloc.keys()
        keylist.sort()
        for module in keylist:
            stats = 0
            for lang in sloc[module]:
                if not lang == "(none)":
                    stats = stats + int(lang.split("=")[1])

            x = xbase * 5 + xoffset
            #y = stats / 2000
            y = stats / 150
            water.fill(colors[xbase], ([x, RES[1] - 100 - y, 5, y]))
            if xbase == 1:
                flood = font.render(module, 0, (255, 255, 255))
                water.blit(flood, (x, RES[1] - 100 + (xoffset % 2) * 10))
            xoffset = xoffset + 51
        if do_index:
            water.fill(colors[xbase], ([10, xbase * 25, 20, 20]))

    while 1:
        pygame.event.pump()

        keyinput = pygame.key.get_pressed()

        if keyinput[K_ESCAPE] or pygame.event.peek(QUIT):
            return

        screen.blit(water, (0, 0))

        pygame.display.update()

if __name__ == '__main__': main()

