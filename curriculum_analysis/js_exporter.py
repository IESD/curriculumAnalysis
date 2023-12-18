import json
from pathlib import Path
from distutils.dir_util import copy_tree
import logging
import webbrowser

from .analysis import Analysis

log = logging.getLogger(__name__)

class JSExporter:
    def __init__(self, file, output_path):
        self.file = file
        self.output_path = output_path / file.path.stem
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.data_path = self.output_path / 'data.js'
        self.pages_path = output_path / 'pages.js'

    def export(self, keywords):
        result = []
        for obj in self.file:
            analysis = Analysis(obj)
            analysis.analyse_alternative(keywords)
            record = {
                "code": obj.code,
                "title": obj.full_title,
                "results": analysis.alternative,
                "total": analysis.total,
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
        with self.data_path.open('w', encoding='utf8', errors='surrogateescape') as data_script:
            data_script.write(js_string)
        self.recreate_index()
        log.info(f"See {self.output_path.absolute() / 'index.html'}")
        webbrowser.open(str(self.output_path.absolute() / 'index.html'))    

    def recreate_index(self):
        result = []
        folders = [folder for folder in self.output_path.parent.iterdir() if folder.is_dir()]
        for folder in folders:
            if (folder / 'index.html').exists():
                page = {
                    'title': folder.name,
                    'url': str(Path(folder.name) / 'index.html')
                }
                result.append(page)
        json_string = json.dumps(result)
        js_string = f"""
        async function loadJSON() {{
            return {json_string}
        }}
        """
        copy_tree(str(Path(__file__).parent / 'top-level'), str(self.output_path.parent), update=True)
        with self.pages_path.open('w', encoding='utf8', errors='surrogateescape') as pages_script:
            pages_script.write(js_string)
