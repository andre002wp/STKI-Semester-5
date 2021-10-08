from document import Document

class InvertedIndexRow:
    id_file : int = None
    filename : str = None
    path : str = None

    keyword_freq : int = 0 # Seberapa kali muncul
    keyword_pos : int = None # Lokasi keyword di file

    def __init__(self) -> None:
        pass

class BooleanModelII: # Inverted Index
    documents : list[Document] = None
    inverted_index_table: dict[str, ]