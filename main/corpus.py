"""Corpus instances are initialised with text and can calculate everything we need"""

import nltk
from nltk.stem import PorterStemmer
from collections import defaultdict

stemmer = PorterStemmer()

class Corpus:
    def __init__(self, label, text):
        self.label = label
        self.raw_string = text
        self.tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        stemmed_tokens = [stemmer.stem(t) for t in self.tokens]
        self.text = nltk.text.Text(self.tokens)
        self.stemmed_text = nltk.text.Text(stemmed_tokens)
        self.vocab = self.text.vocab()
        self.stemmed_vocab = self.stemmed_text.vocab()

    def analyse(self, keywords, **kwargs):
        keywords = [stemmer.stem(kw) for kw in keywords]
        matches = [kw for kw in keywords if self.stemmed_vocab[kw]]
        concordances = defaultdict(list)
        for kw in matches:
            for stem in self.stemmed_text.concordance_list(kw, **kwargs):
                t = self.tokens[stem.offset - len(stem.left):stem.offset + len(stem.right) + 1]
                t[stem.offset] = t[stem.offset].upper()
                concordances[kw].append(' '.join(t))
        return [Result(kw, self.stemmed_vocab[kw], concordances[kw]) for kw in matches]

    def __repr__(self):
        return f"Corpus({self.label})"


class Result:
    def __init__(self, keyword, count, concordances):
        self.keyword = keyword
        self.count = count
        self.concordances = concordances

    def __repr__(self):
        return f"Result({self.keyword}, {self.count or None})"


if __name__ == "__main__":
    c = Corpus('test', 'sustainable sustainability')
    print(c.raw_string)
    print(c.text)
    print(c.vocab)
    print(c)
    result = c.analyse(['sustain'])
    print(result)
    for r in result:
        print('-' * 20)
        print(f'{r.keyword}: {r.count}')
        print('-' * 20)
        print(r.concordances)
        for c in r.concordances:
            print(c)
