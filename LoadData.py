import os, nltk, string
nltk.download('stopwords')
from DataBlock import DataBlock
from collections import defaultdict, OrderedDict
from pathlib import Path

def extract_data(path):
    for file in os.scandir(path):
        if not file.name.endswith('txt'):
            continue
        name, _ = file.name.rsplit('.', 1)
        with open(file.path, encoding="utf8") as f:
            tokens = [word for line in f.readlines() for sent in nltk.sent_tokenize(line) for word in nltk.word_tokenize(sent)]
        yield name, tokens

root_folder = "../import/"
sw = nltk.corpus.stopwords.words('english')
punct = string.punctuation + "“”–‘’—¿•"

raw_data = {name: tokens for name, tokens in extract_data(root_folder)}
names = list({name for name in raw_data})
data = {name: nltk.text.Text([token.lower() for token in raw_data[name] if token not in punct and token not in sw]) for name in names}

dataBlock = DataBlock(raw_data)

_vocabs = {k: data[k].vocab() for k in data}
_unique_words = defaultdict(list)
_special_words = defaultdict(dict)
for this_name, that_name in zip(names, reversed(names)):
    for word in _vocabs[this_name]:
        this_relative_frequency = _vocabs[this_name][word] / len(data[this_name]) * 10000
        that_relative_frequency = _vocabs[that_name][word] / len(data[that_name]) * 10000
        try:
            relative_frequency_ratio = this_relative_frequency / that_relative_frequency
        except ZeroDivisionError:
            _unique_words[this_name].append((word, this_relative_frequency))
            continue
        _special_words[this_name][word] = {
            f'this': this_relative_frequency,
            f'that': that_relative_frequency,
            f'ratio': relative_frequency_ratio,
            f'total': this_relative_frequency + that_relative_frequency
        }
    _unique_words[this_name].sort(key=lambda x: x[1], reverse=True)

def _show_unique_words(path):
    with path.open('w') as f:
        print("-" * 90, file=f)
        print(f"unique words", file=f)
        print("-" * 90, file=f)
        print(*[f"{n:<42}" for n in names], sep="\t\t", file=f)
        print("-" * 90, file=f)
        for i in range(10):
            top = [_unique_words[n][i] for n in names]
            print(*[f"{word:37} {f:.2f}" for word, f in top], sep="\t\t", file=f)

def _show_keywords(key, path):
    with open('keywords.txt', encoding="utf8") as f:
        keywords = f.read().split(', ')
    with path.open('a') as f:
        for name in names:
            words = OrderedDict(sorted(_special_words[name].items(), key=key, reverse=True))
            keys = words['report'].keys()
            print('', file=f)
            print('-' * 65, file=f)
            print(name, file=f)
            print('-' * 65, file=f)
            print(f"{'word':25}", *[f'{k:10}' for k in keys], sep=' ', file=f)
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
_show_unique_words(path)
_show_keywords(lambda x: x[1]['ratio'], path)
# creates file in directory 'data' containing keywords in modules and programmes

print(dataBlock.modules[0].tokens)