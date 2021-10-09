from os import path
from document import Document
from apalah_parser import ApalahParser
import math



class TF_IDF:
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
        self.result_docs['keyword'] = self.keywords

        self.term_Frequency: 'list[int]' = self.getTF()
        self.document_Frequency: 'list[int]'  = self.getDF(self.term_Frequency)
        self.d_over_df: 'list[float]'  = self.getD_over_Df(self.document_Frequency)
        self.idf: 'list[float]' = self.getIDF(self.document_Frequency,self.d_over_df)
        self.idf_plus: 'list[float]' = self.getIDF_plus(self.idf)
        self.Weight: 'list[float]' = self.getWeight(self.term_Frequency,self.idf_plus)
        self.totalWeight:'list[float]' = self.getTotal(self.Weight)
        self.result = self.getRelevance(self.totalWeight)
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

    def getDF(self,term_Frequency):
        document_Frequency = []
        for key_frequency in term_Frequency:
            count = 0
            for frequency in key_frequency:
                if (frequency>0):
                    count += 1
            document_Frequency.append(count)
        self.result_docs['document_Frequency'] = document_Frequency
        return document_Frequency

    def getD_over_Df(self,document_Frequency):
        D_over_df = []
        for keys in document_Frequency:
            try:
                D_over_df.append(len(self.documents)/keys)
            except:
                D_over_df.append(0)
        self.result_docs['d_over_df'] = D_over_df
        return D_over_df

    def getIDF(self,document_Frequency,d_over_df):
        idf_keys = []
        for i,keys in enumerate(document_Frequency):
            try:
                idf_keys.append(math.log(d_over_df[i],10))
            except:
                idf_keys.append(0)
        self.result_docs['idf'] = idf_keys
        return idf_keys
        
    def getIDF_plus(self,idf_value):
        idf_plus = []
        for num in idf_value:
            idf_plus.append(num+1)
        self.result_docs['idf_plus'] = idf_plus
        return idf_plus

    def getWeight(self,term_Frequency,idf_plus):
        Weight_keys = []
        for i,keys in enumerate(term_Frequency):
            temp_weight_for_key_in_doc = []
            for document in keys:
                temp_weight_for_key_in_doc.append(document*idf_plus[i])
            Weight_keys.append(temp_weight_for_key_in_doc)
        self.result_docs['weight_keys'] = Weight_keys
        return Weight_keys

    def getTotal(self,document_weight):
        total = []
        for i,weight in enumerate(document_weight):
            if(i==0): # how do you declare 3int list then update the num
                for num_single_weight in weight:
                    total.append(num_single_weight)
            else:
                for j,num_single_weight in enumerate(weight):
                    total[j]+=num_single_weight
            print(total)
        self.result_docs['Toootalsss'] = total
        return total

    def getRelevance(self,total):
        relevance = []
        maxscore = max(total)
        
        # for i,document_weight in self.result_docs['Toootalsss']:# cannot unpack shit
        if(maxscore>0):
            for i in range(len(total)):
                if(self.result_docs['Toootalsss'][i]==maxscore):
                    relevance.append(self.documents[i].filename)
        else:
            relevance.append("None of the documents is relevant")
        

        relevance_to_text = ""
        for doc in relevance:
            relevance_to_text +=  doc + " "

        self.result_docs['most_relevance'] = relevance_to_text
        return relevance

        


