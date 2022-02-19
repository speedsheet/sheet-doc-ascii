#!/usr/bin/env python3
import csv
from ascii import *
from dataclasses import dataclass
from os.path import join
from stash import *


DATA_DIR = "../data"
CONTROL_CHARS_FILE = 'ascii 000-031.csv'
ASCII_CHARS_FILE = 'ascii 032-126.csv'

CONTROL_CHARS_PATH = join(DATA_DIR, CONTROL_CHARS_FILE)
ASCII_CHARS_PATH = join(DATA_DIR, ASCII_CHARS_FILE)

STASH_PATH = "../ascii.stash"
STASH_TABLE_PATH = "../ascii-table.stash"


CONTROL_FIELD_CODE = 0
CONTROL_FIELD_NAME = 1
CONTROL_FIELD_CARET = 2
CONTROL_FIELD_ESCAPE = 3
CONTROL_FIELD_DESCRIPTION = 4
CONTROL_FIELD_DESCRIPTION_2 = 5
CONTROL_FIELD_LINK = 6

ASCIIS_FIELD_CODE = 0
ASCIIS_FIELD_NAME = 1
ASCIIS_FIELD_DESCRIPTION = 3
ASCIIS_FIELD_DESCRIPTION_2 = 4
ASCIIS_FIELD_LINK = 5

ASCII_DOC_START = '''# <#>ASCII<> SpeedSheet
<b>Find what you need, faster.<>


### Search For It

This is a searchable ASCII table.
Use search to find what you need.

<card><table><col><b>Need This?		<><><col><b>Search For:		<><><col><b>See Search In Action:<><>
<col> <>
<col>Letter A<><col><c>/<v>a<><><><col><l /s/ascii?search=%2Fa>/a<><>
<col>by ASCII Code<><col><c><v>65<><><><col><l /s/ascii?search=65>65<><>
<col>by ASCII Hex<><col><c>#<v>41<><><><col><l /s/ascii?search=%2341>#41<><>
<col> <><col><c>0x<v>41<><><><col><l /s/ascii?search=0x41>0x41<><>
<col> <>
<col>All Forms of A<><col><c>base-<v>a<><><><col><l /s/ascii?search=base-a>base-a<><>
<col> <>
<col>Numbers<><col><c>numbers<><><col><l /s/ascii?search=numbers>numbers<><>
<col>Punctuation<><col><c>punctuation<><><col><l /s/ascii?search=punctuation>punctuation<><>
<col> <>
<col>Help<><col><c>help<><><col><l /s/ascii?search=help>help<><><><>



'''

ASCII_TABLE_DOC_START = '''# <#>ASCII Table<> SpeedSheet
<b>Find what you need, faster.<>

A searchable ASCII table.


'''

DOC_END = '''# Newline

<b>Windows:<>

<in-2><c>\\\\n\\\\r

Dec: 10, 13
Hex: 0A, 0D<><>

<b>Mac / Linux:<>

<in-2><c>\\\\n

Dec: 10
Hex: 0A<><>
@
@ EOL, end of line, nl


# Help

Use these search terms / formats to find something specific.

<b>Letter:<>

<in-2>/<v>x<>
char-<v>x<><>

<b>Hex:<>

<in-2>\#<v>FF<>
0x<v>FF<><>

<b>Base Letters:<>

<in-2>base-a, vowels
base-e, vowels
base-i, vowels
base-o, vowels
base-u, vowels
base-y<>

<b>Accented Letters:<>

<in-2>accented

<table><col>acute<><col>´<>
<col>circumflex<><col>^<>
<col>grave<><col>`<>
<col>ring<><col>˚<>
<col>tilde<><col>~<>
<col>umlaut<><col>¨<><><>

<b>Others:<>

<in-2>accents
alphabet
brackets
control character
currencies
diacritic
digits
numbers
math
punctuation
symbols<>
@
@ tips, tricks, help, search terms

'''


def read_list_item(list, index):

	if index < len (list):
		return list[index]
	return ''

