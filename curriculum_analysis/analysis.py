from collections import defaultdict

from .corpus import Corpus


class Analysis:
    def __init__(self, obj):
        self.corpora = {section: Corpus(section, text) for section, text in obj.corpora().items()}
        self.results = {}
        self.summary = defaultdict(int)

    def analyse(self, keywords, **kwargs):
        for kw in keywords:
            result = self.check_for_keyword(kw, **kwargs)
            self.results[kw] = result
            for section in result:
                self.summary[kw] += len(result[section])

    def check_for_keyword(self, keyword, **kwargs):
        return {
            section: c.delemmatized_concordance_list(keyword, **kwargs) 
            for section, c in self.corpora.items()
        }