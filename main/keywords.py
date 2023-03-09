from pathlib import Path
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def load_keywords_file(p=Path('keywords.txt')):
    with p.open('r') as f:
        keywords = [kw.lower() for kw in f.read().splitlines()]
        return list(set(stemmer.stem(kw) for kw in keywords))
