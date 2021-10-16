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

    def query(self, q: 'str',n:'int') -> 'list[Document]':
        parsed = ApalahParser.parse(q)
        self.keywords:'list[str]'= []
        for i, token in enumerate(parsed.token):
            if not token.is_symbol:
                self.keywords.append(token.token)
        self.result_docs['keyword_on_gram'] = self.generate_ngrams(self.keywords, n)
        self.result_docs['document_on_gram'] = self.generate_document_ngrams(self.documents, n)
        self.result_docs['ngram_sentence_result'] = self.getNGram()
        self.result_docs['ngram_coef_result'] = self.getNGramCoef()
        return self.result_docs

    def generate_document_ngrams(self, documents: 'list[Document]', n:'int')-> 'list[Document]':
        documents_gram = []
        for document in documents:
            documents_gram.append(self.generate_ngrams(document.tokenized,n))
        return documents_gram


    # output berupa keyword berbentuk n-kata
    def generate_ngrams(self,s: 'str', n:'int')-> 'list[Document]':
        ngrams = zip(*[s[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    def getNGram(self):
        ngram_result = []
        for document in self.result_docs['document_on_gram']:
            result_temp=[]
            for doc_sentence in document:
                for key_sentence in self.result_docs['keyword_on_gram']:
                    if(doc_sentence == key_sentence):
                        result_temp.append(key_sentence)
            ngram_result.append(result_temp)
        print(ngram_result)
        return ngram_result



                    

        


