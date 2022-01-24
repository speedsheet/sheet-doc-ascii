#!/usr/bin/env python3

def code(item):
	return f'<c>{item}<>'

def table_row(items):
	''' Creates Stash Table Row
	'''

	match (len(items)):
		case 0:
			return ''
		case 1:
			return '<col>' + items[0] + '<>'
		case _:
			return '<col>' + '<><col>'.join(items) + '<>'

def spaced_table_row(items):
	''' Creates Stash Table Row
	'''

	match (len(items)):
		case 0:
			return ''
		case 1:
			return '<col>' + items[0] + ' <>'
		case _:
			return '<col>' + ' <><col>'.join(items) + ' <>'

