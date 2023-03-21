"""This is an example script demonstrating the basic functionality"""
from pathlib import Path

from keywords import load_keywords_file
from txt_parser import file_factory
from exporter import Exporter


root = Path(__file__).parent.parent
output_path = root / 'output'
import_path = root / "import"
k = import_path /  'keywords.txt'
keywords = load_keywords_file(k)

p = import_path / "0325_Programme_Specification_for_Academics.txt"
m = import_path / "0324_Module_Specification_for_Academics.txt"

for path in [p, m]:
    file = file_factory(path)
    exporter = Exporter(file, output_path)
    exporter.export(keywords)
