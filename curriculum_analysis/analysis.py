from collections import defaultdict
import logging

from .corpus import Corpus

log = logging.getLogger(__name__)

class Analysis:
    def __init__(self, obj):
        self.name = str(obj)
        self.corpora = {section: Corpus(section, text) for section, text in obj.corpora().items()}
        self.results = {}
        self.alternative = {}
        self.summary = defaultdict(int)
        self.total = 0

    def analyse(self, keywords, **kwargs):
        self.keywords = keywords
        for kw in keywords:
            result = self.check_for_keyword(kw, **kwargs)
            self.results[kw] = result
            for section in result:
                self.summary[kw] += len(result[section])
        self.total = sum(self.summary.values())
        if self.total:
            log.debug(f"found '{self.total}' keywords in {self.name}")

    def analyse_alternative(self, keywords):
        for section, corpus in self.corpora.items():
            keyword_indices = {
                keyword: corpus.find_indices(keyword) for keyword in keywords
            }
            total = sum([len(indices) for _, indices in keyword_indices.items()])
            self.alternative[section] = {
                "tokens": corpus.tokens,
                "keywords": keyword_indices,
                "total": total,
            }
            self.total += total 


    def check_for_keyword(self, keyword, **kwargs):
        return {
            section: c.delemmatized_concordance_list(keyword, **kwargs) 
            for section, c in self.corpora.items()
        }

    def raw(self):
        return {section: self.corpora[section].raw_string for section in self.corpora.keys()}