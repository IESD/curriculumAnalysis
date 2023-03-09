"""Corpus instances are initialised with text and can calculate everything we need"""

import nltk
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

class Corpus:
    def __init__(self, label, text):
        self.label = label
        self.raw_string = text
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        stemmed = [stemmer.stem(t) for t in tokens]
        self.text = nltk.text.Text(tokens)
        self.stemmed_text = nltk.text.Text(stemmed)
        self.vocab = self.text.vocab()
        self.stemmed_vocab = self.stemmed_text.vocab()

    def analyse(self, keywords, **kwargs):
        matches = [kw for kw in keywords if kw in self.stemmed_vocab]
        return [Result(kw, self.stemmed_vocab[kw], self.stemmed_text.concordance_list(kw, **kwargs)) for kw in matches]

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
    c = Corpus('test', "hello world and goodbye")
    print(c.raw_string)
    print(c.text)
    print(c.vocab)
    print(c)
    result = c.analyse(['hello', 'goodbye'])
    print(result)
    for r in result:
        print('-' * 20)
        print(f'{r.keyword}: {r.count}')
        print('-' * 20)
        print(r.concordances)
        for c in r.concordances:
            if c.left_print:
                print(c.left_print, end=' ')
            print(c.query.upper(), end=' ')
            if c.right_print:
                print(c.right_print)
