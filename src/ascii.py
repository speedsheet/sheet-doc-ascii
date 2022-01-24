#!/usr/bin/env python3
import csv
from dataclasses import dataclass

def to_codes(string):
	return [ord(character) for character in string]


BASE_A_CODES = to_codes('AÀÁÂÃÄÅaàáâãäå')
BASE_E_CODES = to_codes('EÈÉÊËeèéêë')
BASE_I_CODES = to_codes('IÌÍÎÏiìíîï')
BASE_O_CODES = to_codes('OÒÓÔÖÕoòóôöõ')
BASE_U_CODES = to_codes('UÙÚÛÜuùúûü')
BASE_Y_CODES = to_codes('YÝŸyýÿ')

UPPER_CASE_CODES = to_codes('AÀÁÂÄÃÅEÈÉÊËIÌÍÎÏOÒÓÔÖÕUÙÚÛÜYÝŸ')
LOWER_CASE_CODES = to_codes('àáâäãåèéêëìíîïòóôöõùúûüýÿ')

GRAVE_CODES = to_codes('ÀàÈèÌìÒòÙù')
ACUTE_CODES = to_codes('ÀÁáÉéÍíÓóÚúýÝ')
CIRCUMFLEX_CODES = to_codes('ÂâÊêÎîÔôÛû')
TILDE_CODES = to_codes('ÃãÕõ')
UMLAUT_CODES = to_codes('ÄäËëÏïÖöÜüÿŸ')
RING_CODES = to_codes('Åå')

DIACRITIC_CODES = to_codes("´^`~¨¯")
CURRENCY_CODES = to_codes ('$¢¤£¥')

NEWLINES = [10, 13]
PUNCTUATION = to_codes('…"\'(){}[]--;:,!?.')

CODE_0 = ord('0')
CODE_9 = ord('9')
CODE_LOWER_A = ord('a')
CODE_LOWER_Z = ord('z')
CODE_UPPER_A = ord('A')
CODE_UPPER_Z = ord('Z')

CODE_AT = ord('@')
CODE_BACKSLASH = ord('\\')
CODE_COLON = ord(':')
CODE_DELETE = 127
CODE_EXCLAMATION = ord('!')
CODE_FORWARD_SLASH = ord('/')
CODE_LESS_THAN = ord('<')
CODE_NON_BREAKING_SPACE = 128
CODE_SPACE = ord(' ')
CODE_SPY = 173

CODE_UNKNOWN_1_1 = 128
CODE_UNKNOWN_1_2 = 159
CODE_UNKNOWN_2 = 173


def base_character(code):

	if has_base_a (code):
		return 'a'

	if has_base_e (code):
		return 'e'

	if has_base_i (code):
		return 'i'

	if has_base_o (code):
		return 'o'

	if has_base_u (code):
		return 'u'

	if has_base_y (code):
		return 'y'

	return chr(code)


def between (value, low, high):
	return value >= low and value <= high

def not_empty(value):
	return value != None and value != ''

def value_or_none(value):
	if not_empty(value):
		return value
	return None


def has_base_a (code):
	return code in BASE_A_CODES

def has_base_e (code):
	return code in BASE_E_CODES

def has_base_i (code):
	return code in BASE_I_CODES

def has_base_o (code):
	return code in BASE_O_CODES

def has_base_u (code):
	return code in BASE_U_CODES

def has_base_y (code):
	return code in BASE_Y_CODES


def has_acute(code):
	return code in ACUTE_CODES

def has_circumflex(code):
	return code in CIRCUMFLEX_CODES

def has_grave(code):
	return code in GRAVE_CODES

def has_ring(code):
	return code in RING_CODES

def has_tilde(code):
	return code in TILDE_CODES

def has_umlaut(code):
	return code in UMLAUT_CODES


def has_diacritic(code):
	return (has_acute(code) or
			has_circumflex(code) or
			has_grave(code) or
			has_ring(code) or
			has_tilde(code) or
			has_umlaut(code))


def has_case(code):

	character = chr(code)

	return (character != character.casefold() or
			character != character.upper())

def is_backslash (code):
	return code == CODE_BACKSLASH

def is_control_char (code, name):
	return (code < CODE_SPACE or
			code in [CODE_DELETE, CODE_SPY])

def is_currency (code):
	return code in CURRENCY_CODES

def is_diacritic (code):
	return code in DIACRITIC_CODES

def is_less_than (code):
	return code == CODE_LESS_THAN

def is_letter (code):
	return (between (code, CODE_LOWER_A, CODE_LOWER_Z) or
			between (code, CODE_UPPER_A, CODE_UPPER_Z))

def is_lower_case (code):
	return between (code, CODE_LOWER_A, CODE_LOWER_Z)

	return (between (code, CODE_EXCLAMATION, CODE_FORWARD_SLASH) or
			between (code, CODE_COLON, CODE_AT))

def is_newline (code):
	return code in NEWLINES

def is_non_breaking_space (code):
	return code == CODE_NON_BREAKING_SPACE

def is_number (code):
	return between (code, CODE_0, CODE_9)

def is_punctuation (code):
	return code in PUNCTUATION

def is_space (code):
	return code == CODE_SPACE

def is_upper_case (code):
	return between (code, CODE_UPPER_A, CODE_UPPER_Z)

def is_unknown (code):
	return between (code, CODE_UNKNOWN_1_1, CODE_UNKNOWN_1_2)

def to_bin(code):
	return "{:>08}".format(
		bin(code).removeprefix('0b'))

def to_hex(code):
	return "{:>02}".format(
		hex(code).removeprefix('0x').upper())

def to_description(code):

	character = chr(code).upper()

	if is_space(code):
		return "Space"

	if is_number(code):
		return "Number " + character

	if is_lower_case(code):
		return "Lower Case " + character

	if is_upper_case(code):
		return "Upper Case " + character

	if has_case(code):
		return "Letter " + character

	return character

def to_short_bin(code):
	return bin(code).removeprefix('0b')


@dataclass
class Ascii:

	name: str
	code: int
	description: str
	description_2: str = ''
	caret: str = ''
	escape: str = ''
	link: str = ''

	def is_control_char(self):
		return is_control_char (self.code, self.name.lower)

	def is_number(self):
		return is_number (self.code)

	def is_letter(self):
		return is_letter(self.code)

	def is_punctuation(self):
		return is_punctuation (self.code)

	def is_lower_case(self):
		return is_lower_case (self.code)

	def is_upper_case(self):
		return is_upper_case (self.code)

	@property
	def base_character(self):
		return base_character(self.code)

	@property
	def bin(self):
		return to_bin(self.code)

	@property
	def char(self):
		return chr(self.code)

	@property
	def character(self):
		return chr(self.code)

	@property
	def hex(self):
		return to_hex(self.code)

	@property
	def short_bin(self):
		return to_short_bin(self.code)

