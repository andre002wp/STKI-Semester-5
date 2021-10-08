from os import path
from document import Document


# MAKE TOKENIZED sebelum di stem dkk

USE_FILENAME_INSTEAD_ID = True


class BooleanModelIncidentMatrix:  # Incident Matrix
    uniq_words: set[str] = None  # Semua kata dalam semua dokumen
    documents: list[Document] = None

    #         doc0   doc1    doc2
    # kata1    1        0       1
    # kata2    0        0       1
    incident_matrix: dict[str, list[int]]  # Format diatas jadinya adalah
    # {"kata1": [0, 2], "kata2": [2]} index memakai index di `self.documents`

    def index(self, _documents: list[Document]):
        self.documents = _documents
        self.uniq_words = set()
        self.incident_matrix = dict()

        for it in self.documents:
            for word in it.tokenized:
                self.uniq_words.add(word)

        for word in self.uniq_words:
            foundIndex: list[int] = []
            for doci, doc in enumerate(self.documents):
                if word in doc.tokenized: # MASIH PAKE TOKENIZED SEBELUM STEM DKK
                    foundIndex.append(doci)

            self.incident_matrix[word] = foundIndex
