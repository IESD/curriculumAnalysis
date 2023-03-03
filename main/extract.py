import nltk, string
from collections import defaultdict, OrderedDict
from pathlib import Path

nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('english')
punct = string.punctuation + '“”–‘’—¿•'


def extractData(path, splitString):
    with path.open('r', encoding='utf8') as f:
        data = f.read()
    chunks = data.split(splitString)
    chunks = [ch.splitlines() for ch in chunks]
    # chunks = [[line.strip() for line in ch if line.strip()] for ch in chunks]
    chunks[0] = ['deleteme', '', *chunks[0]]
    chunks = [ch[1:] for ch in chunks][:-1]
    for ch in chunks:
        yield ch


def extractKeywords(path):
    with path.open('r') as f:
        keywords = f.read().split(', ')
        for kw in keywords:
            yield kw


def extractProgrammes(path, outputPath, keywords):
    for ch in extractData(path, 'End of Programme Specification for'):
        yield (Programme(ch, outputPath, keywords))


def extractModules(path, outputPath, keywords):
    for ch in extractData(path, 'End of Module Specification for'):
        yield (Module(ch, outputPath, keywords))


def fragment(data, final):
    result = []
    while not data[0].startswith(final):
        row = data.pop(0).strip()
        if not row:
            continue
        result.append(row)
    return result


