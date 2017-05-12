#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  Module: zassume.py
##  Version: 2017-12-05
##  gaissa <https://github.com/gaissa>

import random

h = {
	'0': 10,
	'1': 15,
	'2': 30,
	'3': 20,
	'4': 10,
	'5': 5,
	'6': 5,
	'7': 3,
	'8': 2}

a = {
	'0': 25,
	'1': 30,
	'2': 20,
	'3': 10,
	'4': 5,
	'5': 5,
	'6': 2,
	'7': 2,
	'8': 1}

def guesser(weights):

	dist = []

	for x in weights.keys():
		dist += (weights[x] * x)

	return random.choice(dist)
