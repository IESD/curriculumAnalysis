"""This is an example script demonstrating the basic functionality"""
import sys
from configparser import SafeConfigParser

from pathlib import Path

from keywords import load_keywords_file
from txt_parser import file_factory
from csv_exporter import CSVExporter
from json_exporter import JSONExporter


def main(inpath, outpath, keyword_path):
    file = file_factory(inpath)
    keywords = load_keywords_file(keyword_path)
    exporter = JSONExporter(file, outpath)
    exporter.export(keywords)


if __name__ == "__main__":
    assert len(sys.argv) == 2
    config = SafeConfigParser()
    config.read('../config.ini')
    keyword_path = Path(config.get('curriculummAnalysis', 'keywords_path'))
    outpath = Path(config.get('curriculummAnalysis', 'outpath'))
    inpath = Path(sys.argv[1])
    main(inpath, outpath, keyword_path)