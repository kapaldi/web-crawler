def regexedLinks(current):
	pass


def uniqueEntries(found):
	pass


def main(start):
	current = start
	nextIndexToSearch = 0
	pruned = []
	# len(n) of xs should be accessible in constant time O(1) as length is stored as a field alongside lists in python
	while (len(pruned) < 100):
		found = regexedLinks(current)
		# uniqueEntries(xs) should consume found and empty list - adds unique entry to END of list
		pruned = uniqueEntries(found)
		if (len(pruned) == nextIndexToSearch):
			print("No more sites left to search, terminating process.\n")
		current = pruned[nextIndexToSearch]
		nextIndexToSearch += 1

		'''
		ASSERT(LEN(FOUND) == 0)
		ASSERT(UNIQUE(PRUNE))	
		'''
	return pruned
