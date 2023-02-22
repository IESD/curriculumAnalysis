import nltk, string
from collections import defaultdict, OrderedDict
from pathlib import Path

sw = nltk.corpus.stopwords.words('english')
punct = string.punctuation + "“”–‘’—¿•"

with open('keywords.txt', encoding="utf8") as f:
    keywords = f.read().split(', ')


class DataBlock:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.programmes = []
        self.modules = []
        self.__loadProgrammes(raw_data['0325_Programme_Specification_for_Academics'])
        self.__loadModules(raw_data['0324_Module_Specification_for_Academics'])

    def __loadProgrammes(self, raw_data):
        linesIter = iter(raw_data)
        tokens = []
        for token in linesIter:
            tokens.append(token)
            if tokens[-6:-1] == ['End', 'of', 'Programme', 'Specification', 'for']:
                newProgramme = Programme(tokens)
                self.programmes.append(newProgramme)
                tokens = []

    def __loadModules(self, raw_data):
        linesIter = iter(raw_data)
        tokens = []
        for token in linesIter:
            tokens.append(token)
            if tokens[-6:-1] == ['End', 'of', 'Module', 'Specification', 'for']:
                newModule = Module(tokens)
                self.modules.append(newModule)
                tokens = []


class Programme:
    def __init__(self, raw_data):
        self.raw_data = nltk.text.Text([token.lower() for token in raw_data])
        self.data = nltk.text.Text([token.lower() for token in self.raw_data if token not in punct and token not in sw])
        self.code = raw_data[2]
        self.root = Path('data', f'{self.code}')
        self.keywords = []
        self.saveRawData(raw_data)
        self.collocations = self.saveCollocations()
        self.concordances = self.saveConcordances()
        self.saveKeywords()
        self.saveKeywordConcordances()

    def saveRawData(self, raw_data):
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f'{self.code}.txt'
        with path.open('w', encoding="utf8") as f:
            print(raw_data, file=f)

    def saveCollocations(self):
        collocations = self.data.collocation_list(num=10, window_size=30)
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / 'collocations.txt'
        with path.open('w') as f:
            print('-' * 30, file=f)
            print(f'{self.code:30}', file=f)
            print('-' * 30, file=f)
            for i in range(10):
                print(*[f'{" ".join(collocations[i]):30}'], file=f)
        return collocations

    def saveConcordances(self):
        concordances = {self.collocations[i]: self.raw_data.concordance_list(list(self.collocations[i])) for i in
                        range(5)}
        path = self.root / 'concordances.txt'
        with path.open('w') as f:
            for term in concordances:
                print('-' * 90, file=f)
                print(f'{" ".join(term)}', file=f)
                print('-' * 90, file=f)
                for conc in concordances[term]:
                    print(*conc.left, ' '.join(term).upper(), *conc.right, '\n', file=f)
        return concordances

    def saveKeywords(self):
        _vocabs = self.data.vocab()
        _special_words = defaultdict(dict)
        for word in _vocabs:
            relative_frequency = _vocabs[word] / len(self.data) * 10000
            _special_words[word] = {
                f'freq': relative_frequency
            }
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / 'keywords.txt'
        with path.open('w') as f:
            words = OrderedDict(sorted(_special_words.items(), reverse=True))
            keys = words['end'].keys()
            print('-' * 30, file=f)
            print(f'{self.code:30}', file=f)
            print('-' * 30, file=f)
            print(f"{'word':25}", *[f'{k:10}' for k in keys], sep=' ', file=f)
            print('-' * 30, file=f)
            for kw in keywords:
                try:
                    print(f'{kw:20}', *[f'{words[kw.lower()][k]:10.2f}' for k in keys], sep=' ', file=f)
                    self.keywords.append(kw)
                except KeyError:
                    continue
            print('-' * 30, file=f)
            print('', file=f)

    def saveKeywordConcordances(self):
        concordances = {kw: self.raw_data.concordance_list(list(kw)) for kw in self.keywords}
        path = self.root / 'keywordConcordances.txt'
        with path.open('w') as f:
            for term in concordances:
                print('-' * 90, file=f)
                print(f'{term}', file=f)
                print('-' * 90, file=f)
                for conc in concordances[term]:
                    print(*conc.left, ' '.join(term).upper(), *conc.right, '\n', file=f)


class Module(Programme):
    def __init__(self, raw_data):
        super().__init__(raw_data)
