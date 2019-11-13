import os

from lib.constants import *


def unique_entries(current_items, new_items):
	if (len(new_items) == 0):
		return current_items
	for item in new_items:
		if (item not in current_items):
			current_items.append(item)
	return current_items


def display_and_write(file, item):
	file.write(item + "\n")
	print(item)


def print_list(pruned, links, files):
	if (len(pruned) > 1):
		print_range = min(len(pruned), links + 1)
		print("There were " + str(print_range - 1) + " links found. Below are the links found after crawling:\n")
		for number in range(1, print_range):
			display_and_write(files[output_file_index].file, str(number) + ": " + pruned[number])
	else:
		display_and_write(files[output_file_index].file, "nothing has been found...")


def setup():
	start = input("Enter starting URL: ")
	valid_number = False
	while (not valid_number):
		try:
			number = int(input("Enter the number of links to be found: "))
			valid_number = True
		except ValueError:
			print("Please re-enter a valid integer for the amount of links to be found.\n")
	clear_command = 'cls' if os.name == 'nt' else 'clear'
	os.system(clear_command)
	return number, start
