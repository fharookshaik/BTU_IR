import re

def is_consonant(word, i):
    """Check if the character at index i in word is a consonant."""
    letter = word[i].lower()
    if letter in 'aeiou':
        return False
    if letter == 'y':
        return i == 0 or not is_consonant(word, i - 1)
    return True

def get_measure(word):
    """Calculate the measure (m) of a word: number of VC sequences."""
    m = 0
    i = 0
    # Find [C]
    while i < len(word) and is_consonant(word, i):
        i += 1
    # Count VC sequences
    while i < len(word):
        # Must have at least one vowel
        has_vowel = False
        while i < len(word) and not is_consonant(word, i):
            has_vowel = True
            i += 1
        if not has_vowel:
            break
        # Must have at least one consonant
        has_consonant = False
        while i < len(word) and is_consonant(word, i):
            has_consonant = True
            i += 1
        if has_consonant and has_vowel:
            m += 1
    return m

def contains_vowel(stem):
    """Check if the stem contains at least one vowel."""
    for i in range(len(stem)):
        if not is_consonant(stem, i):
            return True
    return False

def ends_with_double_consonant(stem):
    """Check if the stem ends with a double consonant."""
    if len(stem) < 2:
        return False
    return (is_consonant(stem, len(stem) - 1) and 
            is_consonant(stem, len(stem) - 2) and 
            stem[-1].lower() == stem[-2].lower())

def ends_with_cvc(stem):
    """Check if the stem ends with consonant-vowel-consonant, where the last consonant is not w, x, or y."""
    if len(stem) < 3:
        return False
    return (is_consonant(stem, len(stem) - 3) and 
            not is_consonant(stem, len(stem) - 2) and 
            is_consonant(stem, len(stem) - 1) and 
            stem[-1].lower() not in 'wxy')

def apply_rule(word, pattern, replacement, condition):
    """Apply a suffix removal rule using regex if the condition is met."""
    match = re.search(pattern + '$', word, re.IGNORECASE)
    if not match:
        return word, False
    stem = word[:match.start()]
    if condition(stem):
        return stem + replacement, True
    return word, False

