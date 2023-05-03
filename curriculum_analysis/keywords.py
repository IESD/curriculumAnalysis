from pathlib import Path
import logging

log = logging.getLogger(__name__)

def load_keywords_file(p=Path('keywords.txt')):
    log.info(f"loading keywords from {p.absolute()}")
    with p.open('r', encoding='utf8', errors='surrogateescape') as f:
        return [kw.lower() for kw in f.read().splitlines()]
