# Curriculum analysis

A simple tool for analysing DMU module and programme specifications with respect to provided keywords.

## Installation

Installation is via pip.

```
pip install curriculum_analysis
```

## Usage

Basic usage is via the command line script `curriculum-analysis`.

```
curriculum-analysis <filename> [-c <optional configuration file>]
```

The tool will process the provided file according to the configuration given.
If no configuration is given, then the default configuration will be used.

The default configuration file (`config.cfg`) is placed in the users home directory under a hidden folder `~/.curriculumAnalysis`.

```
[curriculummAnalysis]
keywords_path = ~/.curriculumAnalysis/keywords.txt
outpath = ~/.curriculumAnalysis/output
format = json
```

Changing these values will influence the default settings.

# Example usage

```
curriculum-analysis modules.txt
```

