from os import path
from document import Document
from apalah_parser import ApalahParser
import math



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
        for i, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)

        self.result_docs['term_frequency']  =self.getTF()
        self.result_docs['document_term_matrix'] = self.generateTermMatrix()
        ## todo drimana ni ? disamain
        self.result_docs['cosine_distance'] = self.getCosineDistance(self.result_docs['document_term_matrix'][0],self.result_docs['document_term_matrix'][1])
        # print("term_frequency")
        # print(self.result_docs['term_frequency'])
        # print("document_term_matrix")
        # print(self.result_docs['document_term_matrix'])
        # print("cosine_distance")
        # print(self.result_docs['cosine_distance'])
        return self.result_docs

    def getTF(self):
        term_Frequency = []
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
            term_Frequency.append(temp_TF_d_keyword)
        self.result_docs['term_Frequency'] = term_Frequency
        return term_Frequency

    def generateTermMatrix(self):
        document_matrix=[]
        for i in range(len(self.documents)):
            _temp_matrix = []
            for term in self.result_docs['term_frequency']:
                _temp_matrix.append(term[i])
            document_matrix.append(_temp_matrix)

        return document_matrix

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
            print("a_dot_b")
            print(a_dot_b)
            print("len_a_len_b")
            print(len_a_len_b)
            if(a_dot_b != 0 and len_a_len_b != 0):
                return a_dot_b/len_a_len_b
            else:
                print("zero value exist on cosine coef")
                return 0










                    

        


