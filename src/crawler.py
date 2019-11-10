import os
import requests
import re

errorFileWritten = False
errorFileName = "../out/crawler-errors.txt"

def regexedLinks(current):
	return re.findall(r"(?<=href=\")https?\S+(?=\")", current)

def uniqueEntries(currentItems, newItems):
	if (len(newItems) == 0):
		return currentItems
	for item in newItems:
		if (item not in currentItems):
			currentItems.append(item)
	return currentItems


def clearAndSetupFile(name, start):
	file = open(name, "w")
	file.truncate(0)
	file.write("Error report for starting URL: " + start + "\n----------\n\n")
	file.close()


def writeError(error_code, start):
	file = open(errorFileName, "a")
	file.write("ERROR " + str(error_code) + " was reported for url: " + start + "\n")
	file.close()

def getSource(start):
	global errorFileName
	global errorFileWritten

	page = attemptRetrival(start)
	if (page.status_code > 400):
		errorFileWritten = True
		writeError(str(page.status_code,), start)
		return []
	else:
		return page.text


def attemptRetrival(link):
	try:
		return requests.get(link)
	except requests.exceptions.RequestException as e:
		print(e)
		exit(1)


def printList(pruned, links):
	if (len(pruned) > 1):
		printRange = min(len(pruned), links + 1)
		print("There were " + str(printRange - 1) + " links found. Below are the links found after crawling:\n")
		for number in range(1, printRange):
			print(str(number) + ": " + pruned[number])
	else:
		print("nothing has been found...")

def crawler(start, links):
	global errorFileWritten

	clearAndSetupFile(errorFileName, start)
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

	if (errorFileWritten):
		print("Some issues were found during crawling. Check \"../out/crawler-errors.txt\" for more details.\n")
	printList(pruned, links)
	return pruned


def main():
	number, start = setup()
	print("Will be crawling starting from " + start + " for " + str(number) + " links.\n\n")
	crawler(start, number)


def setup():
	start = input("Enter starting URL: ")
	validNumber = False
	while (not validNumber):
		try:
			number = int(input("Enter the number of links to be found: "))
			validNumber = True
		except ValueError:
			print("Please re-enter a valid integer for the amount of links to be found.\n")
	clearCommand = 'cls' if os.name == 'nt' else 'clear'
	os.system(clearCommand)
	return number, start


if __name__ == '__main__':
	main()
