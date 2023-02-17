from pathlib import Path

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
    def __init__(self, tokens):
        self.tokens = tokens
        self.code = tokens[2]
        self.root = Path('data', f'{self.code}')
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f'{self.code}.txt'
        with path.open('w') as f:
            print(self.tokens, file=f)

    #save high frequency words
    #save collocations
    #save keyword concordances

class Module:
    def __init__(self, tokens):
        self.tokens = tokens