#!/usr/bin/env python3
import csv
from ascii import *
from dataclasses import dataclass
from os.path import join


DATA_DIR = 'data'
ASCII_FILE = 'ascii 032-126-new.csv'
ASCII_PATH = join(DATA_DIR, ASCII_FILE)

code = 196
letter = chr(code)
folded = letter.casefold()
upper = letter.upper()
lower = letter.lower()

print ("")
print (code, letter, folded, upper, lower)
print ("")


with open(ASCII_PATH, 'w') as file:

	dir (file)

	file.write('code, name, folded, description\n')

	for code in range(32, 256):

		character = chr(code)

		if is_unknown(code):
			file.write(str(code) + ',n/a,,\n')
		elif has_case(code):
			file.write(str(code) + ',' + character + ',' + character.casefold() + ',' + to_description(code) + '\n')
		else:
			file.write(str(code) + ',' + character + ',,' + to_description(code) + '\n')

