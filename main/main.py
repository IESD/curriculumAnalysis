"""This is an example script demonstrating the basic functionality"""
from pathlib import Path
from csv import DictWriter
from collections import defaultdict

from txt_parser import file_factory
from keywords import load_keywords_file
from corpus import Corpus

root = Path(__file__).parent.parent
output_path = root / 'output'
import_path = root / "import"
k = import_path /  'keywords.txt'
keywords = load_keywords_file(k)

def export(file_path):
    data_file = file_factory(file_path)
    path = output_path / f"{data_file.type}s"
    code = f"{data_file.type} code"
    name = f"{data_file.type} full title"
    path.mkdir(exist_ok=True)
    summary_path = path / 'summary.csv'
    with summary_path.open('w') as summary_file:
        summary_csv = DictWriter(summary_file, fieldnames=[code, name, *keywords])
        summary_csv.writeheader()
        for obj in data_file:
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


if __name__ == "__main__":

    p = import_path / "0325_Programme_Specification_for_Academics.txt"
    m = import_path / "0324_Module_Specification_for_Academics.txt"

    export(p)
    export(m)
