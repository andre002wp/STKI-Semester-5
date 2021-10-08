from os import path
from document import Document


# MAKE TOKENIZED sebelum di stem dkk

USE_FILENAME_INSTEAD_ID = True


class InvertedIndexRow:
    id_file: int = None
    filename: str = None
    path: str = None

    keyword_freq: int = 0  # Seberapa kali muncul
    keyword_pos: list[int] = None  # Lokasi keyword di file

    @staticmethod
    def from_keyword(id: int, keyword: str, doc: Document, name="-", filepath="-") -> 'InvertedIndexRow':
        l: list[int] = []
        # !!!! DISINI MAKE SEBELUM DI STEM DKK
        for i, word in enumerate(doc.tokenized):
            if word == keyword:
                l.append(i)

        d = InvertedIndexRow()
        d.id_file = id
        d.filename = name
        d.path = filepath
        d.keyword_freq = len(l)
        d.keyword_pos = l
        return d

    def pretty(self) -> str:
        if USE_FILENAME_INSTEAD_ID:
            return f"<{self.filename},{self.keyword_freq},{str(self.keyword_pos)}>"
        else:
            return f"<Id{self.id_file},{self.keyword_freq},{str(self.keyword_pos)}>"


class BooleanModelInvertedIndex:  # Inverted Index
    uniq_words: set[str] = None  # Semua kata dalam semua dokumen
    documents: list[Document] = None
    # <Term, InvertedList>
    inverted_index_table: dict[str, list[InvertedIndexRow]]

    def pretty_inverted_index_row_list_by_key(self, keyword: str):
        s = ""
        for l in self.inverted_index_table[keyword]:
            s += l.pretty() + " "

        return s.strip()

    def index(self, _documents: list[Document]):
        self.documents = _documents
        self.uniq_words = set()
        self.inverted_index_table = dict()

        # Sifat set adalah dia uniq, tidak ada duplikat di dalamnya
        for it in self.documents:
            for word in it.tokenized:
                self.uniq_words.add(word)

        for word in self.uniq_words:
            docindexed: list[InvertedIndexRow] = []
            for doci, doc in enumerate(self.documents):
                iirow = InvertedIndexRow.from_keyword(
                    doci, word, doc, name=doc.filename, filepath=doc.filepath)

                if iirow.keyword_freq > 0:
                    docindexed.append(iirow)
            self.inverted_index_table[word] = docindexed
