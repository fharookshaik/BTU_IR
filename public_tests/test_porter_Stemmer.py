import unittest
from my_module import PorterStemmer  # Assuming your PorterStemmer class is in my_module.py

class TestPorterStemmer(unittest.TestCase):
    def setUp(self):
        self.stemmer = PorterStemmer()

    def test_stemming(self):
        test_cases = {
            "caresses": "caress", "ponies": "poni", "ties": "ti", "caress": "caress", "cats": "cat",
            "feed": "feed", "agreed": "agre", "plastered": "plaster", "bled": "bled", "motoring": "motor", "sing": "sing",
            "conflated": "conflat", "troubled": "troubl", "sized": "size", "hopping": "hop", "tanned": "tan", "falling": "fall", "hissing": "hiss", "fizzed": "fizz",
            "failing": "fail", "filing": "file", "happy": "happi", "sky": "sky",
            "relational": "relate", "conditional": "condit", "rational": "rat", "valenci": "valence", "hesitanci": "hesitance", "digitizer": "digitize",
            "conformabli": "conformable", "radicalli": "radical", "differentli": "different", "vileli": "vile", "analogousli": "analogous", "vietnamization": "vietnamize",
            "predication": "predicate", "operator": "operate", "feudalism": "feudal", "decisiveness": "decisive", "hopefulness": "hopeful", "callousness": "callous",
            "formaliti": "formal", "sensitiviti": "sensitive", "sensibiliti": "sensible",
            "triplicate": "triplic", "formative": "form", "formalize": "formal", "electriciti": "electric", "electrical": "electric", "hopeful": "hope", "goodness": "good",
            "revival": "reviv", "allowance": "allow", "inference": "infer", "airliner": "airlin", "gyroscopic": "gyroscop", "adjustable": "adjust", "defensible": "defensible", # Stays the same
            "irritant": "irrit", "replacement": "replac", "adjustment": "adjust", "dependent": "dependent", # Stays the same
            "adoption": "adopt", "homologous": "homolog", "communism": "commun",
            "activate": "activ", "angulariti": "angular", "effective": "effect", "bowdlerize": "bowdler",
            "probate": "probat", "rate": "rate", "cease": "cease", "controll": "control", "roll": "roll",
            "generalizations": "generalization"
        }

        for word, expected_stem in test_cases.items():
            actual_stem = self.stemmer.stem(word)
            self.assertEqual(actual_stem, expected_stem, f"Stemming of '{word}' failed. Expected '{expected_stem}', got '{actual_stem}'")

if __name__ == '__main__':
    unittest.main()

# for word in test_words:
#     print(f"{word} -> {porter_stem(word)}")