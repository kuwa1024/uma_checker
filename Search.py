from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import NgramTokenizer
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm

class Search:
    ix = object
    list = []

    def __init__(self, list):
        # 全文検索前処理
        schema = Schema(index=NUMERIC(stored=True), body=TEXT(stored=True, analyzer=NgramTokenizer(minsize=1,maxsize=4)))
        self.ix = create_in('tmp', schema)
        writer = self.ix.writer()
        for i, v in enumerate(list):
            body = ''
            for b in v['choices']:
                body += b['n'] + ' '
            writer.add_document(index=i, body=body)
        writer.commit()
        self.list = list

    def getWord(self, string):
        with self.ix.searcher () as searcher:
            query = QueryParser('body', self.ix.schema, termclass=FuzzyTerm).parse(string)
            results = searcher.search(query)
            a = []
            for v in results:
                a.append(self.list[v['index']])
            return a