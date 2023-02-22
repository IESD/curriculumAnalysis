import os, nltk, string

nltk.download('stopwords')
from DataBlock import DataBlock
from collections import defaultdict, OrderedDict
from pathlib import Path


def extractData(path):
    for file in os.scandir(path):
        if not file.name.endswith('txt'):
            continue
        name, _ = file.name.rsplit('.', 1)
        with open(file.path, encoding='utf8') as f:
            tokens = [word for line in f.readlines() for sent in nltk.sent_tokenize(line) for word in
                      nltk.word_tokenize(sent)]
        yield name, tokens


rootFolder = '../import/'
sw = nltk.corpus.stopwords.words('english')
punct = string.punctuation + '“”–‘’—¿•'

rawData = {name: tokens for name, tokens in extractData(rootFolder)}
names = list({name for name in rawData})
data = {name: nltk.text.Text([token.lower() for token in rawData[name] if token not in punct and token not in sw]) for
        name in names}

dataBlock = DataBlock(rawData)

# defining unique words for programmes/modules
vocabs = {k: data[k].vocab() for k in data}
uniqueWords = defaultdict(list)
specialWords = defaultdict(dict)
for thisName, thatName in zip(names, reversed(names)):
    for word in vocabs[thisName]:
        thisRelativeFrequency = vocabs[thisName][word] / len(data[thisName]) * 10000
        thatRelativeFrequency = vocabs[thatName][word] / len(data[thatName]) * 10000
        try:
            relativeFrequencyRatio = thisRelativeFrequency / thatRelativeFrequency
        except ZeroDivisionError:
            uniqueWords[thisName].append((word, thisRelativeFrequency))
            continue
        specialWords[thisName][word] = {
            f'this': thisRelativeFrequency,
            f'that': thatRelativeFrequency,
            f'ratio': relativeFrequencyRatio,
            f'total': thisRelativeFrequency + thatRelativeFrequency
        }
    uniqueWords[thisName].sort(key=lambda x: x[1], reverse=True)


def ShowUniqueWords(path):
    with path.open('w') as f:
        print('-' * 90, file=f)
        print(f'unique words', file=f)
        print('-' * 90, file=f)
        print(*[f'{n:<42}' for n in names], sep='\t\t', file=f)
        print('-' * 90, file=f)
        for i in range(10):
            top = [uniqueWords[n][i] for n in names]
            print(*[f'{word:37} {f:.2f}' for word, f in top], sep='\t\t', file=f)


def ShowKeywords(key, path):
    with open('keywords.txt', encoding='utf8') as f:
        keywords = f.read().split(', ')
    with path.open('a') as f:
        for name in names:
            words = OrderedDict(sorted(specialWords[name].items(), key=key, reverse=True))
            keys = words['report'].keys()
            print('', file=f)
            print('-' * 65, file=f)
            print(name, file=f)
            print('-' * 65, file=f)
            print(f'{"word":25}', *[f'{k:10}' for k in keys], sep=' ', file=f)
            print('-' * 65, file=f)
            for kw in keywords:
                try:
                    print(f'{kw:20}', *[f'{words[kw.lower()][k]:10.2f}' for k in keys], sep=' ', file=f)
                except KeyError:
                    continue
            print('-' * 65, file=f)
            print('', file=f)


path = Path('data')
path.mkdir(parents=True, exist_ok=True)
path = path / 'data.txt'
ShowUniqueWords(path)
ShowKeywords(lambda x: x[1]['ratio'], path)
# creates file in directory 'data' containing keywords in modules and programmes
