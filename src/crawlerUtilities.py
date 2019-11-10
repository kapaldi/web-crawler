import re
import requests

from File import close_files


def regex_links(current):
	return re.findall(r"(?<=href=\")https?\S+(?=\")", current)


def get_source(url, files, error_file_written):
	page = attempt_retrieval(url, files)
	if (page.status_code > 400):
		error_file_written = True
		write_error(files[0].file, str(page.status_code), url)
		return [], error_file_written
	else:
		return page.text, error_file_written


def attempt_retrieval(link, files):
	try:
		return requests.get(link)
	except requests.exceptions.RequestException as e:
		print(e)
		close_files(files)
		exit(1)


def write_error(file, error_code, url):
	file.write("ERROR " + str(error_code) + " was reported for url: " + url + "\n")
