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
        matches = {}
        count = {}
        concordances = {}
        keys = self.vocab.keys()
        for kw in keywords:
            for key in keys:
                if key.startswith(kw):
                    try:
                        matches[kw].append(key)
                        count[kw] = count[kw] + self.vocab[key]
                        newConcordances = [c for c in self.text.concordance_list(key, **kwargs)]
                        for c in newConcordances:
                            concordances[kw].append(c)
                    except KeyError:
                        matches[kw] = [key]
                        count[kw] = self.vocab[key]
                        concordances[kw] = self.text.concordance_list(key, **kwargs)
        return [Result(key, count[key], concordances[key]) for key in matches.keys()]

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
