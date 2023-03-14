"""This is an example script demonstrating the basic functionality"""
from pathlib import Path
from csv import DictWriter
from collections import defaultdict

from txt_parser import ProgrammeFile, ModuleFile
from keywords import load_keywords_file
from corpus import Corpus

root = Path(__file__).parent.parent
import_path = root / "import"

k = import_path /  'keywords.txt'
keywords = load_keywords_file(k)

p = import_path / "0325_Programme_Specification_for_Academics.txt"
programme_file = ProgrammeFile(p)

m = import_path / "0324_Module_Specification_for_Academics.txt"
module_file = ModuleFile(m)

output_path = root / 'output'

programme_path = output_path / 'programmes'
module_path = output_path / 'modules'
# programme_path.mkdir(exist_ok=True)
# summary_path = output_path / 'programmes.csv'

def export(path, objects, code, name):
    path.mkdir(exist_ok=True)
    summary_path = path / 'summary.csv'
    with summary_path.open('w') as summary_file:
        summary_csv = DictWriter(summary_file, fieldnames=[code, name, *keywords])
        summary_csv.writeheader()
        for obj in objects:
            detail_path = path / f"{obj.code}.txt"
            summary = defaultdict(int)
            summary[code] = obj.code
            summary[name] = obj.full_title
            with detail_path.open('w') as detail_file:
                for section, text in obj.corpora().items():
                    corpus = Corpus(section, text)
                    results = corpus.analyse(keywords)
                    for r in results:
                        summary[r.keyword] += r.count
                        if r.count:
                            msg = f'found keyword "{r.keyword}" {r.count} times in "{section}"'
                            print(f"{'='*len(msg)}\n{msg}\n{'='*len(msg)}\n", file=detail_file)
                            print("\n\n".join([f"'{c}'" for c in r.concordances]), "\n", file=detail_file)
                summary_csv.writerow(summary)

# export(programme_path, programme_file.programmes(), 'programme code', 'programme full title')
# export(module_path, module_file.modules(), 'module code', 'module full title')

def extract(path, programme_output=programme_path, module_output=module_path):
    with path.open('r', encoding='utf8') as file:
        header = file.readlines()[2].strip()
    if header == "Module Specification":
        export(module_output, ModuleFile(path).modules(), 'module code', 'module full title')
    else:
        export(programme_output, ProgrammeFile(path).programmes(), 'programme code', 'programme full title')

extract(p)
extract(m)