def porter_stem(word):
    """Apply the Porter Stemming Algorithm to a word using regex."""
    if not word:
        return word

    # Step 1a: Handle plurals
    step1a_rules = [
        (r'sses', 'ss', lambda s: True),
        (r'ies', 'i', lambda s: True),
        (r'ss', 'ss', lambda s: True),
        (r's', '', lambda s: True),
    ]
    for pattern, replacement, condition in step1a_rules:
        new_word, applied = apply_rule(word, pattern, replacement, condition)
        if applied:
            word = new_word
            break

    # Step 1b: Handle past participles and gerunds
    step1b_rules = [
        (r'eed', 'ee', lambda s: get_measure(s) > 0),
        (r'ed', '', lambda s: contains_vowel(s)),
        (r'ing', '', lambda s: contains_vowel(s)),
    ]
    applied_1b = False
    for pattern, replacement, condition in step1b_rules:
        new_word, applied = apply_rule(word, pattern, replacement, condition)
        if applied:
            word = new_word
            applied_1b = True
            break

    # Step 1b follow-up: Adjust stem after ED or ING removal
    if applied_1b:
        for pattern, replacement in [(r'at$', 'ate'), (r'bl$', 'ble'), (r'iz$', 'ize')]:
            if re.search(pattern, word, re.IGNORECASE):
                word = re.sub(pattern, replacement, word, flags=re.IGNORECASE)
                break
        else:
            if (ends_with_double_consonant(word) and 
                word[-1].lower() not in 'lsz'):
                word = word[:-1]
            elif get_measure(word) == 1 and ends_with_cvc(word):
                word = word + 'e'

    # Step 1c: Handle Y after vowel
    if re.search(r'y$', word, re.IGNORECASE) and contains_vowel(word[:-1]):
        word = re.sub(r'y$', 'i', word, flags=re.IGNORECASE)

    # Step 2: Handle complex suffixes
    step2_rules = [
        (r'ational$', 'ate', lambda s: get_measure(s) > 0),
        (r'tional$', 'tion', lambda s: get_measure(s) > 0),
        (r'enci$', 'ence', lambda s: get_measure(s) > 0),
        (r'anci$', 'ance', lambda s: get_measure(s) > 0),
        (r'izer$', 'ize', lambda s: get_measure(s) > 0),
        (r'abli$', 'able', lambda s: get_measure(s) > 0),
        (r'alli$', 'al', lambda s: get_measure(s) > 0),
        (r'entli$', 'ent', lambda s: get_measure(s) > 0),
        (r'eli$', 'e', lambda s: get_measure(s) > 0),
        (r'ousli$', 'ous', lambda s: get_measure(s) > 0),
        (r'ization$', 'ize', lambda s: get_measure(s) > 0),
        (r'ation$', 'ate', lambda s: get_measure(s) > 0),
        (r'ator$', 'ate', lambda s: get_measure(s) > 0),
        (r'alism$', 'al', lambda s: get_measure(s) > 0),
        (r'iveness$', 'ive', lambda s: get_measure(s) > 0),
        (r'fulness$', 'ful', lambda s: get_measure(s) > 0),
        (r'ousness$', 'ous', lambda s: get_measure(s) > 0),
        (r'aliti$', 'al', lambda s: get_measure(s) > 0),
        (r'iviti$', 'ive', lambda s: get_measure(s) > 0),
        (r'biliti$', 'ble', lambda s: get_measure(s) > 0),
    ]
    for pattern, replacement, condition in step2_rules:
        new_word, applied = apply_rule(word, pattern, replacement, condition)
        if applied:
            word = new_word
            break

    # Step 3: Handle additional suffixes
    step3_rules = [
        (r'icate$', 'ic', lambda s: get_measure(s) > 0),
        (r'ative$', '', lambda s: get_measure(s) > 0),
        (r'alize$', 'al', lambda s: get_measure(s) > 0),
        (r'iciti$', 'ic', lambda s: get_measure(s) > 0),
        (r'ical$', 'ic', lambda s: get_measure(s) > 0),
        (r'ful$', '', lambda s: get_measure(s) > 0),
        (r'ness$', '', lambda s: get_measure(s) > 0),
    ]
    for pattern, replacement, condition in step3_rules:
        new_word, applied = apply_rule(word, pattern, replacement, condition)
        if applied:
            word = new_word
            break

    # Step 4: Handle further suffixes
    step4_rules = [
        (r'al$', '', lambda s: get_measure(s) > 1),
        (r'ance$', '', lambda s: get_measure(s) > 1),
        (r'ence$', '', lambda s: get_measure(s) > 1),
        (r'er$', '', lambda s: get_measure(s) > 1),
        (r'ic$', '', lambda s: get_measure(s) > 1),
        (r'able$', '', lambda s: get_measure(s) > 1),
        (r'ible$', '', lambda s: get_measure(s) > 1),
        (r'ant$', '', lambda s: get_measure(s) > 1),
        (r'ement$', '', lambda s: get_measure(s) > 1),
        (r'ment$', '', lambda s: get_measure(s) > 1),
        (r'ent$', '', lambda s: get_measure(s) > 1),
        (r'ion$', '', lambda s: get_measure(s) > 1 and s[-1].lower() in 'st'),
        (r'ou$', '', lambda s: get_measure(s) > 1),
        (r'ism$', '', lambda s: get_measure(s) > 1),
        (r'ate$', '', lambda s: get_measure(s) > 1),
        (r'iti$', '', lambda s: get_measure(s) > 1),
        (r'ous$', '', lambda s: get_measure(s) > 1),
        (r'ive$', '', lambda s: get_measure(s) > 1),
        (r'ize$', '', lambda s: get_measure(s) > 1),
    ]
    for pattern, replacement, condition in step4_rules:
        new_word, applied = apply_rule(word, pattern, replacement, condition)
        if applied:
            word = new_word
            break

    # Step 5a: Remove final E
    if re.search(r'e$', word, re.IGNORECASE):
        stem = word[:-1]
        m = get_measure(stem)
        if m > 1 or (m == 1 and not ends_with_cvc(stem)):
            word = stem

    # Step 5b: Handle double L
    if (re.search(r'll$', word, re.IGNORECASE) and 
        ends_with_double_consonant(word) and 
        get_measure(word[:-1]) > 1):
        word = word[:-1]

    return word

