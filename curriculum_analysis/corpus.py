"""Corpus instances are initialised with text and can calculate everything we need"""

import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet', quiet=True)
lemmatizer = WordNetLemmatizer()

def slice_from_concordance(con):
    return slice(
        con.offset - len(con.left),
        con.offset + len(con.right) + 1
    )

def delemmatize(concordance, tokens):
    t = tokens[slice_from_concordance(concordance)]
    i = len(concordance.left)
    t[i] = t[i].upper()
    return " ".join(t)

class Corpus:
    def __init__(self, label, text):
        self.label = label
        self.raw_string = text
        self.tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        self.lemmatized_tokens = [lemmatizer.lemmatize(t) for t in self.tokens]
        self.text = nltk.text.Text(self.tokens)
        self.lemmatized_text = nltk.text.Text(self.lemmatized_tokens)
        self.vocab = self.text.vocab()
        self.lemmatized_vocab = self.lemmatized_text.vocab()

    def delemmatized_concordance_list(self, kw, **kwargs):
        lemmatized = self.lemmatized_text.concordance_list(kw, **kwargs)
        return [delemmatize(l, self.tokens) for l in lemmatized]

    def __repr__(self):
        return f"Corpus({self.label})"

