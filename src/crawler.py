import requests


def regexedLinks(current):
	pass


def uniqueEntries(found):
	pass


def getSource(start):
	page = requests.get(start)
	if (page.status_code > 400):
		print("ERROR: " + page.status_code + " was reported.")
		return []
	else:
		return page.text


def main(start):
	current = getSource(start)
	nextIndexToSearch = 0
	pruned = []
	# len(n) of xs should be accessible in constant time O(1) as length is stored as a field alongside lists in python
	while (len(pruned) < 100):
		found = regexedLinks(current)
		# uniqueEntries(xs) should consume `found` and empty list - adds unique entry to END of `pruned` list
		pruned = uniqueEntries(found)
		if (len(pruned) == nextIndexToSearch):
			print("No more sites left to search, terminating process.\n")
			break
		current = getSource(pruned[nextIndexToSearch])
		nextIndexToSearch += 1

		'''
		ASSERT(LEN(FOUND) == 0)
		ASSERT(UNIQUE(PRUNE))	
		'''
	return pruned


main("https://news.ycombinator.com/")
