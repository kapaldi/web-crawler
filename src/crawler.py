from File import create_files
from utils.utilities import *
from utils.crawlerUtilities import *

errorFileName = os.path.join(os.path.dirname(__file__), "../out/crawler-errors.txt")
output_file_name = os.path.join(os.path.dirname(__file__), "../out/crawler-output.txt")


def crawler(start, links):
	error_file_written = False

	files = create_files(start, errorFileName, output_file_name)
	current, error_file_written = get_source(start, files, error_file_written)
	pruned = [start]
	next_index_to_search = 1
	while (len(pruned) < links + 1):
		if (current != ""):
			found = regex_links(current)
			pruned = unique_entries(pruned, found)
		if (next_index_to_search >= len(pruned)):
			print("No more sites left to search, terminating process.\n")
			break
		current, error_file_written = get_source(pruned[next_index_to_search], files, error_file_written)
		next_index_to_search += 1
	if (error_file_written):
		print("-> Some issues were found during crawling. Check \"../out/crawler-errors.txt\" for more details.")
	print("-> Check \"../out/crawler-output.txt\" for a copy of the crawled output.\n")
	print_list(pruned, links, files)
	close_files(files)
	return pruned


def main():
	number, start = setup()
	print("Will be crawling starting from " + start + " for " + str(number) + " links.\n\n")
	crawler(start, number)


if __name__ == '__main__':
	main()
