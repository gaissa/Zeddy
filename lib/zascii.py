#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  Module: zascii.py
##  Version: 2015-08-07
##  gaissa <https://github.com/gaissa>

from PIL import Image
from  PIL import ImageOps
import sys

chars = ['.', ',', '^', '.', '*', '+', '/', '%', '9', '&']

def convert(*args):

	x = int(args[0])
	y = int(args[1])

	#print args[2]
	#print args[3]

	# input file
	infilename = args[2]

	# output file
	outfilename = args[3]

	# COMMENT
	resizefile = args[4]

	if x > 155:
		x == 155

	if y > 155:
		y == 155

	#print x
	#print y

	im = Image.open(infilename)
	#im = ImageOps.autocontrast(im, cutoff=0)
	im = ImageOps.grayscale(im)

	im.resize((x,y), Image.ANTIALIAS).save(resizefile, quality=95)

	im = Image.open(resizefile)
	f = open(outfilename, "w")

	for pixelx in range(0, im.size[1]):
		f.write('\n')
		for pixely in range(0, im.size[0]):
			color = im.getpixel((pixely, pixelx))
			if color <= 255 and color >= 253:ch = " "
			elif color <= 253 and color >= 250:ch = " "
			elif color <= 250 and color >= 230:ch = " "
			elif color <= 230 and color >= 210:ch = chars[0]
			elif color <= 210 and color >= 190:ch = chars[1]
			elif color <= 190 and color >= 170:ch = chars[2]
			elif color <= 170 and color >= 150:ch = chars[3]
			elif color <= 150 and color >= 130:ch = chars[4]
			elif color <= 130 and color >= 110:ch = chars[5]
			elif color <= 110 and color >= 90:ch = chars[6]
			elif color <= 90 and color >= 70:ch = chars[7]
			elif color <= 70 and color >= 50:ch = chars[8]
			elif color <= 50 and color >= 30:ch = chars[9]
			elif color <= 30 and color >= 10:ch = "R"
			elif color < 10 and color >= 0:ch = "#"
			else:ch = ""
			f.write(ch)

	f.close()
