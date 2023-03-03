"""Corpus instances are initialised with text and can calculate everything we need"""

import nltk


class Corpus:
    def __init__(self, label, text):
        self.label = label
        self.raw_string = text
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        self.text = nltk.text.Text(tokens)
        self.vocab = self.text.vocab()
    
    def analyse(self, keywords, **kwargs):
        matches = [kw for kw in keywords if self.vocab[kw]]
        return [Result(kw, self.vocab[kw], self.text.concordance_list(kw, **kwargs)) for kw in matches]

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
    c = Corpus('test', "hello world")
    print(c.raw_string)
    print(c.text)
    print(c.vocab)
    print(c)
    result = c.analyse(['hello', 'goodbye'])
    print(result)
    for r in result:
        print(r.concordances)