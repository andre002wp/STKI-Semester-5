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

        self.keywords:'list[str]'= []
        for _, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)

        self.result_docs['term_frequency']  =self.getTF()
        self.result_docs['keyword_term_matrix'] = self.generateKeyMatrix()
        self.result_docs['document_term_matrix'] = self.generateTermMatrix()
        ## todo drimana ni ? disamain
        self.result_docs['cosine_coef'] = self.getCosineCoef()
        print("term_frequency")
        print(self.result_docs['term_frequency'])
        print("keyword_term_matrix")
        print(self.result_docs['keyword_term_matrix'])
        print("document_term_matrix")
        print(self.result_docs['document_term_matrix'])
        print("cosine_coef")
        print(self.result_docs['cosine_coef'])
        return self.result_docs


    def getTF(self):
        term_Frequency = {}
        for key in self.keywords:
            temp_TF_d_keyword = []
            for document in self.documents:
                term_count = 0
                for tokens in document.stemmed:
                    if (key == tokens):
                        term_count +=1
                if (term_count == 0):
                    temp_TF_d_keyword.append(0)
                else:
                    temp_TF_d_keyword.append(term_count)
            term_Frequency[key] = temp_TF_d_keyword
        return term_Frequency

    def generateKeyMatrix(self):
        key_matrix=[]
        for key,item in self.result_docs['term_frequency'].items():
            _tempcount = 0
            for word in self.keywords:
                if(key == word):
                    _tempcount +=1
            key_matrix.append(_tempcount)
        print("key_matrix")
        print(key_matrix)
        return key_matrix

    def generateTermMatrix(self):
        document_matrix=[]
        for i in range(len(self.documents)):
            _temp_matrix = []
            for term,value in self.result_docs['term_frequency'].items():
                _temp_matrix.append(value[i])
            document_matrix.append(_temp_matrix)
        return document_matrix

    def getCosineCoef(self):
        cosine_coef = []
        for docs in self.result_docs['document_term_matrix']:
            _tmpcosineVal = self.getCosineDistance(self.result_docs['keyword_term_matrix'],docs)
            cosine_coef.append(_tmpcosineVal)
        return cosine_coef

    def getCosineDistance(self,key_matrix_a,key_matrix_b):
        if(len(key_matrix_a)!= len(key_matrix_b)):
            return -1
        else:
            a_dot_b = 0
            for term_idx in range(len(key_matrix_a)):
                a_dot_b += key_matrix_a[term_idx]*key_matrix_b[term_idx]

            len_matrix_a = 0
            len_matrix_b = 0
            for term_idx in range(len(key_matrix_a)):
                len_matrix_a += key_matrix_a[term_idx]*key_matrix_a[term_idx]
                len_matrix_b += key_matrix_b[term_idx]*key_matrix_b[term_idx]

            len_a_len_b = math.sqrt(len_matrix_a*len_matrix_b)
            if(a_dot_b != 0 and len_a_len_b != 0):
                return a_dot_b/len_a_len_b
            else:
                print("zero value exist on cosine coef")
                return 0
