from os import path
from document import Document
from apalah_parser import ApalahParser
import math
import numpy as np



class VSM:
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

        self.result_docs['document_Dict'] = self._getDocumentDict()
        self.result_docs['document_TF'] = self.documentTF()
        self.result_docs['document_frequency'],self.result_docs['document_idf'] = self.document_idf()
        self.result_docs['document_weight'],self.result_docs['document_distance'] = self.DocumentWeight()
        self.result_docs['query_TF'] = self.QueryTF()
        self.result_docs['query_weight'],self.result_docs['query_distance'] = self.QueryWeight()
        #perhitungan similarity
        self.result_docs['weight_Dj_query'],self.result_docs['sum_Dj_query'] = self.WeightDjQ()
        self.result_docs['distance_Dj_query'] = self.DistanceDjQ()
        self.result_docs['similarity'] = self.getSimilarity()
        # print("weight_Dj_query")
        # print(self.result_docs['weight_Dj_query'])
        # print("document_TF")
        # print(self.result_docs['document_TF'])
        return self.result_docs

    def _getDocumentDict(self):
        document_dict = {}
        for document in self.documents:
            for token in document.stemmed:
                if(token not in document_dict.keys()):
                    document_dict[token] = document_dict
        return document_dict

    def documentTF(self):
        document_dict = self.result_docs['document_Dict']
        documentTF = []
        for document in self.documents:
            _tmpcurrentdoc = {}
            for term in document_dict.keys():
                count = 0
                for tokens in document.stemmed:
                    if(term == tokens):
                        count+=1
                _tmpcurrentdoc[term]=count
            documentTF.append(_tmpcurrentdoc)        
        return documentTF

    def document_idf(self):
        document_frequency = {}
        for term in self.result_docs['document_Dict'].keys():
            count = 0
            for document in self.result_docs['document_TF']:
                if(document[term]>0):
                    count+=1
            document_frequency[term]= count
        
        document_idf = {}
        for term in self.result_docs['document_Dict'].keys():
            document_idf[term] = math.log(len(self.documents)/document_frequency[term])
        return document_frequency,document_idf

    def DocumentWeight(self):
        documents_weight = []
        self.result_docs['document_TF']
        self.result_docs['document_idf']
        for document in self.result_docs['document_TF']:
            _document_weight = {}
            for term in self.result_docs['document_Dict'].keys():
                _document_weight[term] = document[term] * self.result_docs['document_idf'][term]
            documents_weight.append(_document_weight)

        sum_document_weight = []
        for document in documents_weight:
            _sum = 0
            for _,value in document.items():
                _sum += value*value
            _sum = math.sqrt(_sum)
            sum_document_weight.append(_sum)
        return documents_weight,sum_document_weight

    def QueryTF(self):
        queryTF = {}
        for term in self.result_docs['document_Dict'].keys():
            count = 0
            for token in self.keywords:
                if(term == token):
                    count+=1
            queryTF[term]=count
        return queryTF

    def QueryWeight(self):
        query_weight = {}
        max_tf_value = max(self.result_docs['query_TF'].values())
        for term,values in self.result_docs['query_TF'].items():
            for key in self.result_docs['document_Dict'].keys():
                query_weight[term] = (values/max_tf_value) * self.result_docs['document_idf'][key]

        sum_query_weight = 0
        for value in query_weight.values():
            sum_query_weight += value*value
        sum_query_weight = math.sqrt(sum_query_weight)
        return query_weight,sum_query_weight

    def WeightDjQ(self):
        weight_DjQ = []
        for document in self.result_docs['document_weight']:
            _tempDjDoc = {}
            for term,value in document.items():
                _tempDjDoc[term] = value*self.result_docs['query_weight'][term]
            weight_DjQ.append(_tempDjDoc)

        sum_DjQ = []
        for document in weight_DjQ:
            _sum = 0
            for _,value in document.items():
                _sum += value*value
            _sum = math.sqrt(_sum)
            sum_DjQ.append(_sum)
        return weight_DjQ,sum_DjQ

    def DistanceDjQ(self):
        DjQ_distance = []
        for document_distance in self.result_docs['document_distance']:
            DjQ_distance.append(document_distance*self.result_docs['query_distance'])
        return DjQ_distance

    def getSimilarity(self):
        similarity = {}
        for index,values in enumerate(zip(self.result_docs['sum_Dj_query'],self.result_docs['distance_Dj_query'])):
            similarity[self.documents[index].filename] = values[0]/values[1]

        vsm_result = dict(sorted(similarity.items(), key=lambda item: item[1],reverse=True))
        return vsm_result
            
        



        
    
            



