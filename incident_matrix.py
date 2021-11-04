from os import path
from apalah_parser import ApalahParser
from document import Document
import re
from querier import BooleanModelQuerier

# MAKE TOKENIZED sebelum di stem dkk

USE_FILENAME_INSTEAD_ID = True


class BooleanModelIncidentMatrix:  # Incident Matrix
    uniq_words: 'set[str]' = None  # Semua kata dalam semua dokumen
    documents: 'list[Document]' = None

    #         doc0   doc1    doc2
    # kata1    1        0       1
    # kata2    0        0       1
    incident_matrix: 'dict[str, list[int]]'  # Format diatas jadinya adalah
    # {"kata1": [0, 2], "kata2": [2]} index memakai index di `self.documents`

    def index(self, _documents: 'list[Document]'):
        self.documents = _documents
        self.uniq_words = set()
        self.incident_matrix = dict()

        for it in self.documents:
            for word in it.tokenized:
                self.uniq_words.add(word)

        for word in self.uniq_words:
            foundIndex: list[int] = []
            for doci, doc in enumerate(self.documents):
                if word in doc.tokenized:  # MASIH PAKE TOKENIZED SEBELUM STEM DKK
                    foundIndex.append(doci)

            self.incident_matrix[word] = foundIndex

    # Helper function
    def __keyword_to_binary(self, keyword: 'str') -> 'int':
        # Urutan dari bit terkiri (Most important) ke kanan (Least important)
        # Most important adalah dokumen 0
        # Least important adalah dokumen terakhir
        a = 0
        for bit in reversed(self.incident_matrix[keyword]):
            a = a << 1
            a = a | bit

        return a

    def query(self, q: 'str') -> 'list[Document]':
        if self.incident_matrix == None:
            raise Exception("Lakukan indexing sebelum mengquery")

        # region Parsing Query
        parsed = ApalahParser.parse(q)
        for i, token in enumerate(parsed.token):
            if not token.is_symbol:
                b = self.__keyword_to_binary(token.token)
                # print(token, bin(b))
                parsed.token[i].set_binary(b)

        to_eval = ""
        for it in parsed.token:
            if it.is_symbol:
                to_eval += it.token
            else:
                to_eval += f" {bin(it.binary)} "

        if to_eval == "":
            print("Invalid query")
            return
        # endregion

        # region Actual Querying
        res: 'int' = eval(to_eval)  # DANGER, tapi biar cepet yasudahlah
        print("Incident Matrix::", to_eval, "==>", res)

        result_docs: 'list[Document]' = []
        # Kenapa reversed?
        # Karena di `__keyword_to_binary`, index 0 ada di most important bit
        # sedangkan ketika mereturn, kita mulai dari bit terkanan
        # Biar konsisten index 0 ada dikiri, kita reverse aja
        for i, doc in enumerate(reversed(self.documents)):
            keyword_in_doc: 'int' = res & 1  # Bisa 0, atau bisa 1. Kek bool
            if keyword_in_doc == 1:
                result_docs.append(doc)
            res = res >> 1

        return result_docs
        # endregion


# bukan | (adalah & sama)

# bukan | (satunya & sama)
# 010 | (001 & 011) = 010 | 001 = 011 = 3

# brutus & caesar & ~calpurnia
# brutus | caesar & ~calpurnia
