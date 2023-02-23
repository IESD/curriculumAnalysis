from pathlib import Path

def extractData(path, split_string):
    with path.open('r', encoding='utf8') as f:
        data = f.read();
        chunks = data.split(split_string)
        chunks = [ch.splitlines() for ch in chunks]
        chunks = [[line.strip() for line in ch if line.strip()] for ch in chunks]
        chunks[0] = ['deleteme', *chunks[0]]
        chunks = [ch[1:] for ch in chunks][:-1]
        for chunk in chunks:
            yield chunk

def extractProgrammes(path):
    for chunk in extractData(path, 'End of Programme Specification for'):
        yield(Programme(chunk))

def extractModules(path):
    for chunk in extractData(path, 'End of Programme Specification for'):
        yield(Programme(chunk))


class Module:
    def __init__(self, data):
        self.code = data[1]
        self.name = data[4]

class Programme:
    def __init__(self, data):
        self.data = data

root = Path(__file__).parent.parent / "import"
m = root / "0324_Module_Specification_for_Academics.txt"
p = root / "0325_Programme_Specification_for_Academics.txt"
modules = [Module(ch) for ch in extractData(m, 'End of Module Specification for')]
programmes = [Programme(ch) for ch in extractData(p, 'End of Programme Specification for')]

print([m.data[4] for m in modules])

print(modules[0].data)