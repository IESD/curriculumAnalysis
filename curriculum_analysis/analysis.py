from collections import defaultdict
import logging

from .corpus import Corpus

log = logging.getLogger(__name__)

class Analysis:
    def __init__(self, obj):
        self.name = str(obj)
        self.corpora = {section: Corpus(section, text) for section, text in obj.corpora().items()}
        self.results = {}
        self.summary = defaultdict(int)

    def analyse(self, keywords, **kwargs):
        for kw in keywords:
            result = self.check_for_keyword(kw, **kwargs)
            self.results[kw] = result
            for section in result:
                self.summary[kw] += len(result[section])
        if sum(self.summary.values()):
            log.debug(f"found '{sum(self.summary.values())}' keywords in {self.name}")

    def check_for_keyword(self, keyword, **kwargs):
        return {
            section: c.delemmatized_concordance_list(keyword, **kwargs) 
            for section, c in self.corpora.items()
        }
    
    def raw(self):
        return {section: self.corpora[section].raw_string for section in self.corpora.keys()}