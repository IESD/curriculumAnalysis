import json
from pathlib import Path
from distutils.dir_util import copy_tree
import logging

from .analysis import Analysis

log = logging.getLogger(__name__)

class JSExporter:
    def __init__(self, file, output_path):
        self.file = file
        self.output_path = output_path
        self.output_path.mkdir(exist_ok=True)
        self.code_header = f"{self.file.type} code"
        self.name_header = f"{self.file.type} full title"
        self.data_path = self.output_path / 'data.js'

    def export(self, keywords):
        result = []
        for obj in self.file:
            analysis = Analysis(obj)
            analysis.analyse(keywords)
            record = {
                "code": obj.code,
                "title": obj.full_title,
                "data": analysis.results,
                "summary": analysis.summary,
                "raw": analysis.raw()
            }
            result.append(record)
        json_string = json.dumps(result)
        js_string = f"""
        async function loadJSON() {{ 
            return {json_string}; 
        }}
        """
        log.info(f"exporting results as HTML to {self.output_path.absolute()}")
        copy_tree(str(Path(__file__).parent / 'html'), str(self.output_path), update=True)
        with self.data_path.open('w') as data_script:
            data_script.write(js_string)