class Chunk:
    def __init__(self, data, outputPath, keywords):

        self.rawData = nltk.text.Text([token.lower() for token in data])
        self.data = nltk.text.Text([token.lower() for token in data if token not in punct and token not in sw])
        self.tokens = [word for line in data for sent in nltk.sent_tokenize(line) for word in nltk.word_tokenize(sent)]
        self.rawAgg = nltk.text.Text([token.lower() for token in self.tokens])
        self.agg = nltk.text.Text([token.lower() for token in self.rawAgg if token not in punct and token not in sw])
        self.code = self.rawAgg[2]

        self.root = outputPath / self.code
        self.root.mkdir(parents=True, exist_ok=True)
        self.collocations = self.saveCollocations()
        self.concordances = self.saveConcordances()
        self.keywords = []
        self.saveKeywords(keywords)
        self.saveKeywordConcordances()

    def saveCollocations(self):
        collocations = self.agg.collocation_list(num=10, window_size=30)
        path = self.root / 'collocations.txt'
        with path.open('w') as f:
            print('-' * 30, file=f)
            print(f'{self.code:30}', file=f)
            print('-' * 30, file=f)
            for i in range(10):
                print(f'{" ".join(collocations[i]):30}', file=f)
        return collocations

    def saveConcordances(self):
        concordances = {self.collocations[i]: self.rawAgg.concordance_list(list(self.collocations[i])) for i in
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

    def saveKeywords(self, keywords):
        vocabs = self.agg.vocab()
        specialWords = defaultdict(dict)
        for word in vocabs:
            relativeFrequency = vocabs[word] / len(self.agg) * 10000
            specialWords[word] = {
                f'freq': relativeFrequency
            }
        path = self.root / 'keywords.txt'
        with path.open('w') as f:
            words = OrderedDict(sorted(specialWords.items(), reverse=True))
            try:
                keys = words['work'].keys()
            except KeyError:
                keys = words['year'].keys()
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
        concordances = {kw: self.rawAgg.concordance_list(list(kw)) for kw in self.keywords}
        path = self.root / 'keywordConcordances.txt'
        with path.open('w') as f:
            for term in concordances:
                print('-' * 90, file=f)
                print(f'{term}', file=f)
                print('-' * 90, file=f)
                for conc in concordances[term]:
                    print(*conc.left, ' '.join(term).upper(), *conc.right, '\n', file=f)


class Module(Chunk):
    def __init__(self, data, outputPath, keywords):
        super().__init__(data, outputPath, keywords)

        assert data[3] == "Module Specification"
        assert data[9] == "Module Full Title: "
        assert data[15] == "Module Short Title: "
        assert data[17] == "Module Code: "
        assert data[19] == "Credit Value: "
        assert data[23] == "Credit Level: "
        assert data[29] == "Faculty: "
        assert data[33] == "School: "
        assert data[37] == "Department: "
        assert data[41] == "Module Leader: "
        assert data[45] == "Module Appraiser(s) / Marker(s): "

        self.fullName = data[11]
        self.shortName = data[13]
        self.creditValue = data[21]
        self.creditLevel = data[25]
        self.code = data[27]
        self.faculty = data[31]
        self.school = data[35]
        self.department = data[39]
        self.moduleLeader = data[43]
        data = data[46:]

        self.moduleAppraisers = fragment(data, "Offered at the following sites:")
        assert data[0] == "Offered at the following sites:"
        data = data[1:]

        self.sites = fragment(data, "Semester / Year-long:")
        assert data[0] == "Semester / Year-long: "
        data = data[1:]

        self.intakes = fragment(data, "DMUGlobal Content indicator:")

        assert data[0] == "DMUGlobal Content indicator: "
        assert data[2] in ["Y", "N"]
        self.DMUGlobal = data[2] == "Y"

        assert data[4] == "Ethical approval required: "
        assert data[6] in ["Y", "N"]
        self.ethicalApproval = data[6] == "Y"

        assert data[8] == "Details of Accreditation by Professional, Statutory or Regulatory Body:"
        data = data[9:]
        self.accreditation = fragment(data, "Module Pre-requisites:")
        assert data[0] == "Module Pre-requisites:"
        data = data[1:]

        self.prerequisites = fragment(data, "Module Description:")
        assert data[0] == "Module Description:"
        assert data[3] == "Learning Outcomes:"

        self.description = data[1]
        self.learningOutcomes = data[4]

        assert data[6].strip() == "Evaluation:"

        assessmentKeys = data[7].split('\t')
        data = data[8:]
        assert len(assessmentKeys) == 8
        assessments = fragment(data, "Anonymous marking exemption codes:")
        self.assessments = [{k: v for k, v in zip(assessmentKeys, a.split('\t'))} for a in assessments]
        assert data[0] \
               == "Anonymous marking exemption codes: OPTO1: Individually distinct work; OPTO2: Reflection on " \
                  "development of own work; OPTO3:"

        assert data[3] == "Assessment Notes:"
        self.assessmentNotes = data[4]

        assert data[6] == "Reassessment:"
        self.reassessment = data[7]

        assert data[9] == "Expected Methods of Delivery:"
        self.methodOfDelivery = data[10]

        assert data[12].strip() == "Programmes using this module:"
        programmeKeys = data[15].split('\t')
        data = data[16:]
        programmes = fragment(data, "Remarks:")
        self.programmes = [{k: v for k, v in zip(programmeKeys, p.split('\t'))} for p in programmes]
        assert data == ["Remarks:", "", ""]


class Programme(Chunk):
    def __init__(self, data, outputPath, keywords):

        super().__init__(data, outputPath, keywords)

        assert data[3] == "Programme Specification"
        assert data[9] == "Programme Full Title: "
        assert data[15] == "Programme Short Title: "
        assert data[17] == "Programme Code: "
        assert data[19] == "Programme Type: "

        if (data[25] == "This programme is a joint degree comprising the following areas:	"):
            self.degreeComponents = fragment(data[26:], "This programme")
            for i in range(len(self.degreeComponents) + 2):
                data.pop(25)

        if (data[25] == "This programme has the following specialisations:	"):
            self.specialisations = fragment(data[26:], "This programme")
            for i in range(len(self.specialisations) + 2):
                data.pop(25)

        assert data[27] == "Faculty: "
        assert data[31] == "School: "
        assert data[35] == "Department: "
        assert data[39] == "Programme Leader: "
        assert data[43] == "Mode of Delivery: "
        assert data[45] == "Normal Duration: "

        self.shortName = data[11]
        self.fullName = data[13]
        self.programmeType = data[21]
        self.code = data[23]
        self.faculty = data[29]
        self.school = data[33]
        self.department = data[37]
        self.programmeLeader = data[41]
        self.normalDuration = data[47]
        self.modeOfDelivery = data[49]
        data = data[51:]

        self.sites = fragment(data, "Distance Learning availability: ")
        assert data[0] == "Distance Learning availability: "
        data = data[1:]

        self.distanceLearning = fragment(data, "Awards Available:	")
        assert data[0] == "Awards Available:	"
        data = data[1:]

        self.awards = fragment(data, "Relevant QAA subject benchmarking statement(s):")
        assert data[0] == "Relevant QAA subject benchmarking statement(s):"
        data = data[1:]

        self.benchmarkingStatements = fragment(data, "Accreditation Details:")
        assert data[0] == "Accreditation Details:"
        data = data[1:]

        self.accreditation = fragment(data, "Entry Requirements (General):")
        assert data[0] == "Entry Requirements (General):"
        data = data[1:]

        self.entryRequirements = fragment(data, "Programme Description: Characteristics and Aims")
        assert data[0] == "Programme Description: Characteristics and Aims"

        self.description = data[1]
        self.learningStrategies = data[4]
        self.structureRegulations = data[7]
        self.learningOutcomes = data[10]

        assert data[12].strip() == "Module Details (across all module groups):"
        moduleKeys = data[13].split('\t')
        data = data[14:]
        assert len(moduleKeys) == 9
        modules = fragment(data,
                           "				* for descriptions of these terms/semesters, see other tab				")
        self.modules = [{k: v for k, v in zip(moduleKeys, m.split('\t'))} for m in modules]
        assert data[0].strip() == "* for descriptions of these terms/semesters, see other tab"
        assert data[2] == "Any programme-specific differences or regulations:"
        data = data[3:]
        self.differences = [line for line in data if line]


if __name__ == '__main__':
    root = Path(__file__).parent
    outputPath = root / 'Output'
    k = root / 'keywords.txt'
    keywords = [kw for kw in extractKeywords(k)]
    m = root / 'Modules' / '0324_Module_Specification_for_Academics.txt'
    p = root / 'Programmes' / '0325_Programme_Specification_for_Academics.txt'
    modules = [Module(ch, outputPath, keywords) for ch in extractData(m, 'End of Module Specification for')]
    programmes = [Programme(ch, outputPath, keywords) for ch in extractData(p, 'End of Programme Specification for')]
