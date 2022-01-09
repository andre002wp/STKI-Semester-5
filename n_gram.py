from os import path
from document import Document
from apalah_parser import ApalahParser
import math



class N_Gram:
    uniq_words: 'set[str]' = None  # Semua kata dalam semua dokumen
    documents: 'list[Document]' = None
    result_docs : 'dict[list]' = {}

    def index(self, _documents: 'list[Document]'):
        #document is passed
        self.documents = _documents

    def query(self, q: 'str',n:'int' = 2) -> 'list[Document]':
        parsed = ApalahParser.parse(q.lower())
        self.keywords:'list[str]'= []
        for i, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)
        self.result_docs['keyword_on_gram'] = self.generate_ngrams(self.keywords, n)
        self.result_docs['document_on_gram'] = self.generate_document_ngrams(self.documents, n)
        self.result_docs['union_docs_gram'] = self.getUnionGram()
        self.result_docs['ngram_similarity'] = self.getNGram()
        self.result_docs['ngram_coef_result'] = self.getNGramCoef()
        # print("keyword_on_gram")
        # print(self.result_docs['keyword_on_gram'])
        # print("document_on_gram")
        # print(self.result_docs['document_on_gram'])
        # print("ngram_union_docs")
        # print(self.result_docs['union_docs_gram'])
        # print("ngram_similarity")
        # print(self.result_docs['ngram_similarity'])
        # print("ngram_coef_result")
        # print(self.result_docs['ngram_coef_result'])
        return self.result_docs


    # output berupa keyword berbentuk n-kata
    def generate_ngrams(self,s: 'str', n:'int')-> 'list[Document]':
        ngrams = zip(*[s[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    def generate_document_ngrams(self, documents: 'list[Document]', n:'int')-> 'list[Document]':
        documents_gram = []
        for document in documents:
            documents_gram.append(self.generate_ngrams(document.tokenized,n))
        return documents_gram

    def getUnionGram(self):
        union_docs = []
        # untuk setiap dokumen
        for i in range(len(self.documents)):
            temp_union = {}
            for key in self.result_docs['keyword_on_gram']:
                temp_union[key] = 1
            for tokens in self.result_docs['document_on_gram'][i]:
                temp_union[tokens] = 1
            union_docs.append(temp_union)
        return union_docs

    def getNGram(self):
        term_Similarity = []
        
        for document in self.result_docs['document_on_gram']:
            temp_TF_d_keyword = {}
            for tokens in document:
                for key in self.result_docs['keyword_on_gram']:
                    if (key == tokens):
                        temp_TF_d_keyword[key] = 1
                            
            term_Similarity.append(temp_TF_d_keyword)
        return term_Similarity

    def getNGramCoef(self):
        _temp_result = {}

        for i,doc in enumerate(self.result_docs['ngram_similarity']):
            _temp_result[self.documents[i].filename] = len(doc)/len(self.result_docs['union_docs_gram'][i])

        #sort
        ngram_result = dict(sorted(_temp_result.items(), key=lambda item: item[1],reverse=True))
        return ngram_result




                    

        


