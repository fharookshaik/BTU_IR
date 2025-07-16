from urllib.request import urlopen, Request
from collections import defaultdict
from document import Document
import re

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


class PorterStemmer:
    def __init__(self) -> None:
        # RULES
        self.STEP1A_RULES = [
            (r'sses', 'ss', lambda s: True),
            (r'ies', 'i', lambda s: True),
            (r'ss', 'ss', lambda s: True),
            (r's', '', lambda s: True),
        ]

        self.STEP1B_RULES = [
            (r'eed', 'ee', lambda s: self._get_measure(s) > 0),
            (r'ed', '', lambda s: self._contains_vowel(s)),
            (r'ing', '', lambda s: self._contains_vowel(s)),
        ]

        self.STEP1B_RULES_EXT = [
            (r'at$', 'ate'),
            (r'bl$', 'ble'),
            (r'iz$', 'ize')
        ]

        self.STEP1C_RULES = [
            (r'y$', 'i')
        ]

        self.STEP2_RULES = [
            (r'ational$', 'ate', lambda s: self._get_measure(s) > 0),
            (r'tional$', 'tion', lambda s: self._get_measure(s) > 0),
            (r'enci$', 'ence', lambda s: self._get_measure(s) > 0),
            (r'anci$', 'ance', lambda s: self._get_measure(s) > 0),
            (r'izer$', 'ize', lambda s: self._get_measure(s) > 0),
            (r'abli$', 'able', lambda s: self._get_measure(s) > 0),
            (r'alli$', 'al', lambda s: self._get_measure(s) > 0),
            (r'entli$', 'ent', lambda s: self._get_measure(s) > 0),
            (r'eli$', 'e', lambda s: self._get_measure(s) > 0),
            (r'ousli$', 'ous', lambda s: self._get_measure(s) > 0),
            (r'ization$', 'ize', lambda s: self._get_measure(s) > 0),
            (r'ation$', 'ate', lambda s: self._get_measure(s) > 0),
            (r'ator$', 'ate', lambda s: self._get_measure(s) > 0),
            (r'alism$', 'al', lambda s: self._get_measure(s) > 0),
            (r'iveness$', 'ive', lambda s: self._get_measure(s) > 0),
            (r'fulness$', 'ful', lambda s: self._get_measure(s) > 0),
            (r'ousness$', 'ous', lambda s: self._get_measure(s) > 0),
            (r'aliti$', 'al', lambda s: self._get_measure(s) > 0),
            (r'iviti$', 'ive', lambda s: self._get_measure(s) > 0),
            (r'biliti$', 'ble', lambda s: self._get_measure(s) > 0),
            (r'xflurti$', 'xti', lambda s: self._get_measure(s) > 0),
        ]

        self.STEP3_RULES = [
            (r'icate$', 'ic', lambda s: self._get_measure(s) > 0),
            (r'ative$', '', lambda s: self._get_measure(s) > 0),
            (r'alize$', 'al', lambda s: self._get_measure(s) > 0),
            (r'iciti$', 'ic', lambda s: self._get_measure(s) > 0),
            (r'ical$', 'ic', lambda s: self._get_measure(s) > 0),
            (r'ful$', '', lambda s: self._get_measure(s) > 0),
            (r'ness$', '', lambda s: self._get_measure(s) > 0),
        ]

        self.STEP4_RULES = [
            (r'al$', '', lambda s: self._get_measure(s) > 1),
            (r'ance$', '', lambda s: self._get_measure(s) > 1),
            (r'ence$', '', lambda s: self._get_measure(s) > 1),
            (r'er$', '', lambda s: self._get_measure(s) > 1),
            (r'ic$', '', lambda s: self._get_measure(s) > 1),
            (r'able$', '', lambda s: self._get_measure(s) > 1),
            (r'ible$', '', lambda s: self._get_measure(s) > 1),
            (r'ant$', '', lambda s: self._get_measure(s) > 1),
            (r'ement$', '', lambda s: self._get_measure(s) > 1),
            (r'ment$', '', lambda s: self._get_measure(s) > 1),
            (r'ent$', '', lambda s: self._get_measure(s) > 1),
            (r'ion$', '', lambda s: self._get_measure(s) > 1 and s[-1].lower() in 'st'),
            (r'ou$', '', lambda s: self._get_measure(s) > 1),
            (r'ism$', '', lambda s: self._get_measure(s) > 1),
            (r'ate$', '', lambda s: self._get_measure(s) > 1),
            (r'iti$', '', lambda s: self._get_measure(s) > 1),
            (r'ous$', '', lambda s: self._get_measure(s) > 1),
            (r'ive$', '', lambda s: self._get_measure(s) > 1),
            (r'ize$', '', lambda s: self._get_measure(s) > 1),
        ]

        self.STEP5A_RULES = [
            (r'e$', '', lambda s: self._get_measure(s) > 1 or (self._get_measure(s) == 1 and not self._ends_with_cvc(s))),
        ]

        self.STEP5B_RULES = [
            (r'll$', '', lambda s: self._get_measure(s) > 1 and self._ends_with_double_consonant(s) and self._get_measure(s[:-1]) > 1),
        ]
    
    def _is_consonant(self, word, i):
        """Check if the character at index i in word is a consonant."""
        letter = word[i].lower()
        if letter in 'aeiou':
            return False
        if letter == 'y':
            return i == 0 or not self._is_consonant(word, i - 1)
        return True

    def _contains_vowel(self, stem):
        """Check if the stem contains at least one vowel."""
        for i in range(len(stem)):
            if not self._is_consonant(stem, i):
                return True
        return False

    def _ends_with_double_consonant(self, stem):
        """Check if the stem ends with a double consonant."""
        if len(stem) < 2:
            return False
        return (self._is_consonant(stem, len(stem) - 1) and 
                self._is_consonant(stem, len(stem) - 2) and 
                stem[-1].lower() == stem[-2].lower())

    def _ends_with_cvc(self, stem):
        """Check if the stem ends with consonant-vowel-consonant, where the last consonant is not w, x, or y."""
        if len(stem) < 3:
            return False
        return (self._is_consonant(stem, len(stem) - 3)  and
                not self._is_consonant(stem, len(stem) - 2) and 
                self._is_consonant(stem, len(stem) - 1) and
                stem[-1].lower() not in 'wxy')

    def _apply_rule(self, word, pattern, replacement, condition):
        """Apply a suffix removal rule using regex if the condition is met."""
        match = re.search(pattern + '$', word, re.IGNORECASE)
        if not match:
            return word, False
        stem = word[:match.start()]
        if condition(stem):
            return stem + replacement, True
        return word, False

    def _get_measure(self, word):
        """Calculate the measure (m) of a word: number of VC sequences."""
        m = 0
        i = 0
        # Find [C]
        while i < len(word) and self._is_consonant(word, i):
            i += 1
        # Count VC sequences
        while i < len(word):
            # Must have at least one vowel
            has_vowel = False
            while i < len(word) and not self._is_consonant(word, i):
                has_vowel = True
                i += 1
            if not has_vowel:
                break
            # Must have at least one consonant
            has_consonant = False
            while i < len(word) and self._is_consonant(word, i):
                has_consonant = True
                i += 1
            if has_consonant and has_vowel:
                m += 1
        return m


    def stem(self, word):
        if not word:
            return word
        
        # Apply Step_1A Rules
        for pattern, replacement, condition in self.STEP1A_RULES:
            new_word, applied = self._apply_rule(word, pattern, replacement, condition)
            if applied:
                word = new_word
                break
        
        # Apply Step_1B Rules
        applied_1b = False
        for i, (pattern, replacement, condition) in enumerate(self.STEP1B_RULES):
            new_word, applied = self._apply_rule(word, pattern, replacement, condition)
            if applied:
                word = new_word
                if i in (1,2):
                    applied_1b = True
                break
        
        if applied_1b:
            for pattern, replacement in self.STEP1B_RULES_EXT:
                if re.search(pattern, word, re.IGNORECASE):
                    word = re.sub(pattern, replacement, word, flags=re.IGNORECASE)
                    break

            else:    
                if self._ends_with_double_consonant(word) and word[-1].lower() not in 'lsz':
                    word = word[:-1]
                
                elif self._get_measure(word) == 1 and self._ends_with_cvc(word):
                    word = word + 'e'

        # Apply Step_1C Rules
        if re.search(r'y$', word, re.IGNORECASE) and self._contains_vowel(word[:-1]):
            word = re.sub(r'y$', 'i', word, flags=re.IGNORECASE)

        # Apply Step_2, Step_3 and Step_4, Step_5A, Step_5B Rules
        SUBRULES = [self.STEP2_RULES, self.STEP3_RULES, self.STEP4_RULES, self.STEP5A_RULES, self.STEP5B_RULES]
        for RULE in SUBRULES:
            for pattern, replacement, condition in RULE:
                new_word, applied = self._apply_rule(word, pattern, replacement, condition)
                if applied:
                    word = new_word
                    break
            
        return word