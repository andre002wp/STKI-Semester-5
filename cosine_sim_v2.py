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
        print("TOKEN: ", parsed.token)

        keywords:'list[str]'= []
        for _, token in enumerate(parsed.token):
            if not token.is_symbol:
                keywords.append(token.token)

          
        result: 'dict[Document, float]' = {} # Nilai similarity di kanan

        # buat union
        for doc in self.documents:
            union_term = set() # Gabungan semua term di query dan doc saat ini
            for word in doc.stemmed:
                union_term.add(word)
            for word in keywords:
                union_term.add(word)

            similarity_dict = self.__dictFromSet(union_term)
            # print(similarity_dict)

            a = self.countTermPerDict(similarity_dict.copy(), keywords)
            # print(a, b, self.similarityByDict)

            b = self.countTermPerDict(similarity_dict.copy(), doc.stemmed)
            # print("a")
            # print(a)
            # print("b")
            # print(b)
            result[doc] = self.similarityByDict(a, b)
        

        return result
            


    def __dictFromSet(self, set: 'set[str]') -> 'dict[str, int]':
        res = {}
        for term in set:
            res[term] = 0
        return res

    # Input dict {anthony: 0, brutus: 0} query "[anthony, anthony, brutus]" hasil "[anthony: 2, brutus: 1]"
    def countTermPerDict(self, dict: 'dict[str, int]', query: 'list[str]') -> 'dict[str, int]':
        res = dict.copy()
        for key in dict.keys():
            # Hanya untuk mencegah error
            if dict[key] != 0:
                raise Exception("Pastikan dictionary dimulai dari 0")

        for term in query:
            res[term] = res[term] + 1
        return res

    def similarityByDict(self, a: 'dict[str, int]', b: 'dict[str, int]') -> 'float':
        if set(a.keys()) != set(b.keys()):
            raise Exception("Keys a dan b haruslah sama")
        
        def matrixByDict(dict):
            res = []
            for term in dict.keys():
                res.append(dict[term])
            return res
        
        A = np.array(matrixByDict(a))
        B = np.array(matrixByDict(b))

        # A.B / ||A|| ||B||

        similarity_scores = A.dot(B)/ (np.linalg.norm(A) * np.linalg.norm(B))
        return similarity_scores

        # self.result_docs['term_frequency']  =self.getTF()
        # self.result_docs['document_term_matrix'] = self.generateTermMatrix()
        # ## todo drimana ni ? disamain
        # self.result_docs['cosine_distance'] = self.getCosineDistance(self.result_docs['document_term_matrix'][0],self.result_docs['document_term_matrix'][1])
        # print("term_frequency")
        # print(self.result_docs['term_frequency'])
        # print("document_term_matrix")
        # print(self.result_docs['document_term_matrix'])
        # print("cosine_distance")
        # print(self.result_docs['cosine_distance'])
        # return self.result_docs


    # def getTF(self):
    #     term_Frequency = []
    #     for key in self.keywords:
    #         temp_TF_d_keyword = []
    #         for document in self.documents:
    #             term_count = 0
    #             for tokens in document.stemmed:
    #                 if (key == tokens):
    #                     term_count +=1
    #             if (term_count == 0):
    #                 temp_TF_d_keyword.append(0)
    #             else:
    #                 temp_TF_d_keyword.append(term_count)
    #         term_Frequency.append(temp_TF_d_keyword)
    #     self.result_docs['term_Frequency'] = term_Frequency
    #     return term_Frequency

    # def generateTermMatrix(self):
    #     document_matrix=[]
    #     for i in range(len(self.documents)):
    #         _temp_matrix = []
    #         for term in self.result_docs['term_frequency']:
    #             _temp_matrix.append(term[i])
    #         document_matrix.append(_temp_matrix)

    #     return document_matrix

    # def getCosineDistance(self,key_matrix_a,key_matrix_b):
    #     if(len(key_matrix_a)!= len(key_matrix_b)):
    #         return -1
    #     else:
    #         a_dot_b = 0
    #         for term_idx in range(len(key_matrix_a)):
    #             a_dot_b += key_matrix_a[term_idx]*key_matrix_b[term_idx]

    #         len_matrix_a = 0
    #         len_matrix_b = 0
    #         for term_idx in range(len(key_matrix_a)):
    #             len_matrix_a += key_matrix_a[term_idx]*key_matrix_a[term_idx]
    #             len_matrix_b += key_matrix_b[term_idx]*key_matrix_b[term_idx]

    #         len_a_len_b = math.sqrt(len_matrix_a*len_matrix_b)
    #         if(a_dot_b != 0 and len_a_len_b != 0):
    #             return a_dot_b/len_a_len_b
    #         else:
    #             print("zero value exist on cosine coef")
    #             return 0
