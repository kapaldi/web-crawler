import requests
import re

def regexedLinks(current):
	return re.findall(r"(?<=href=\")https?\S+(?=\")", current)

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
		print("ERROR " + str(page.status_code) + " was reported for url: " + start)
		return []
	else:
		return page.text


def printList(pruned, links):
	if (len(pruned) > 1):
		printRange = min(len(pruned), links + 1)
		for number in range(1, printRange):
			print(str(number) + ": " + pruned[number])
	else:
		print("nothing has been found...\n")

def main(start, links):
	current = getSource(start)
	# Added current site into list of pruned links to avoid cyclic cases arising from first link re-linking to itself
	pruned = [start]
	nextIndexToSearch = 1
	'''
		- len(n) of xs should be accessible in constant time O(1) as length is stored as a field alongside lists in python.
		- `links + 1` as (design choice) to avoid cyclic redirects, we will not allow visits back to initial link, thus
			the `start` link is included to not allow the same site to be accessed.
	'''
	while (len(pruned) < links + 1):
		# Catches case for where `getSource` html receives an error from provided url
		if (current != []):
			found = regexedLinks(current)
			# uniqueEntries(xs) should consume `found` and empty list - adds unique entry to END of `pruned` list
			pruned = uniqueEntries(pruned, found)
		if (nextIndexToSearch >= len(pruned)):
			# short-circuit out in cases where no extra links `found` and current list of links exhausted
			print("No more sites left to search, terminating process.\n")
			break
		current = getSource(pruned[nextIndexToSearch])
		nextIndexToSearch += 1

		'''
		ASSERT(LEN(FOUND) == 0)
		ASSERT(UNIQUE(PRUNE))	
		'''
	printList(pruned, links)
	return pruned

main("https://news.ycombinator.com", 100)
