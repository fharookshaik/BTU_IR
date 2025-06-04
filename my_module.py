"""
TODO: Write the folllowing components

1. load_collection_from_url(url, search_pattern, start_line, end_line, author, origin)


"""


"""
Document: 

self.document_id = document_id  # Unique document ID
self.title = title  # String containing the title of the document
self.raw_text = raw_text  # String that holds the complete text of the document.
self.terms = terms  # List of terms (strings) in the document.
self._filtered_terms = []  # Holds terms without stopwords.
self._stemmed_terms = []  # Holds terms that were stemmed with Porter algorithm.
self._filtered_stemmed_terms = []  # Terms that were filtered and stemmed.
self.author = author
self.origin = origin

"""

from urllib.request import urlopen, Request
import re
from document import Document

PUNCT = ['.', ',', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '"', "'"]


class gutenbergParser:
    def __init__(self,url, author, origin, start_line, end_line, search_pattern) -> None:
        self.url = url
        self.author = author
        self.origin = origin
        self.start_line = start_line
        self.end_line = end_line
        self.search_pattern = search_pattern

        self._url_text = self._fetch_url_text()
    
    def _fetch_url_text(self):
        req = Request(self.url)
        with urlopen(req) as res:
            return(res.read().decode('utf-8'))
    
    def parse(self):
        pass



def load_collection_from_url(url, author, origin, start_line, end_line, search_pattern):
    parser = gutenbergParser(url, author, origin, start_line, end_line, search_pattern)



