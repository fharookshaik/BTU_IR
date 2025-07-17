import re
import math

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
            (r'y$', 'i', lambda s: self._contains_vowel(s[:-1]))
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
    

    def _apply_rule(self, word, pattern, replacement, condition):
        """Apply a suffix removal rule using regex if the condition is met."""
        match = re.search(pattern + '$', word, re.IGNORECASE)
        if not match:
            return word, False
        stem = word[:match.start()]
        if condition(stem):
            return stem + replacement, True
        return word, False
    

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
        for i, (pattern, replacement, condition) in enumerate(self.STEP1B_RULES):
            new_word, applied = self._apply_rule(word, pattern, replacement, condition)

            # Logic that handles special case words like feed, deed, etc. 
            if not applied and re.search(pattern, word, re.IGNORECASE):
                return word

            if applied:
                word = new_word
                if i in (1,2):
                    for pattern, replacement in self.STEP1B_RULES_EXT:
                        if re.search(pattern, word, re.IGNORECASE):
                            word = re.sub(pattern, replacement, word, flags=re.IGNORECASE)
                    else:
                        if self._ends_with_double_consonant(word) and word[-1].lower() not in 'lsz':
                            word = word[:-1]
                        
                        elif self._get_measure(word) == 1 and self._ends_with_cvc(word):
                            word = word + 'e'
                break
            

        SUBRULES = [self.STEP1C_RULES, self.STEP2_RULES, self.STEP3_RULES, self.STEP4_RULES, self.STEP5A_RULES, self.STEP5B_RULES]

        for RULE in SUBRULES:
            for pattern, replacement, condition in RULE:
                new_word, applied = self._apply_rule(word, pattern, replacement, condition)
                if applied:
                    word = new_word
                    break
 

        return word



def get_term_freq(terms):
    tf = {}
    for t in terms:
        tf[t] = tf.get(t, 0) + 1
    return tf

def vector_space_search(query, collection, stopword_filtered=False, stemmed=False):
    """
    Performs a search using the Vector Space Model with TF-IDF weighting and inverted index.
    Uses augmented TF for query as per Salton & Buckley (1988).

    Args:
        query (str): The query string to search for.
        collection (list[Document]): List of Document objects.
        stopword_filtered (bool): If True, use doc.filtered_terms instead of raw terms.
        stemmed (bool): If True, stem the query and document terms before searching.

    Returns:
        list[tuple[float, Document]]: List of tuples of relevance score (cosine similarity) and Document, sorted by score descending.
    """
    if not collection:
        return []

    N = len(collection)
    stemmer = None
    if stemmed:
        stemmer = PorterStemmer()

    # Process query
    query_terms = query.lower().split()
    if stemmed:
        query_terms = [stemmer.stem(t) for t in query_terms if t]
    if not query_terms:
        return [(0.0, doc) for doc in collection]

    query_tf = get_term_freq(query_terms)
    max_qtf = max(query_tf.values()) if query_tf else 0

    # Build document terms and inverted index
    inverted = {}
    doc_terms = []
    for doc_id, doc in enumerate(collection):
        if stopword_filtered:
            terms = doc.filtered_terms
        else:
            terms = doc.terms
        terms_lower = [t.lower() for t in terms if t]
        if stemmed:
            terms_lower = [stemmer.stem(t) for t in terms_lower]
        doc_terms.append(terms_lower)
        doc_tf = get_term_freq(terms_lower)
        for t, freq in doc_tf.items():
            inverted.setdefault(t, []).append((doc_id, freq))

    # Compute IDFs
    idfs = {t: math.log(N / len(postings)) if len(postings) > 0 else 0.0 for t, postings in inverted.items()}

    # Compute document norms (using tf * idf)
    doc_norms = [0.0] * N
    for doc_id in range(N):
        doc_tf_dict = get_term_freq(doc_terms[doc_id])
        for t, tf in doc_tf_dict.items():
            weight = tf * idfs.get(t, 0.0)
            doc_norms[doc_id] += weight ** 2
        doc_norms[doc_id] = math.sqrt(doc_norms[doc_id]) if doc_norms[doc_id] > 0 else 0.0

    # Compute query norm (using augmented tf * idf)
    query_norm = 0.0
    for t, tf in query_tf.items():
        aug_tf = 0.5 + 0.5 * (tf / max_qtf) if max_qtf > 0 else 0.0
        idf = idfs.get(t, 0.0)
        weight = aug_tf * idf
        query_norm += weight ** 2
    query_norm = math.sqrt(query_norm) if query_norm > 0 else 0.0
    if query_norm == 0:
        return [(0.0, doc) for doc in collection]

    # Accumulate dot products
    accum = [0.0] * N
    for t, q_tf in query_tf.items():
        aug_tf = 0.5 + 0.5 * (q_tf / max_qtf) if max_qtf > 0 else 0.0
        q_weight = aug_tf * idfs.get(t, 0.0)
        for doc_id, d_tf in inverted.get(t, []):
            d_weight = d_tf * idfs.get(t, 0.0)
            accum[doc_id] += q_weight * d_weight

    # Compute cosine scores
    result = []
    for doc_id in range(N):
        if doc_norms[doc_id] == 0.0:
            score = 0.0
        else:
            score = accum[doc_id] / (query_norm * doc_norms[doc_id]) if query_norm * doc_norms[doc_id] != 0 else 0.0
        result.append((score, collection[doc_id]))

    # Sort by score descending
    result.sort(key=lambda x: x[0], reverse=True)
    return result



def precision_recall(retrieved, relevant):
    pass


# words = ['program', 'programs', 'programmer', 'programming', 'programmers']

# stemmer = PorterStemmer()

# for word in words:
#     stemmed_word = stemmer.stem(word)
#     print(f'Stemmed word: {stemmed_word}')
                