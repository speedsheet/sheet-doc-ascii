#!/usr/bin/env python3

from shared import *
from re import match
from re import search
from re import split

FILE_1 = "../ascii.stash"
FILE_2 = "../ascii_table.stash"


# Functions ────────────────────────────────────────────── #

def add_binary_literal(line):
	number = get_number(line)
	split_point = get_binary_split_point(line)

	insert = f"0b{number:b}"

	if number < 128:
		insert = f"0b{number:08b}, " + insert
	
	return line[:split_point] + ", " + insert + line[split_point:]


def add_decimal_literal(line):

	number = get_number(line)

	insert = f"0d{number}"

	if number < 100:
		insert += f", 0d{number:03}"

	split = line.split(",", 1)
	return split[0] + ", " + insert + "," + split[1]


def add_number(line):
	number = get_number_from_hex(line)
	return f"@ {number:03}, {line[2:]}"


def contains(value, matcher):
	return match(matcher, value) is not None


def file_name(path):
	return path.split("/")[1]


def get_binary_split_point(line):
	match = search(r"\d{8}, \d+", line)
	return match.end()


def get_number(line):
	number = line.split(" ", 2)[1]
	return int(number[:-1]) 


def get_number_from_hex(line):
	number = line.split(" ", 2)[1]
	return int(number[1:-1], 16) 


def is_hex_tag_line(line):
	return contains(line, r"@ #[\da-fA-F]{2}, ")


def is_number_tag_line(line):
	return contains(line, r"@ \d{3}, ")


def not_number_tag_line(line):
	return not is_number_tag_line(line)


def process_file(path):

	lines = read_lines(path)
	updated = []

	for line in lines:
		updated.append(process_line(line))

	write_lines(path, updated)


def process_file_main(path):

	print(file_name(path), ": Processing...")

	process_file(path)

	print(file_name(path), ": Complete")
	print()


def process_line(line):
	
	if is_hex_tag_line(line):
		line = add_number(line)
	
	if is_number_tag_line(line):
		line = add_decimal_literal(line)
		line = add_binary_literal(line)

	return line


def split_on_first(line):
	return line.split(",", 1)


def split_on_binary(line):
	return split(r"\d{8}, \d+", line)

# Tests ────────────────────────────────────────────────── #

def test_op(name, function, value, expected):

	try:
		actual = function(value)
		result = "good ✓" if (actual == expected) else f"fail ❌ - Expected {expected}, Found {actual}"
		print(f"{name:20}  {result}")
	except Exception as exception:
		print(f"{name:20}  Error ❌  - {exception.args[0]}")

def test_ops():

	test_op("Is Number Tag Line", is_number_tag_line, "@ 002, #02, 0x02, 00000010, 10, control characters, ^B", True)
	test_op("Is Number Tag Line", is_number_tag_line, "@ #CD, 0xCD, 11001101, 11001101, base-i, -i, vowels, accented, i-acute , acute, ´, character-Í, char-Í, c-Í, /Í", False)
	test_op("Is Number Tag Line", is_number_tag_line, "@", False)

	test_op("Is Hex Tag Line", is_hex_tag_line, "@ #CD, 0xCD, 11001101, 11001101, base-i, -i, vowels, accented, i-acute , acute, ´, character-Í, char-Í, c-Í, /Í", True)
	test_op("Is Hex Tag Line", is_hex_tag_line, "@ 002, #02, 0x02, 00000010, 10, control characters, ^B", False)
	test_op("Is Hex Tag Line", is_hex_tag_line, "@", False)

	test_op("add_binary_literal", add_binary_literal, "@ 002, 0d2, 0d002, #02, 0x02, 00000010, 10, control characters, ^B", "@ 002, 0d2, 0d002, #02, 0x02, 00000010, 10, 0b00000010, 0b10, control characters, ^B")
	test_op("add_decimal_literal", add_decimal_literal, "@ 002, #02, 0x02, 00000010, 10, control characters, ^B", "@ 002, 0d2, 0d002, #02, 0x02, 00000010, 10, control characters, ^B")
	test_op("add_number", add_number, "@ #CD, 0xCD, 11001101, 11001101", "@ 205, #CD, 0xCD, 11001101, 11001101")


# Main ─────────────────────────────────────────────────── #

print()
process_file_main(FILE_1)
process_file_main(FILE_2)
# test_ops()







