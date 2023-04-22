import json
from pathlib import Path
from distutils.dir_util import copy_tree

from .analysis import Analysis

class JSONExporter:
    def __init__(self, file, output_path):
        self.file = file
        self.output_path = output_path
        self.output_path.mkdir(exist_ok=True)
        self.code_header = f"{self.file.type} code"
        self.name_header = f"{self.file.type} full title"
        self.summary_path = self.output_path / 'summary.json'

    def export(self, keywords):
        result = []
        for obj in self.file:
            analysis = Analysis(obj)
            analysis.analyse(keywords)
            record = {
                "code": obj.code,
                "title": obj.full_title,
                "data": analysis.results
            }
            result.append(record)
        with self.summary_path.open('w') as summary_file:
            json.dump(result, summary_file)
        copy_tree(str(Path(__file__).parent / 'html'), str(self.output_path), update=True)