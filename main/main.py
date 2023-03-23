"""This is an example script demonstrating the basic functionality"""
import sys

from pathlib import Path

from keywords import load_keywords_file
from txt_parser import file_factory
from exporter import Exporter

def main(inpath, outpath, keyword_path):
    file = file_factory(inpath)
    keywords = load_keywords_file(keyword_path)
    exporter = Exporter(file, outpath)
    exporter.export(keywords)


if __name__ == "__main__":
    print(sys.argv)
    assert len(sys.argv) == 4
    main(*[Path(p) for p in sys.argv[1:]])