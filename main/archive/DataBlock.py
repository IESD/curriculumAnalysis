import nltk, string
from collections import defaultdict, OrderedDict
from pathlib import Path

sw = nltk.corpus.stopwords.words('english')
punct = string.punctuation + '“”–‘’—¿•'

with open('keywords.txt', encoding='utf8') as f:
    keywords = f.read().split(', ')


class DataBlock:
    def __init__(self, rawData):
        self.rawData = rawData
        self.programmes = []
        self.modules = []
        self.__loadProgrammes(rawData['0325_Programme_Specification_for_Academics'])
        self.__loadModules(rawData['0324_Module_Specification_for_Academics'])

    def __loadProgrammes(self, rawData):
        linesIter = iter(rawData)
        tokens = []
        for token in linesIter:
            tokens.append(token)
            if tokens[-6:-1] == ['End', 'of', 'Programme', 'Specification', 'for']:
                newProgramme = Programme(tokens)
                self.programmes.append(newProgramme)
                tokens = []

    def __loadModules(self, rawData):
        linesIter = iter(rawData)
        tokens = []
        for token in linesIter:
            tokens.append(token)
            if tokens[-6:-1] == ['End', 'of', 'Module', 'Specification', 'for']:
                newModule = Module(tokens)
                self.modules.append(newModule)
                tokens = []


class Programme:
    def __init__(self, rawData):
        self.rawData = nltk.text.Text([token.lower() for token in rawData])
        self.data = nltk.text.Text([token.lower() for token in self.rawData if token not in punct and token not in sw])
        self.code = rawData[2]
        self.root = Path('data', f'{self.code}')
        self.keywords = []
        self.saveRawData(rawData)
        self.collocations = self.saveCollocations()
        self.concordances = self.saveConcordances()
        self.saveKeywords()
        self.saveKeywordConcordances()

    def saveRawData(self, rawData):
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f'{self.code}.txt'
        with path.open('w', encoding='utf8') as f:
            print(rawData, file=f)

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
        concordances = {self.collocations[i]: self.rawData.concordance_list(list(self.collocations[i])) for i in
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
        vocabs = self.data.vocab()
        specialWords = defaultdict(dict)
        for word in vocabs:
            relativeFrequency = vocabs[word] / len(self.data) * 10000
            specialWords[word] = {
                f'freq': relativeFrequency
            }
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / 'keywords.txt'
        with path.open('w') as f:
            words = OrderedDict(sorted(specialWords.items(), reverse=True))
            keys = words['end'].keys()
            print('-' * 30, file=f)
            print(f'{self.code:30}', file=f)
            print('-' * 30, file=f)
            print(f'{"word":25}', *[f'{k:10}' for k in keys], sep=' ', file=f)
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
        concordances = {kw: self.rawData.concordance_list(list(kw)) for kw in self.keywords}
        path = self.root / 'keywordConcordances.txt'
        with path.open('w') as f:
            for term in concordances:
                print('-' * 90, file=f)
                print(f'{term}', file=f)
                print('-' * 90, file=f)
                for conc in concordances[term]:
                    print(*conc.left, ' '.join(term).upper(), *conc.right, '\n', file=f)


class Module(Programme):
    def __init__(self, rawData):
        super().__init__(rawData)