def read_csv_file(file_name):

	with open(file_name) as file:
		reader = csv.reader(file)
		header = next(reader)
		return [row for row in reader]

def read_asciis():

	return to_ascii_items(
		read_csv_file(ASCII_CHARS_PATH))

def read_controls():

	return to_control_ascii_items(
		read_csv_file(CONTROL_CHARS_PATH))

def show_ascii(ascii):

	for item in sorted_ascii:
		if item.is_control_char():
			print(f'{item.code:>3}  {item.hex:>2}  {item.bin:>08}  {item.name:<3}  {item.escape:<2}  {item.caret:<2}  {item.description:<30}  {item.link}')
		else:
			print(f'{item.code:>3}  {item.hex:>2}  {item.bin:>08}  {item.name:<3}  {item.description:<30}  {item.description_2:<30}  {item.link}')

def to_ascii(item):

	return Ascii(
		name = item[ASCIIS_FIELD_NAME],
		code = int(item[ASCIIS_FIELD_CODE]),
		description = read_list_item(item, ASCIIS_FIELD_DESCRIPTION),
		description_2 = read_list_item(item, ASCIIS_FIELD_DESCRIPTION_2),
		link = read_list_item(item, ASCIIS_FIELD_LINK))

def to_ascii_items(data):

	return [to_ascii(item) for item in data]

def to_char(item):
	if is_backslash(item.code) or is_less_than(item.code):
		return '\\' + item.char

	return item.char

def to_control_ascii(item):

	return Ascii(
		name = item[CONTROL_FIELD_NAME],
		code = int(item[CONTROL_FIELD_CODE]),
		description = item[CONTROL_FIELD_DESCRIPTION],
		description_2 = item[CONTROL_FIELD_DESCRIPTION_2],
		escape = item[CONTROL_FIELD_ESCAPE],
		caret = item[CONTROL_FIELD_CARET],
		link = item[CONTROL_FIELD_LINK])

def to_control_ascii_items(data):

	return [to_control_ascii(item) for item in data]

def to_stash_tag(item):

	tag = '#' + item.hex + ', 0x' + item.hex + ', ' + item.bin + ', ' + item.short_bin
	code = item.code

	if has_base_a(code):
		tag += ', base-a, -a, vowels'
	if has_base_e(code):
		tag += ', base-e, -e, vowels'
	if has_base_i(code):
		tag += ', base-i, -i, vowels'
	if has_base_o(code):
		tag += ', base-o, -o, vowels'
	if has_base_u(code):
		tag += ', base-u, -u, vowels'
	if has_base_y(code):
		tag += ', base-y, -y'

	if has_diacritic(code):
		tag += ', accented'

	if has_acute(code):
		tag += ', ' + item.base_character + '-acute , acute, ´'
	if has_circumflex(item.code):
		tag += ', ' + item.base_character + '-circumflex , circumflex, ^'
	if has_grave(code):
		tag += ', ' + item.base_character + '-grave , grave, `'
	if has_ring(code):
		tag += ', ' + item.base_character + '-ring , ring, ˚'
	if has_tilde(code):
		tag += ', ' + item.base_character + '-tilde , tilde, ~'
	if has_umlaut(code):
		tag += ', ' + item.base_character + '-umlaut , umlaut, ¨'

	if is_letter(code):
		tag += ', alphabet, letters'

	if is_backslash(code):
		tag += ', \\\\\\\\'

	if is_currency(code):
		tag += ', currencies, currency, moneys'

	if is_diacritic(code):
		tag += ', diacritics, accents'

	if is_digit(code):
		tag += ', digits'

	if is_math(code):
		tag += ', maths, mathematics'

	if is_number(code):
		tag += ', numbers'

	if item.is_punctuation():
		tag += ', punctuation'

	if item.is_symbol():
		tag += ', symbols'

	if item.is_control_char():
		tag += ', control characters'
	elif not is_unknown(code) and not is_space(code):
		tag += ', character-' + to_name(item) + ', char-' + to_name(item) + ', c-' + to_name(item) + ', /' + to_name(item)

	if is_newline(code):
		tag += ', newline, nl'

	if not_empty(item.caret):
		tag += ', ' + item.caret
	if not_empty(item.escape):
		tag += ', ' + '\\\\' + item.escape

	return tag

