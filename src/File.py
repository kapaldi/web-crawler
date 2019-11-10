class File:
	def __init__(self, file_name, file_header):
		self.file_name = file_name
		self.file = open(file_name, "w")
		clear_and_setup_file(self.file, file_header)


def create_files(start, error_file_name, output_file_name):
	files = []
	divider = "\n----------\n\n"
	files.append(File(error_file_name, "Error report for crawler.\nStarting URL: " + start + divider))
	files.append(File(output_file_name, "Crawling results for " + start + divider))
	return files


def close_files(files):
	for index in range(0, len(files)):
		files[index].file.close()


def clear_and_setup_file(file, file_header=""):
	file.truncate(0)
	file.write(file_header)
