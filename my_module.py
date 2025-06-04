"""
TODO: Write the folllowing components

1. load_collection_from_url(url, search_pattern, start_line, end_line, author, origin)


"""


"""
Document metadata:

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

PUNCT = '.,!?;:"\'()[]{}'


class gutenbergParser:
    def __init__(self,url, author, origin, start_line, end_line, search_pattern) -> None:
        self.url = url
        self.author = author
        self.origin = origin
        self.start_line = start_line
        self.end_line = end_line
        self.search_pattern = search_pattern

        # Document Class essentials
        self.title = None
        self.raw_text = self._fetch_raw_text()
        self.main_text = self._get_main_text(text=self.raw_text)
        self.terms = None
        self._filtered_terms = None
        self._stemmed_terms = None
        self._filtered_stemmed_terms = None


        self.documents = None

    
    def _fetch_raw_text(self):
        req = Request(self.url)
        with urlopen(req) as res:
            return(res.read().decode('utf-8'))
        
    def _get_main_text(self, text: str):
        start_marker = "*** START OF THIS PROJECT"
        end_marker = "*** END OF THIS PROJECT"

        start = text.find(start_marker)
        end = text.find(end_marker)

        if start == -1 or end == -1:
            return text.strip()
        
        start = text.index("\n", start) + 1
        return text[start:end].strip()

    def _split_chapters(self, text: str):
        lines = text.splitlines()
        current_title = None
        current_lines = []
        documents = []
        document_id = 0

        for line in lines:
            line_strip = line.strip()
            if line_strip.isupper() and len(line_strip.split()) >= 2:
                if current_title and current_lines:
                    chapter_text = '\n'.join(current_lines).strip()
                    self.terms = self._tokenize(chapter_text)
                    documents.append(Document(
                        document_id=document_id,
                        title=current_title,
                        raw_text=chapter_text,
                        author=self.author,
                        origin=self.origin
                    ))
                    document_id += 1

                #Start new document
                current_title = line_strip
                current_lines = []
            elif current_title:
                current_lines.append(line)

        #last doc
        if current_title and current_lines:
            chapter_text = '\n'.join(current_lines).strip()
            self.terms = self._tokenize(chapter_text)
            documents.append(Document(
                    document_id=document_id,
                    title=current_title,
                    raw_text=chapter_text,
                    author=self.author,
                    origin=self.origin
                ))

        return documents

    def _parse(self):
        header = self.main_text[:1000]
        for line in header.splitlines():
            if line.lower().startswith("author"):
                author = line.split(":", 1)[1].strip()
        


    def _tokenize(self,content : str) -> list[str]:
        #Tokenize
        # Convert text to lower and replace punctuation
        for punct in PUNCT:
            content = content.replace(punct,' ')
        # print(content)
        return [word.lower() for word in content.split() if word]


def load_collection_from_url(url, author, origin, start_line, end_line, search_pattern=None):
    parser = gutenbergParser(url, author, origin, start_line, end_line, search_pattern)
    return parser.documents