def to_name(item):
	if is_backslash(item.code):
		return '\\\\'

	if is_non_breaking_space(item.code):
		return ''

	return item.name

def to_stash_entry(item):

	if item.is_control_char():
		entry = f'# {item.code} {to_name (item)} - {item.description}\n\n'
	elif is_unknown (item.code):
		entry = f'# {item.code}\n\n'
	elif is_non_breaking_space (item.code):
		entry = f'# {item.code} - {item.description}\n\n'
	else:
		entry = f'# {item.code} {to_char (item)} - {item.description}\n\n'

	if not_empty(item.description):
		entry += item.description + '\n'
	if not_empty(item.description_2):
		entry += '\n'.join(item.description_2.split(' / ')) + '\n'

	entry += '\n'

	entry += '<table>'

	if item.is_control_char():
		entry += table_row(['Name', item.description])
	else:
		entry += table_row(['Character', to_char (item)])
	entry += '\n' + table_row(['Decimal', code(str(item.code))])
	entry += '\n' + table_row(['Hex', code(item.hex)])
	entry += '\n' + table_row(['Bin', code(item.bin)])

	if not_empty(item.caret):
		entry += '\n' + table_row(['Caret', code(item.caret)])
	if not_empty(item.escape):
		entry += '\n' + table_row(['Escape', code('\\\\' + item.escape)])
	if not_empty(item.link):
		entry += '\n<col> <>\n'
		entry += table_row(['More', '<l>'+ item.link + '<>'])
	entry += '\n<>\n'
	entry += '@\n@ ' + to_stash_tag(item)
	if item.description_2:
		entry += '\n@ ' + item.description_2

	entry += '\n\n\n'

	return entry

def to_stash_table(item):
	""" Creates entries and formatted headings
		the headings section needs spaces between column values to display correctly (sidebar view).
	"""

	entry = '#### <table>'
	entry += spaced_table_row([code(f'{str(item.code):>3}'), code(item.hex), code(item.bin)])

	if item.is_control_char():
		entry += spaced_table_row([code(f'{to_name(item):3}'), item.description])
	elif is_non_breaking_space (item.code):
		entry += spaced_table_row([code('   '), item.description])
	elif is_unknown(item.code):
		entry += spaced_table_row([''])
	else:

		if is_backslash(item.code):
			character = f'{to_char (item):4}'	# Pad wider for escaped backslash (\\).
		else:
			character = f'{to_char (item):3}'

		if not_empty(item.description_2):
			description = item.description + ' / ' + item.description_2
		else:
			description = item.description
			
		entry += spaced_table_row([code(character), description])

	entry += '<>\n@ ' + to_stash_tag(item)

	entry += '\n'

	return entry

def write_to_stash(asciis):

	with open(STASH_PATH, 'w') as file:

		file.write(ASCII_DOC_START)

		for item in asciis:
			file.write(to_stash_entry(item))

		file.write(DOC_END)

def write_to_stash_table(asciis):

	with open(STASH_TABLE_PATH, 'w') as file:

		file.write(ASCII_TABLE_DOC_START)

		for item in asciis:
			file.write(to_stash_table(item))

		file.write(DOC_END)


def generate():

	print ("")
	print ("Reading Control Data...")
	controls = read_controls()

	print ("Reading Ascii Data...")
	asciis = read_asciis()

	print ("Sorting...")
	sorted_asciis = sorted(controls + asciis, key = lambda x: x.code)

	print ("Writing Ascii...")
	write_to_stash(sorted_asciis)

	print ("Writing Ascii Table...")
	write_to_stash_table(sorted_asciis)

	print ("")
	print ("Done.")
	print ("")


