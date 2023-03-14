from pathlib import Path

def load_keywords_file(p=Path('keywords.txt')):
    with p.open('r') as f:
        return [kw.lower() for kw in f.read().splitlines()]
