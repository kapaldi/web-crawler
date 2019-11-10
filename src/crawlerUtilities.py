import re
import requests


def regex_links(current):
	return re.findall(r"(?<=href=\")https?\S+(?=\")", current)

def get_source(url, error_file_name, error_file_written):
	page = attempt_retrival(url)
	if (page.status_code > 400):
		error_file_written = True
		write_error(error_file_name, str(page.status_code), url)
		return [], error_file_written
	else:
		return page.text, error_file_written


def attempt_retrival(link):
	try:
		return requests.get(link)
	except requests.exceptions.RequestException as e:
		print(e)
		exit(1)


def write_error(error_file_name, error_code, url):
	file = open(error_file_name, "a")
	file.write("ERROR " + str(error_code) + " was reported for url: " + url + "\n")
	file.close()
