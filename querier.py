from apalah_parser import ApalahParser
from document import Document


class BooleanModelQuerier:
    documents: 'list[Document]' = None

    def __init__(self, docs: 'list[Document]') -> None:
        self.documents = docs

    def __keyword_to_binary(self, keyword: 'str') -> 'int':
        # Urutan dari bit terkiri (Most important) ke kanan (Least important)
        # Most important adalah dokumen 0
        # Least important adalah dokumen terakhir
        # Menyesuaikan dengan urutan di `self.documents`
        # WARNING! BANYAK BITWISE OPERATION
        # BARU PERTAMA KALI KUPAKE 3 HARI LALU DI RUST
        # DAN NYENTUH BITWISE PERTAMA KALI DI ROBOTEC
        # JANGAN DIBULLY
        a = 0
        for it in self.documents:
            # Masih case sensitive
            found = 0
            if keyword in it.tokenized:
                found = 1
            a = a << 1
            a = a | found
        return a

    def make_boolean_query(self, q: 'str') -> 'str':
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

        return to_eval

    def query(self, q: 'str') -> 'list[Document]':
        to_eval = self.make_boolean_query(q)

        res: 'int' = eval(to_eval)  # DANGER, tapi biar cepet yasudahlah
        print(to_eval, "==>", res)

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
