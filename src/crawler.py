from utilities import *
from crawlerUtilities import *

errorFileWritten = False
errorFileName = "../out/crawler-errors.txt"


def crawler(start, links):
	global errorFileWritten

	clear_and_setup_file(errorFileName, start)
	current, errorFileWritten = get_source(start, errorFileName, errorFileWritten)
	# Added current site into list of pruned links to avoid cyclic cases arising from first link re-linking to itself
	pruned = [start]
	next_index_to_search = 1
	'''
		- len(n) of xs should be accessible in constant time O(1) as length is stored as a field alongside lists in python.
		- `links + 1` as (design choice) to avoid cyclic redirects, we will not allow visits back to initial link, thus
			the `start` link is included to not allow the same site to be accessed.
	'''
	while (len(pruned) < links + 1):
		# Catches case for where `getSource` html receives an error from provided url
		if (current != []):
			found = regex_links(current)
			# uniqueEntries(xs) should consume `found` and empty list - adds unique entry to END of `pruned` list
			pruned = unique_entries(pruned, found)
		if (next_index_to_search >= len(pruned)):
			# short-circuit out in cases where no extra links `found` and current list of links exhausted
			print("No more sites left to search, terminating process.\n")
			break
		current, errorFileWritten = get_source(pruned[next_index_to_search], errorFileName, errorFileWritten)
		next_index_to_search += 1

		'''
		ASSERT(LEN(FOUND) == 0)
		ASSERT(UNIQUE(PRUNE))	
		'''

	if (errorFileWritten):
		print("Some issues were found during crawling. Check \"../out/crawler-errors.txt\" for more details.\n")
	print_list(pruned, links)
	return pruned


def main():
	number, start = setup()
	print("Will be crawling starting from " + start + " for " + str(number) + " links.\n\n")
	crawler(start, number)


if __name__ == '__main__':
	main()
