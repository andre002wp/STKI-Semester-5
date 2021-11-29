from os import path
from document import Document
from apalah_parser import ApalahParser
import math
import numpy as np



class DROPT:
    uniq_words: 'set[str]' = None  # Semua kata dalam semua dokumen
    documents: 'list[Document]' = None
    result_docs : 'dict[list]' = {}

    def index(self, _documents: 'list[Document]'):
        #document is passed
        self.documents = _documents

    def query(self, q: 'str') -> 'list[Document]':
        parsed = ApalahParser.parse(q)

        self.keywords:'list[str]'= []
        for _, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)

        self.result_docs['term_frequency']  =self.getTF()
        self.result_docs['document_corpus'] = self.document_corpus()
        self.result_docs['weight_matrix'] = self.weight_matrix()
        print("term_frequency")
        print(self.result_docs['term_frequency'])
        # print("document_corpus")
        # print(self.result_docs['document_corpus'])
        print("weight_matrix")
        print(self.result_docs['weight_matrix'])
        return self.result_docs


    def getTF(self):
        # is this a dict of weight or frekuensi kemunculan term dan weight im so confused
        term_Frequency = {}
        for key in self.keywords:
            _keycount = 0
            for term in self.keywords:
                if(key == term):
                  _keycount+=1 
            term_Frequency[key] = [_keycount,1]
        return term_Frequency

    def document_corpus(self):
        document_corpus = []
        _term_weight = self._IDF()
        _document_matrix= self._getdocument_matrix()
        for i in range(len(self.documents)):
            _temp_matrix = {}
            for key in _term_weight[i].keys():
                _temp_matrix[key] = _term_weight[i][key]*_document_matrix[i][key]
            document_corpus.append(_temp_matrix)
        return document_corpus
    
    def _getdocument_matrix(self):
        documents_matrix = []
        for document in self.documents:
            _document_items = {}
            for tokens in document.stemmed:
                if(tokens not in _document_items.keys()):
                    _tempcount=0
                    for _word in document.stemmed:
                        if(tokens == _word):
                            _tempcount+=1
                    _document_items[tokens] = _tempcount
            documents_matrix.append(_document_items)
        return documents_matrix

    def _IDF(self):
        idf_dict=[]
        for document in self.documents:
            _document_corpus = {}
            n=len(document.stemmed)
            for tokens in document.stemmed:
                if(tokens not in _document_corpus.keys()):
                    _tempcount=0
                    for _word in document.stemmed:
                        if(tokens == _word):
                            _tempcount+=1
                        _document_corpus[tokens]=(math.log((1+n)/(_tempcount+1)))+1
            idf_dict.append(_document_corpus)
        return idf_dict

    def weight_matrix(self):
        weight_matrix = []
        for i in range(len(self.documents)):
            _tempweight = {}
            for term,value in self.result_docs['term_frequency'].items():
                if(term in self.result_docs['document_corpus'][i].keys()):
                    _tempweight[term] = self.result_docs['document_corpus'][i][term]*value[0]*value[1] # value[0] itu jumlahnya di keyword, value[1] ni weight yang awalnya di set 1
            weight_matrix.append(_tempweight)
        return weight_matrix
