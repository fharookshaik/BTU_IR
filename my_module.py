"""
TODO: Write the folllowing components

[x]1. load_collection_from_url(url, search_pattern, start_line, end_line, author, origin)
[ ]2. Handle Data Processing - Stopword Elimination, Stemming, Tokenization
[ ]3. 
[ ]4.

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

        # Full Text  Helper Variables
        self.full_text = self._fetch_full_text()
        self.chapter_text = self.full_text.splitlines()[self.start_line: self.end_line]
        self.chapters = self._split_chapters(self.chapter_text)

    
    def _fetch_full_text(self):
        req = Request(self.url)
        with urlopen(req) as res:
            return res.read().decode('utf-8')
    
    def _split_chapters(self, chapter_lines):
        full_chapter_text = '\n'.join(chapter_lines)
        raw_chapters = re.split(r'\n{4,}', full_chapter_text.strip())

        documents = []

        document_id = 0

        for chapter in raw_chapters:
            chapter_parts = [line.strip() for line in chapter.split('\n') if line.strip()]
            if not chapter_parts:
                continue
        
            chapter_title = chapter_parts[0]
            chapter_content = '\n'.join(chapter_parts[1:])

            documents.append(Document(
                document_id=document_id, 
                title=chapter_title, 
                raw_text=chapter_content.strip(),
                terms=chapter_content.replace('\n',' ').split(),
                author=self.author,
                origin=self.origin)
                )

            document_id += 1

            # chapters.append((chapter_title, chapter_content.strip()))
        
        return documents

    def get_documents(self):
        self.documents = self._split_chapters(chapter_lines=self.chapter_text)

        return self.documents

    def _tokenize(self,content : str) -> list[str]:
        #Tokenize
        # Convert text to lower and replace punctuation
        for punct in PUNCT:
            content = content.replace(punct,' ')
        # print(content)
        return [word.lower() for word in content.split() if word]


def load_collection_from_url(url, author, origin, start_line, end_line, search_pattern=None):
    parser = gutenbergParser(url, author, origin, start_line, end_line, search_pattern)
    documents =  parser.get_documents()
    return documents

