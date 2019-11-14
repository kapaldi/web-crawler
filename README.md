# Web Crawler

This crawler, starting from the inputted `start` URL, crawls each page found for unique links found in each page that is
linked in each page the crawler traverses. For each page, the crawler prunes out all the links in the page, adds any
newly found link(s) that were not previously discovered and continues pruning the next page to prune from the list of
pages discovered from the crawl.

The result of the crawl is a list of all unique links that are found through the process. The amount of links reported
is either the specified amount or, if not able to find as many, all the links found from the crawl from `start`.

The result is displayed on the user's console and also a copy of the crawled result is provided at
`out/crawler-output.txt`. If there were any request errors, that are recoverable, the crawl will continue - skipping
over the problematic URL -  but reporting the URL and the error code received. The errors will collate in an error
report that can be found at `out/crawler-errors.txt`.

**For more technical detail on the different methods and the crawler, take a look at `doc/documentation.md`.**

Otherwise, below is a brief _how to use the crawler._

**HAPPY CRAWLING!**

## I/O

### Inputs

Running `src/crawler.py` will ask for the following:

- Enter starting URL:

    **Enter the required URL to crawl from.**

    This should be in a form similar to the following:

    `https://www.example.com/path/to/page/if/any`

- Enter the number of links to be found:

    **Enter the number of links to crawl for.**

    This should be a **positive integer, including zero**.

### Outputs

**The result of a successful crawl will be either:**

1. Unique links, of which there are the specified number, are displayed in console.
2. Unique links, of which there are less than the specified number, are displayed in console.

In the case of 2, this is due to the fact that no other unique links could be discovered in the crawl from the provided
start point to the amount specified.

In both cases, a copy of the output is provided at `out/crawler-outoput.txt` and an error report, if any - indicated by
an console message:

_"-> Some issues were found during crawling. Check "../out/crawler-errors.txt" for more details.",_

is provided at `out/crawler-errors.txt`.

The result of an unsuccessful crawl will output an error stack trace in console which can be helpful for debugging
and/or identifying possible user errors.

## Prerequisite(s)

1. As the crawler utilises the `requests` library, which is non-standard. This must be installed for the environment in
which this program is being run.

_For a guide of how to install this library, consult:_

To install Python modules (in this case, replace "somePackage" with requests).

_https://docs.python.org/3/installing/index.html_

For a guide of how to install requests (exact command) and functionality details.

https://realpython.com/python-requests/

2. Python 3 is used.
(Tested and developed for Python 3. Not verified working for Python 2.)

## Operation

Given that the prerequisite(s) have been met:

1. Run the main script `src/crawler.py`

    For example with commands (dependent on setup) from the `src` directory:

    `python crawler.py`

    or

    `python3 crawler.py`

2. Check outputs on console and `out/crawler-output.txt` as well as error report at `out/crawler-errors.txt` if
applicable.

NB: Errors may be raised in the form of a stack trace displayed in console but program should not
terminate with errors not caught.

## Next steps

- Concurrent crawling on links found

    Instead of iteratively crawling, one link at a time, through the list of unique links, execution could be sped up
    if the crawling would be done in parallel each unique link in list until the amount required is found.

- Addition of `pytest` testing to provide robustness

- Extra error handling for specific HTML status code returned such that program does not terminate for certain errors
that are in the 400+ status code range (for example the "too many requests" with status code of 429).
