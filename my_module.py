"""
TODO: Write the folllowing components

[X]1. load_collection_from_url(url, search_pattern, start_line, end_line, author, origin)
[!]2. Handle Data Processing - Stopword Elimination, Stemming, Tokenization
[X]3. remove_stop_words(doc.terms, stopwords)
[X]4. remove_stop_words_by_frequency(doc.terms, collection, low_freq=rare_frequency, high_freq=common_frequency)
[X]5. linear_boolean_search(term, collection, stopword_filtered)

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
from collections import defaultdict
from document import Document

# Global Variables
PUNCT = '.,!?;:"“”\'()[]{}'


class DataPreprocess:
    def __init__(self, doc: Document) -> None:
        pass






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
        self.chapter_text = '\n'.join(self.full_text.splitlines()[self.start_line: self.end_line])

    
    def _fetch_full_text(self):
        req = Request(self.url)
        with urlopen(req) as res:
            return res.read().decode('utf-8')
    
    def _split_chapters(self, chapter_text, search_pattern):
        chapter_parts = search_pattern.findall(chapter_text)

        documents = []
        document_id = 0

        for chapter_title, chapter_content in chapter_parts:
            documents.append(Document(
                document_id= document_id,
                title = chapter_title,
                raw_text = chapter_content.strip(),
                terms = self._tokenize(chapter_content),
                author=self.author,
                origin=self.origin)
            )
            document_id += 1
        
        return documents

    def get_documents(self):
        self.documents = self._split_chapters(chapter_text=self.chapter_text, search_pattern=self.search_pattern)

        return self.documents

    def _tokenize(self,content : str) -> list[str]:
        #Tokenize
        # Convert text to lower and replace punctuation
        for punct in PUNCT:
            content = content.replace(punct,' ')
        # print(content)
        return [word.lower() for word in content.split() if word]



# Main Functions compatible with test_wrapper

def load_collection_from_url(url, author, origin, start_line, end_line, search_pattern):
    parser = gutenbergParser(url=url, author=author, origin=origin, start_line=start_line, end_line=end_line, search_pattern=search_pattern)
    documents =  parser.get_documents()
    # print(parser._tokenize(documents[0].raw_text))
    return documents


def remove_stop_words(terms, stopwords=None):
    if stopwords is not None:
        return [term.lower() for term in terms if term.lower() not in stopwords]

    with open('helpers/stopwords.txt','r') as src:
        stopwords = [line.strip() for line in src.readlines()]

    return [term.lower() for term in terms if term.lower() not in stopwords]    


def remove_stop_words_by_frequency(terms, collection, low_freq, high_freq):

    # Count total document frequency of each term    
    term_doc_freq = defaultdict(int)

    for doc in collection:
        unique_terms = set(doc.terms)
        for term in unique_terms:
            term_doc_freq[term] += 1
        

    # Compute frequency percentile thresholds
    term_freqs = list(term_doc_freq.values())
    term_freqs.sort()

    percentile = lambda p: term_freqs[min(int(p * len(term_freqs)), len(term_freqs) - 1)]

    # def percentile(p):
    #     idx = int(p * len(term_freqs))
    #     return term_freqs[min(idx, len(term_freqs) - 1)]
    
    min_thresold = percentile(low_freq)
    max_thresold = percentile(high_freq)


    # Determine stop words (too rare or too frequent)
    stopwords = {
        term for term, freq in term_doc_freq.items() if freq <= min_thresold or freq >= max_thresold
    }

    # Filter terms from given list
    return [term for term in terms if term not in stopwords]


def linear_boolean_search(term, collection, stopword_filtered=False):
    result = []
    term = term.lower()

    for doc in collection:
        if stopword_filtered:
            terms_to_search = doc.filtered_terms
        else:
            terms_to_search = doc.terms
        
        terms_lower = [t.lower() for t in terms_to_search]
        score = terms_lower.count(term)

        result.append((score, doc))
    
    return result