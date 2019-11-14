# Web Crawler

Given a `URL` that is well-formed^ and a number of `links`, the crawler returns the links that could be scraped
from the given starting URL. The amount of links returned is either the specified amount or all the links that could be
reached from every single link in the start source page, and every subsequent page, if there is less than the specified
amount.

If there are any malformation of links, the crawler will suggest a more complete URL formation that the user could have
meant to type in. If there are any invalid numbers specified for the amount of links to crawl for, the program will
detect and inform the user to re-enter the amount again.

In addition to the displaying the results to the console, the crawler will generate a copy of the results (if any) and
an error report (if any) as a result of each crawl. The output and error report can be found at `out/crawler-output.txt`
and `out/crawler-errors.txt`.

^ A URL is well-formed and a "valid URL string" if it follows syntax standardised in the "Internet Standard".
(https://tools.ietf.org/html/rfc3986) 

## Uniqueness (A note on uniqueness)

**Uniqueness is based upon "string uniqueness". Even though the URL points to the same page, _currently_ they are still
considered unique ("string unique").**

    http://www.example.com
    https://www.example.com
    http://example.com
    https://example.com

The links above, although are different only on whether they utilise the `www` prefix in the domain name and the
secure https protocol or the standard http protocol, are considered unique.

**Uniqueness is page unique and not domain unique.**

    https://www.example.com/path/to/a
    https://www.example.com/path/to/b
    
The links above are considered unique as they point to different places, as they have different paths, even if they are
part of the same domain.    

## Documentation

### Crawler Functionality: `src/crawler.py`

- `crawler(start, links)`

| Input | Type  | Description                                 |
|-------|-------|---------------------------------------------|
|start  |String |Starting link that will be crawled from.     |
|links  |Integer|The amount of links that will be crawled for.|

| Output | Type  | Description                                                  |
|--------|-------|--------------------------------------------------------------|
|pruned  |[String]|The pruned links resulting from a crawl from the `start` URL.|

#### Preconditions

1. The `start` link is well-formed and a "valid URL string" according to that of the syntax standardised in the
"Internet Standard". (https://tools.ietf.org/html/rfc3986)

2. The `links` provided is a positive integer, including zero. Specifically `links` is an element of the
Natural numbers 'N'.

#### Post-conditions

1. The method will return a list of unique pruned list of all URLs that are accessible from the `start` page and any
subsequent page(s) linked from the `start` page (identified in the "a href" tag), if any.
2. The method will not include the `start` URL as an element of the returned list and will not entertain such cases, as
the `start` will have been considered from the start.

    **Example: A --> B --> ... --> Z --> A (where an 'X --> Y' represents a link that exists on page with URL 'X' to a page
    with url 'Y')**
    
    _Consider the case where the crawler has somehow crawled URL 'A' and has crawled through the path above reaching
    URL 'Z' and is pruning the links on the page with URL 'Z'. The method comes across URL 'A' which it has found, will
    this result in re-searching through the page of URL 'A' and traversing through the same path again?_
    
    Although the page with URL 'Z' has a link to page with URL 'A', among the lists of items linked to in page, the
    method will not consider the 'A' again as it has been previously seen and uniquely added to the list of `pruned`
    items.
    
    This means that any cyclic searches through the same pages, possibly discovering the same links and going through
    the same search path as previous, will never occur.

#### Behaviour

This method handles the main functionality of the program. This means the method delegates tasks, as required, to the
utility methods and ensures:

1. Links are stored uniquely and pruned after each retrieval of each URL source.
2. The correct link is being considered on each iteration.
3. Links that produced an error when retrieving page source are not filtered/searched through.
4. Searching of only the unique links found until there are no more links to consider and/or the required `links` links
are identified and pruned.
5. The output to console for the crawled result is displayed.
6. The files, `crawler-output.txt` and `crawler-errors.txt` are correctly setup and closed when program terminates.

### File Class: `src/File.py`

#### Class Precondition

`file_name` and `file_header` are valid Strings.

#### Class Description

The following is stored in each `File` that is created:

| Item (Input) | Type  | Description                                                 |
|--------------|-------|-------------------------------------------------------------|
|file_name     |String |Stores the file_name specified for creation.                 |
|file_header   |String |Stores the header that will be placed at the top of the file.|

The `File` created, is opened and left open even after completion of its creation, ready to be written too. To finalise
a creation of each file, the class clears each file completely and setups file with the header specified via the
`clear_and_setup_file` method.

NB: If a file, `file_name` already exists, the file will be overwritten and utilised for the creation.

- `create_files(start, error_file_name, output_file_name)`

| Input           | Type  | Description                                                         |
|-----------------|-------|---------------------------------------------------------------------|
|start            |String |Starting link that will be crawled from.                             |
|error_file_name  |String |File name (and if applicable, path) to the error file to be created. |
|output_file_name |String |File name (and if applicable, path) to the output file to be created.|


| Output | Type    | Description                                    |
|--------|---------|------------------------------------------------|
|files   |[File]   |The files resulting from file creation process. |

#### Preconditions
1. `error_file_name` and `output_file_name` are relative paths to the directory where file, name specified as the final
part of the string `__/__/.../name`
(path containing only file name `___.txt` will create file in the current directory), is to be created is a directory
where user executing file has write permissions.
2. File should have type that is writable by the `file.write(...)` command, such as `.txt`.

#### Post-conditions
1. Returns a list of `File`s containing opened, for write, `crawler-errors.txt` and `crawler-output.txt` that has been
cleared and setup as required at indexes 0 and 1 respectively.

#### Behaviour

This method opens and clears the error and output file required for the crawler. The two files are then added to a list
of `files` at index 0 and 1, for error and output respectively, and returned when method terminates.

- `close_files(files)`

| Input | Type   | Description  |
|-------|--------|--------------|
|files  |[File] |List of files. |

| Output | Type    | Description              |
|--------|---------|--------------------------|
|"result" |Boolean |Result of closing file(s).|

#### Precondition

1. `files` is a list of `File`s.

#### Post-condition

1. In the case of successfully closing all files, returns `True` to indicate success.
2. In the case of failing to close ant file, prints a debug message and terminates execution.

#### Behaviour

The method closes all the `files` in the list passed in.

If at any point a file is not closed successfully, the method will terminate the whole program and display a debug
message, otherwise `True` is returned to indicate that all files have been closed successfully.

- `clear_and_setup_file(file, file_header="")`

| Input           | Type | Description                                                      |
|-----------------|------|------------------------------------------------------------------|
|file             |File  |A file to clear and setup.                                        |
|file_header=""   |string  |(Optional) Header to insert into top of file, defaulted with "".|

#### Precondition
1. `file` is opened for write and is a valid file.

#### Post-condition
1. `file` will be cleared and `file_header` will be inserted at the top of the file.
2. `file` will be kept opened.

#### Behaviour

The method will clear the file, via truncation to size 0, and write the header specified at the top.

### Utility Functions: `src/utils/utilities.py`

- `unique_entries(current_items, new_items)`

| Input        | Type  | Description                  |
|--------------|-------|------------------------------|
|current_items |Object |List of current items.        |
|new_items     |Object |List of items to possibly add.|

| Output       | Type   | Description                                |
|--------------|--------|--------------------------------------------|
|current_items |Objects |Resultant list of (possibly) adding objects.|

#### Preconditions

None.

#### Post-condition

1. List of item(s) in `current_item` are unique.
2. Any item(s) not already in `current_item` at the start of the method which are in `new_items` will be added uniquely.

#### Behaviour

This method will add any items that are not already inside `current_items` from `new_items` uniquely into the list of
`current_items`.

- `display_and_write(file, item)`

| Input | Type  | Description                                            |
|-------|-------|--------------------------------------------------------|
|file   |File   |File to be written into.                                |
|item   |String |String to be written into file and outputted to console.|

#### Precondition

1. `file` is a valid open file that is writable.

#### Post-condition

1. `item` will be written to the `file` at the file pointer.
2. `item` will be written to the console as output.
3. `file` will be kept open.

#### Behaviour

Method will write to `file` the item given and also outputs the item onto console.
- `print_list(pruned, links, files)`

- `setup()`

| Output | Type     | Description                 |
|--------|----------|-----------------------------|
|number  |Integer   |Number of links to crawl for.|
|start   |String    |Starting URL for crawler.    |

#### Precondition

None.

#### Post-condition

1. Will return a `start` string.
2. Will return a valid number which is non-negative, including zero. Namely, `number` is an element of the Natural
Number (N).

#### Behaviour

The method will ask for a `start` URL and attempt to retrieve a non-negative integer, which can be zero, as the `number`
of links. After succeeding, the method clears the console to setup for the crawler's output and return `number` and
`start`.

- `clear_console()`

#### Precondition

None.

#### Post-condition

1. Console, from user's perspective, is cleared from previous outputs.

#### Behaviour

The method clears the console, the section visible to the user at the current console window size. This method ensures
it is able to clear the console by using the required command, for the Windows OS and other OSs.

### Crawler Utility Functions: `src/utils/crawler-utilities.py`

- `regex_links(links)`

| Input  | Type  | Description            |
|--------|-------|------------------------|
|source  |String |Source to pattern match.|

| Output | Type    | Description                                                         |
|--------|---------|---------------------------------------------------------------------|
|"links" |[String] |Result of pattern matching, as required, on the source to find links.|

#### Precondition

None.

#### Post-condition

1. Will return a list of matched links using a regular expression pattern match, if any, with the given source.

#### Behaviour

The method will pattern match any URLs in the source in an "<a href=..." tag and return a list containing a list of all
matched URL.

NB1: This method utilises the library "re" which is part of the Python Standard Library.
(https://docs.python.org/3/library/re.html)

NB2: This methods utilises the _non-standard_ library "requests" that must be installed in the environment that this
script is run.

- `get_source(url, files, error_file_written)`

| Input             | Type  | Description                                                   |
|-------------------|-------|---------------------------------------------------------------|
|url                |String |URL to retrieve source from.                                   |
|files              |[File] |List containing error and output files.                        |
|error_file_written |Boolean|Boolean to identify whether the error file has been written to.|

| Output       | Type      | Description                                                   |
|--------------|-----------|---------------------------------------------------------------|
|"page source" |String     |Result of closing file(s).                                     |
|error_file_written|Boolean|Boolean to identify whether the error file has been written to.|

#### Precondition

1. `files` contain error file at `error_file_index` which is opened.

#### Post-condition

1. Will write to error file to report error found with URL if `page_status_code` is considered an error. Will return ""
as `"page_source"` and set `error_file_written` to True. 
2. Will return the `"page_source"` and the `error_file_written` Boolean as passed in.
3. All `File`s in `files` will be kept open.

#### Behaviour

In the case that the status code returned form `attempt_retieval` is not beyond the `html_error_code_starting_point`,
the method returns the retrieved page source as a single String and `the error_file_written` status as is from the
start.

NB: This methods utilises the _non-standard_ library "requests" that must be installed in the environment that this
script is run.

- `attempt_retrieval(link, files)`

| Input | Type  | Description                       |
|-------|-------|-----------------------------------|
|link   |String |Link that will attempt to retrieve.|
|files  |[File] |List of files.                     |

| Output  | Type                    | Description                                                         |
|---------|-------------------------|---------------------------------------------------------------------|
|"result" |requests.models.Response |Response corresponding to the `request` issued for the specified URL.|

#### Preconditions

None.

#### Post-conditions

1. In the case that there is no `requests.exception.RequestException`, the method return a `"result"`. Files will be
kept open in this case.
2. In the case where there is a `requests.exception.RequestException`, the method displays the stack trace, closes all
the files and terminates execution. 

#### Behaviour

The method attempts to request the page found at the `link` provided.

Any exception thrown by the attempt will be
caught and displayed. Then any open `files` is closed and the execution is terminated.

- `write_error(file, error_code_url)`

| Input     | Type   | Description            |
|-----------|--------|------------------------|
|file       |File    |File to write error to. |
|error_code |Integer |Error code.             |
|url        |String  |URL causing the error.  |

#### Precondition

1. `file` is a valid open file that is writable.

#### Post-condition

1. `file` is written to as specified.
2. `file` will be kept open. 

#### Behaviour

`file` is written to with the specified message with the given `error_code` and `url`.

### Constants: `src/lib/constants.py`

#### File Indexes

These are the indexes that the error and output file will be stored at after they are both created in the `create_file`
method in the `src/File.py` class that will be called upon in the main `crawler` method in `src/crawler.py`

- `error_file_index = 0`

The error file will be defined to be stored at index 0.

- `output_file_index = 1`

The output file will be defined to be stored at index 1.

#### Other Constants

- `html_error_code_starting_point = 400`

The boundary for which the HTML error codes start, as specified in section 6 of the 
_"Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content"_.
(https://tools.ietf.org/html/rfc7231)

### Error Output Report: `src/out/crawler-errors.txt`

This file reports upon any errors found in the crawling execution.

Errors are defined as response codes greater than
that of `html_error_code_starting_point`.

Setup is completed when the file is created or cleaned up in the `create_Files` method in `src/File.py`.

This file is written to by the `write_error` method in `src/utils/crawlerUtilities.py`.

### Crawler Output Copy: `src/out/crawler-output.txt`

This file stores a copy of the output of the crawler, as displayed in the console.

Setup is completed when the file is created or cleaned up in the `create_files` method in `src/File.py`.

This file is written to by the `display_and_write` method in `src/utils/utilities.py`.

