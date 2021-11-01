from os import path
from document import Document
from apalah_parser import ApalahParser
import math
import numpy as np



class CosineSim:
    uniq_words: 'set[str]' = None  # Semua kata dalam semua dokumen
    documents: 'list[Document]' = None
    result_docs : 'dict[list]' = {}

    def index(self, _documents: 'list[Document]'):
        #document is passed
        self.documents = _documents

    def query(self, q: 'str') -> 'list[Document]':
        parsed = ApalahParser.parse(q)
        # print("TOKEN: ", parsed.token)

        self.keywords:'list[str]'= []
        for _, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)

        self.result_docs['union_term']  = self.getUnion()
        self.result_docs['term_frequency']  = self.countTermPerDocs()
        self.result_docs['similarity']  = self.similarityByDict()
        
        #buat nyamain print aja
        self.result_docs['term_frequency_v2'] = self.result_docs['term_frequency']
        # print("union_term")
        # print(self.result_docs['union_term'])
        # print("term_frequency")
        # print(self.result_docs['term_frequency'])
        # print("similarity")
        # print(self.result_docs['similarity'])

        return self.result_docs

    def getUnion(self):
        # buat union
        result_dict= []
        for doc in self.documents:
            union_term = set() # Gabungan semua term di query dan doc saat ini
            for word in doc.stemmed:
                union_term.add(word)
            for word in self.keywords:
                union_term.add(word)

            result_dict.append(self.__dictFromSet(union_term))

        return result_dict
            


    def __dictFromSet(self, set: 'set[str]') -> 'dict[str, int]':
        res = {}
        for term in set:
            res[term] = 0
        return res

    def countTermPerDocs(self) -> 'dict[str, int]':
        result_term = []
        for index,docs in enumerate(self.documents):
            docs_term = []
            _docstf = self.result_docs['union_term'][index].copy()
            _keytf = self.result_docs['union_term'][index].copy()

            for word in self.keywords:
                for term in self.result_docs['union_term'][index].keys():
                    if(word==term):
                        _keytf[term] = _keytf[term] + 1
            docs_term.append(_keytf)

            for word in docs.stemmed:
                for term in self.result_docs['union_term'][index].keys():
                    if(word==term):
                        _docstf[term] = _docstf[term] + 1
            docs_term.append(_docstf)

            result_term.append(docs_term)

        return result_term

    def similarityByDict(self) -> 'float':
        similarity_scores = {}
        for index,documents_tf in enumerate(self.result_docs['term_frequency']):
            def matrixByDict(dict):
                res = []
                for term in dict.keys():
                    res.append(dict[term])
                return res

            A = np.array(matrixByDict(documents_tf[0]))
            B = np.array(matrixByDict(documents_tf[1]))

            # A.B / ||A|| ||B||

            similarity_score = A.dot(B)/ (np.linalg.norm(A) * np.linalg.norm(B))
            similarity_scores[self.documents[index].filename] = similarity_score

        cosinesim_result = dict(sorted(similarity_scores.items(), key=lambda item: item[1],reverse=True))
        return cosinesim_result