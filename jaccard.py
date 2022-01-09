from os import path
from document import Document
from apalah_parser import ApalahParser
import math



class Jaccard:
    uniq_words: 'set[str]' = None  # Semua kata dalam semua dokumen
    documents: 'list[Document]' = None
    result_docs : 'dict[list]' = {}

    def index(self, _documents: 'list[Document]'):
        #document is passed
        self.documents = _documents

    def query(self, q: 'str') -> 'list[Document]':
        parsed = ApalahParser.parse(q.lower())
        self.keywords:'list[str]'= []
        for i, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)
        self.result_docs['keyword'] = self.keywords
        self.result_docs['term_Similarity'] = self.check_Similarity()
        self.result_docs['union_docs'] = self.getUnion()
        self.result_docs['jaccard_coef_result'] = self.jaccard_coeficient() #todo use .intersection() easier

        # print("keyword")
        # print(self.result_docs['keyword'])
        # print("term_Similarity")
        # print(self.result_docs['term_Similarity'])
        # print("union_docs")
        # print(self.result_docs['union_docs'])
        # print("jaccard_coef_result")
        # print(self.result_docs['jaccard_coef_result'])
        return self.result_docs

    def jaccard_coeficient(self):
        _temp_result = {}
        for i,doc in enumerate(self.result_docs['term_Similarity']):
            _temp_result[self.documents[i].filename] = len(doc)/len(self.result_docs['union_docs'][i])

        #sort
        jaccard_coef = dict(sorted(_temp_result.items(), key=lambda item: item[1],reverse=True))
        return jaccard_coef

    def check_Similarity(self):
        term_Similarity = []
        
        for document in self.documents:
            temp_TF_d_keyword = {}
            for tokens in document.stemmed:
                for key in self.keywords:
                    if (key == tokens):
                        temp_TF_d_keyword[key] = 1
                            
            term_Similarity.append(temp_TF_d_keyword)
        return term_Similarity
        
    def getUnion(self):
        union_docs = []
        for document in self.documents:
            temp_union = {}
            for tokens in document.stemmed:
                temp_union[tokens] = 1
            for key in self.keywords:
                temp_union[key] = 1
            union_docs.append(temp_union)
        return union_docs
                    

        


