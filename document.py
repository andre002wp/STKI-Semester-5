import re
import string
from pathlib import Path
import json
from typing import Dict
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class Document:
    raw: str = None
    # Case folding
    folded: str = None

    # Sanitize
    no_number: str = None
    no_symbol: str = None
    trimmed: str = None

    tokenized: list[str] = None

    # Filtering adalah tahap mengambil kata-kata penting dari hasil token dengan menggunakan algoritma stoplist (membuang kata kurang penting) atau wordlist (menyimpan kata penting).
    filtered: str = None
    stemmed_str: str = None  # Ambil kata dasar
    stemmed: list[str] = None

    word_count: dict[str, int] = None

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_file(path: str) -> 'Document':
        p = Path(path)
        txt = p.read_text()
        return Document.from_string(txt)

    @staticmethod
    def from_string(source: str) -> 'Document':
        f = Document()
        f.raw = source
        f.folded = f.raw.lower()
        f.no_number = re.sub(r"\d+", "", f.folded)
        f.no_symbol = f.no_number.translate(
            str.maketrans("", "", string.punctuation))
        f.trimmed = f.no_symbol.strip()
        f.tokenized = f.trimmed.split()

        f.filtered = Document.filter_stopword(f.tokenized)
        f.stemmed_str = Document.stem_word(f.filtered)
        f.stemmed = f.stemmed_str.split()
        f.word_count = Document.count_word(f.stemmed)

        return f

    @staticmethod
    def filter_stopword(list_of_word_lowercased: list[str]) -> list[str]:
        p = Path("./stopword_tweet_pilkada_DKI_2017.csv")
        _stop_words = p.read_text().splitlines()

        _filtered: list[str] = []
        for it in list_of_word_lowercased:
            if it not in _stop_words:
                _filtered.append(it)
        return _filtered

    def stem_word(list_of_word_lowercased: list[str]) -> str:
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        sentence = stemmer.stem(
            Document.wordlist_as_sentence(list_of_word_lowercased))
        return sentence

    @staticmethod
    def wordlist_as_sentence(word_list: list[str]) -> str:
        _kalimat = ""
        for it in word_list:
            _kalimat += it + " "
        return _kalimat.strip()

    def __str__(self) -> str:
        return json.dumps(self.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def count_word(list_of_word_lower: list[str]) -> dict[str, int]:
        word_count = dict()

        for word in list_of_word_lower:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        word_count = dict(
            sorted(word_count.items(), key=lambda item: item[1], reverse=True))
        return word_count
