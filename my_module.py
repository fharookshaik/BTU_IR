from urllib.request import urlopen, Request
from collections import defaultdict
from document import Document

# Global constant for punctuation symbols to be removed during tokenization
PUNCT = '.,!?;:"“”\'()[]{}'


class gutenbergParser:
    """
    A parser for Project Gutenberg-style plain text books to extract and split chapters into Document objects.

    Attributes:
        url (str): The source URL of the text file.
        author (str): The author of the work.
        origin (str): The source or origin of the collection.
        start_line (int): The line number to start reading the content from.
        end_line (int | None): The line number to stop reading at (None for end of file).
        search_pattern (Pattern): A compiled regex pattern to identify chapters.
    """
    def __init__(self,url, author, origin, start_line, end_line, search_pattern) -> None:
        """Initialize the gutenbergParser with the provided parameters.

        Args:
            url (str): URL to download the plain text book.
            author (str): Name of the author.
            origin (str): Source of book title.
            start_line (int): Line number to start parsing from.
            end_line (int): Line number to sop parsing (None to go till end).
            search_pattern (Pattern): Regex pattern to identify chapter divisions.
        """
        self.url = url
        self.author = author
        self.origin = origin
        self.start_line = start_line
        self.end_line = end_line
        self.search_pattern = search_pattern

        # Full Text Helper Variables
        self.full_text = self._fetch_full_text()
        self.chapter_text = '\n'.join(self.full_text.splitlines()[self.start_line: self.end_line])

    
    def _fetch_full_text(self):
        """Downloads and returns the full text from the URL as a UTF-8 decoded string.
        """
        req = Request(self.url)
        with urlopen(req) as res:
            return res.read().decode('utf-8')
    
    def _split_chapters(self, chapter_text, search_pattern):
        """
        Splits the chapter text into separate Document instances using the regex pattern.

        Args:
            chapter_text (str): The full relevant content.
            search_pattern (Pattern): Compiled regex with groups for chapter title and content.

        Returns:
            list[Document]: A list of Document objects representing chapters.
        """
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
        """
        Public method to extract and return the list of parsed Document objects.

        Returns:
            list[Document]: The parsed documents.
        """
        self.documents = self._split_chapters(chapter_text=self.chapter_text, search_pattern=self.search_pattern)

        return self.documents

    def _tokenize(self,content : str) -> list[str]:
        """Tokenize the given text into words.

        Args:
            content (str): The text to tokenize.

        Returns:
            list[str]: A list of words extracted from the text.
        """
        # Convert text to lower and replace punctuation
        for punct in PUNCT:
            content = content.replace(punct,' ')
        
        return [word.lower() for word in content.split() if word]



# __________MAIN MODULE FUNCTIONS (compatible with testwrapper.py)_________

def load_collection_from_url(url, author, origin, start_line, end_line, search_pattern):
    """Loads and parses a document collection from a given URL using gutenbergParser

    Args:
        url (str): The URL of the document collection.
        author (str): Author of the book
        origin (str): Origin of the book
        start_line (int): The line number to start reading the content from.
        end_line (int | None): The line number to stop reading at (None for end of file).
        search_pattern (Pattern): A compiled regex pattern to identify chapters.

    Returns:
        list[Document]: A list of Document objects.
    """
    parser = gutenbergParser(url=url, 
                             author=author, 
                             origin=origin, 
                             start_line=start_line, 
                             end_line=end_line, 
                             search_pattern=search_pattern)
    documents =  parser.get_documents()
    # print(parser._tokenize(documents[0].raw_text))
    return documents


def remove_stop_words(terms, stopwords=None):
    """
    Removes common stopwords from a list of terms.

    Args:
        terms (list[str]): The input term list.
        stopwords (set[str] | None): Optional custom stopword list.

    Returns:
        list[str]: Filtered terms without stopwords.
    """
    if stopwords is not None:
        return [term.lower() for term in terms if term.lower() not in stopwords]

    with open('helpers/stopwords.txt','r') as src:
        stopwords = [line.strip() for line in src.readlines()]

    return [term.lower() for term in terms if term.lower() not in stopwords]    


def remove_stop_words_by_frequency(terms, collection, low_freq, high_freq):
    """
    Removes stopwords based on JC Crouch's frequency-based method.

    Terms that appear in too few or too many documents are discarded.

    Args:
        terms (list[str]): The list of terms to filter.
        collection (list[Document]): The full document collection for computing frequencies.
        low_freq (float): Lower percentile (e.g., 0.1) to treat terms as too rare.
        high_freq (float): Upper percentile (e.g., 0.5) to treat terms as too common.

    Returns:
        list[str]: Filtered terms.
    """
    
    term_doc_freq = defaultdict(int)

    # Count total document frequency of each term
    for doc in collection:
        unique_terms = set(doc.terms)
        for term in unique_terms:
            term_doc_freq[term] += 1
        

    # Compute frequency percentile thresholds
    term_freqs = list(term_doc_freq.values())
    term_freqs.sort()

    percentile = lambda p: term_freqs[min(int(p * len(term_freqs)), len(term_freqs) - 1)]

    min_thresold = percentile(low_freq)
    max_thresold = percentile(high_freq)


    # Determine stop words (too rare or too frequent)
    stopwords = {
        term for term, freq in term_doc_freq.items() if freq <= min_thresold or freq >= max_thresold
    }

    # Filter terms from given list
    return [term for term in terms if term not in stopwords]


def linear_boolean_search(term, collection, stopword_filtered=False):
    """
    Performs a simple linear boolean search.

    Args:
        term (str): The term to search for.
        collection (list[Document]): List of Document objects.
        stopword_filtered (bool): If True, use doc.filtered_terms instead of raw terms.

    Returns:
        list[tuple[int, Document]]: List of tuples of relevance score and Document.
    """
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