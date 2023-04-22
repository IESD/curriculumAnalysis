"""This is the main command line interface"""

from configparser import ConfigParser
from pathlib import Path
from argparse import ArgumentParser

from .keywords import load_keywords_file
from .txt_parser import file_factory
from .csv_exporter import CSVExporter
from .json_exporter import JSONExporter

exporters = {
    'csv': CSVExporter,
    'json': JSONExporter,    
}

def main(filename, conf):
    # check the provided config file exists
    conf_path = Path(conf).expanduser()
    if not conf_path.exists():
        print(f"Wait! We are missing the configuration file at {conf_path}")
        default = (Path(__file__).parent / 'config.cfg.default').read_text()
        conf_path.write_text(default);
        print(f"We added this configuration to the file for you.\n")
        print(default)
        print(f"For now, we are aborting.")
        print(f"Please check/edit the configuration before running again.")
        exit()

    # load the config file
    config = ConfigParser()
    config.read(conf_path)

    # Load keywords
    keyword_path = Path(config.get("curriculumAnalysis", "keywords_path")).expanduser()
    if not keyword_path.exists():
        default = (Path(__file__).parent / 'keywords.txt').read_text()
        keyword_path.write_text(default);
        
    keywords = load_keywords_file(keyword_path)

    # load the data
    file = file_factory(Path(filename).expanduser())

    # Generate an analysis
    outpath = Path(config.get("curriculumAnalysis", "outpath")).expanduser()
    format = config.get("curriculumAnalysis", "format")
    exporter = exporters[format](file, outpath)

    # Export it
    exporter.export(keywords)

def cli():
    # The parser accepts a filename and an optional configuration file argument
    parser = ArgumentParser(epilog="For more information see https://github.com/IESD/curriculumAnalysis", description='A simple tool for analysing DMU module and programme specifications with respect to provided keywords.')
    parser.add_argument('filename', help='the file to process')
    parser.add_argument('-c', '--conf', default="~/.curriculumAnalysis/config.cfg", help='configuration file (default ~/.curriculumAnalysis/config.cfg)')
    args = parser.parse_args()
    main(args.filename, args.conf)


if __name__ == "__main__":
    cli()