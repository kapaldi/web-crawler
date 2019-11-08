import requests
import re

def regexedLinks(current):
	return re.findall(r"https?\S+(?=\")", current)

def uniqueEntries(currentItems, newItems):
	if (len(newItems) == 0):
		return currentItems
	for item in newItems:
		if (item not in currentItems):
			currentItems.append(item)
	return currentItems

def getSource(start):
	page = requests.get(start)
	if (page.status_code > 400):
		print("ERROR: " + page.status_code + " was reported.")
		return []
	else:
		return page.text


def printList(pruned):
	for item in pruned:
		print(item + "\n")


def main(start):
	current = getSource(start)
	# Added current site into list of pruned links to avoid cyclic cases arising from first link re-linking to itself
	pruned = [start]
	nextIndexToSearch = 1
	# len(n) of xs should be accessible in constant time O(1) as length is stored as a field alongside lists in python
	while (len(pruned) < 100):
		found = regexedLinks(current)
		# uniqueEntries(xs) should consume `found` and empty list - adds unique entry to END of `pruned` list
		pruned = uniqueEntries(pruned, found)
		if (len(pruned) == nextIndexToSearch):
			print("No more sites left to search, terminating process.\n")
			break
		current = getSource(pruned[nextIndexToSearch])
		nextIndexToSearch += 1

		'''
		ASSERT(LEN(FOUND) == 0)
		ASSERT(UNIQUE(PRUNE))	
		'''
	printList(pruned)
	return pruned


main("https://news.ycombinator.com")
