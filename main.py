from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QTextEdit
import sys
import os
import numpy as np
from document import Document
from inverted_index import BooleanModelInvertedIndex
from incident_matrix import BooleanModelIncidentMatrix
from tfidf import TF_IDF
from jaccard import Jaccard
from n_gram import N_Gram
from cosine_sim_v2 import CosineSim
from querier import BooleanModelQuerier


class Ui(QtWidgets.QMainWindow):
    table_result: 'QTableWidget'
    tbl_inverted: 'QTableWidget'
    tbl_incident: 'QTableWidget'

    widget_docs_list: 'QtCore.QObject'

    lbl_boolean_query: 'QLabel'
    lbl_incident_result: 'QLabel'
    lbl_inverted_result: 'QLabel'

    documents: 'list[Document]' = None
    inverted_strategy: 'BooleanModelInvertedIndex' = None
    incident_strategy: 'BooleanModelIncidentMatrix' = None

    txt_keyword: 'QTextEdit' = None
    txt_query: 'QTextEdit' = None

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.btnOpenFile = self.findChild(QtWidgets.QPushButton, 'openFilebtn')
        self.btnOpenFile.clicked.connect(self.OpenFile)

        self.btnCheckKeys = self.findChild(
            QtWidgets.QPushButton, 'checkKeysbtn')
        self.btnCheckKeys.clicked.connect(self.CheckKey)

        self.widget_docs_list = self.findChild(
            QtWidgets.QTextEdit, 'txt_document')

        self.lbl_boolean_query = self.findChild(
            QtWidgets.QLabel, 'lbl_boolean_query')
        self.lbl_incident_result = self.findChild(
            QtWidgets.QLabel, 'lbl_incident_result')
        self.lbl_inverted_result = self.findChild(
            QtWidgets.QLabel, 'lbl_inverted_result')

        self.tbl_preprocess = self.findChild(
            QtWidgets.QTableWidget, 'tbl_preprocess')

        # input ngram
        self.txt_input_ngram = self.findChild(
            QtWidgets.QLineEdit, 'txt_input_ngram')

        # set table width

        # tfidf
        self.result_tableIDF = self.findChild(
            QtWidgets.QTableWidget, 'tf_idf_table')
        self.result_tableIDF.setColumnWidth(0, 250)
        self.result_tableIDF.setColumnWidth(1, 400)
        self.result_tableIDF.setColumnWidth(2, 100)
        self.result_tableIDF.setColumnWidth(3, 100)
        self.result_tableIDF.setColumnWidth(4, 100)
        self.result_tableIDF.setColumnWidth(5, 100)
        self.result_tableIDF.setColumnWidth(6, 300)

        self.result_tableIDF2 = self.findChild(
            QtWidgets.QTableWidget, 'tf_idf_result_table_2')
        self.result_tableIDF2.setColumnWidth(0, 200)
        self.result_tableIDF2.setColumnWidth(1, 400)

        # jaccard_table
        self.result_tablejaccard = self.findChild(
            QtWidgets.QTableWidget, 'jaccard_result_table')
        self.result_tablejaccard.setColumnWidth(0, 400)
        self.result_tablejaccard.setColumnWidth(1, 200)
        self.txt_jaccard_result = self.findChild(
            QtWidgets.QTextEdit, 'txt_jaccard_result')

        # ngram_table
        self.result_table_ngram = self.findChild(
            QtWidgets.QTableWidget, 'n_gram_result_table')
        self.result_table_ngram.setColumnWidth(0, 400)
        self.result_table_ngram.setColumnWidth(1, 200)
        self.txt_ngram_result = self.findChild(
            QtWidgets.QTextEdit, 'txt_ngram_result')

        # cosine_table
        self.result_tablecosine = self.findChild(
            QtWidgets.QTableWidget, 'cosine_result_table')
        self.result_tablecosine.setColumnWidth(0, 400)
        self.result_tablecosine.setColumnWidth(1, 200)
        self.txt_cosine_result = self.findChild(
            QtWidgets.QTextEdit, 'txt_cosine_result')

        self.tbl_inverted = self.findChild(
            QtWidgets.QTableWidget, 'inverted_index_table')
        self.tbl_incident = self.findChild(
            QtWidgets.QTableWidget, 'incident_matrix_table')

        self.txt_keyword = self.findChild(QtWidgets.QTextEdit, 'txt_keyword')
        self.txt_query = self.findChild(QtWidgets.QTextEdit, 'txt_query')

        self.show()

    # ================ INDEXING =================

    def indexInvertedIndex(self):
        # Inverted Index
        self.inverted_strategy = BooleanModelInvertedIndex()
        self.inverted_strategy.index(self.documents)

        self.tbl_inverted.setRowCount(
            len(self.inverted_strategy.inverted_index_table))
        for i, key in enumerate(self.inverted_strategy.inverted_index_table):
            it = self.inverted_strategy.inverted_index_table[key]

            self.tbl_inverted.setItem(
                i, 0, QtWidgets.QTableWidgetItem(key))

            self.tbl_inverted.setItem(
                i, 1, QtWidgets.QTableWidgetItem(self.inverted_strategy.pretty_inverted_index_row_list_by_key(key)))

    def indexIncidentMatrix(self):
        self.incident_strategy = BooleanModelIncidentMatrix()
        self.incident_strategy.index(self.documents)

        self.tbl_incident.setRowCount(
            len(self.incident_strategy.incident_matrix))
        self.tbl_incident.setColumnCount(
            len(self.incident_strategy.documents) + 1)

        for i, it in enumerate(self.incident_strategy.documents):
            self.tbl_incident.setHorizontalHeaderItem(
                i + 1, QTableWidgetItem(it.filename))

        for i, word in enumerate(self.incident_strategy.uniq_words):
            self.tbl_incident.setItem(
                i, 0, QtWidgets.QTableWidgetItem(word))

            for j, doc in enumerate(self.incident_strategy.documents):
                if j in self.incident_strategy.incident_matrix[word]:
                    self.tbl_incident.setItem(
                        i, j + 1, QtWidgets.QTableWidgetItem("1"))
                else:
                    self.tbl_incident.setItem(
                        i, j + 1, QtWidgets.QTableWidgetItem("0"))

    def indexTFIDF(self):
        self.tfidf = TF_IDF()
        self.tfidf.index(self.documents)

    def indexjaccard(self):
        self.jaccard = Jaccard()
        self.jaccard.index(self.documents)

    def indexN_gram(self):
        self.n_gram = N_Gram()
        self.n_gram.index(self.documents)

    def indexCosine(self):
        self.cosineSim = CosineSim()
        self.cosineSim.index(self.documents)

    # ================ QUERYING =================

    def queryBooleanModel(self):
        q = self.txt_query.toPlainText()
        if len(q) == 0:
            self.lbl_boolean_query.setText("Query tidak boleh kosong")
            return

        if self.incident_strategy == None:
            self.lbl_boolean_query.setText("Incident belum mengindex")
            return

        if self.inverted_strategy == None:
            self.lbl_boolean_query.setText("Inverted belum mengindex")
            return

        # Ini gak efisien, tapi untuk visualisasi query gaapalah
        quer = BooleanModelQuerier(self.documents)
        try:
            binquery = quer.make_boolean_query(q).replace("0b", "")
        except:
            binquery = "Gagal memparse queri"
            return
        self.lbl_boolean_query.setText(binquery)
        # End hack untuk visualisasi

        if len(self.documents) == 0:
            print("Dokumen belum di index")
            return

        def prettyStrRes(result: 'list[Document]'):
            if result == None:
                result = []
            incident_result = ""
            for it in result:
                incident_result += it.filename + "\n"
            return incident_result

        try:
            resultIncident = self.incident_strategy.query(q)
            self.lbl_incident_result.setText(prettyStrRes(resultIncident))
        except Exception as e:
            print(e)
            self.lbl_incident_result.setText(
                "Incident strategy gagal mengeval queri")

        try:
            resultInverted = self.incident_strategy.query(q)
            self.lbl_inverted_result.setText(prettyStrRes(resultInverted))
        except Exception as e:
            print(e)
            self.lbl_inverted_result.setText(
                "Inverted strategy gagal mengeval queri")

    def queryTfIdf(self):
        q = self.txt_keyword.toPlainText()
        if len(q) == 0:
            print("Keyword tidak boleh kosong")
            return

        if self.documents == None or len(self.documents) == 0:
            print("Dokumen belum di index")
            return

        resultTfidf = self.tfidf.query(q)
        self.__setIDFTable(resultTfidf)

    def queryJaccard(self):
        q = self.txt_keyword.toPlainText()
        if len(q) == 0:
            print("Keyword tidak boleh kosong")
            return

        if self.documents == None or len(self.documents) == 0:
            print("Dokumen belum di index")
            return

        resultJaccard = self.jaccard.query(q)
        self.__setJaccardTable(resultJaccard)

    def queryNGram(self):
        q = self.txt_keyword.toPlainText()
        if len(q) == 0:
            print("Keyword tidak boleh kosong")
            return

        if self.documents == None or len(self.documents) == 0:
            print("Dokumen belum di index")
            return

        if(self.txt_input_ngram.text() != ""):
            num_n = ""
            for word in self.txt_input_ngram.text():
                if word.isdigit():
                    num_n += word
            print(num_n)

            if(len(num_n) > 0):
                num_n = int(num_n)
                resultNGram = self.n_gram.query(q, n=num_n)
                self.__setNGramTable(resultNGram)
            else:
                self.txt_ngram_result.setText(
                    str("nilai n harus berupa integer"))
        else:
            self.txt_ngram_result.setText(
                str("silahkan input nilai N terlebih dahulu"))

    def queryCosineSim(self):
        q = self.txt_keyword.toPlainText()
        if len(q) == 0:
            print("Keyword tidak boleh kosong")
            return

        if self.documents == None or len(self.documents) == 0:
            print("Dokumen belum di index")
            return

        resultCosine = self.cosineSim.query(q)
        self.__setCosineTable(resultCosine)

    # ================ BUTTON HANDLER =================

    def CheckKey(self):
        # Incident Matrix
        self.queryBooleanModel()

        # TF IDF
        self.queryTfIdf()
        # Jaccard
        self.queryJaccard()
        # N Gram
        self.queryNGram()
        # CosineSim
        self.queryCosineSim()

    def OpenFile(self):
        files = QFileDialog.getOpenFileNames(
            self, "select txt File", os.getcwd(), "Text Files (*.txt)")

        self.documents = []

        # Preprocessing
        # filelist = ""
        self.tbl_preprocess.setRowCount(len(files[0]))
        for i, file in enumerate(files[0]):
            _d = Document.from_file(file)
            self.documents.append(_d)
            # _d_as_str = str(_d)

            # filelist += f"{_d.filename} {_d_as_str}\n\n=======================\n\n"
            self.tbl_preprocess.setItem(
                i, 0, QtWidgets.QTableWidgetItem(_d.filename))
            self.tbl_preprocess.setItem(
                i, 1, QtWidgets.QTableWidgetItem(_d.raw))
            self.tbl_preprocess.setItem(
                i, 2, QtWidgets.QTableWidgetItem(_d.folded))
            self.tbl_preprocess.setItem(
                i, 3, QtWidgets.QTableWidgetItem(_d.no_number))
            self.tbl_preprocess.setItem(
                i, 4, QtWidgets.QTableWidgetItem(_d.no_symbol))
            self.tbl_preprocess.setItem(
                i, 5, QtWidgets.QTableWidgetItem(_d.trimmed))
            self.tbl_preprocess.setItem(
                i, 6, QtWidgets.QTableWidgetItem(str(_d.tokenized)))
            self.tbl_preprocess.setItem(
                i, 7, QtWidgets.QTableWidgetItem(str(_d.filtered)))
            self.tbl_preprocess.setItem(
                i, 8, QtWidgets.QTableWidgetItem(_d.stemmed_str))
            self.tbl_preprocess.setItem(
                i, 9, QtWidgets.QTableWidgetItem(_d.filepath))
            self.tbl_preprocess.resizeColumnsToContents()

        # self.widget_docs_list.setText(str(filelist))

        self.indexInvertedIndex()
        self.indexIncidentMatrix()
        self.indexTFIDF()
        self.indexjaccard()
        self.indexN_gram()
        self.indexCosine()

    # ================ HELPER =================

    def __setIDFTable(self, result_idf):
        # tabel Pertama
        self.result_tableIDF.setRowCount(len(result_idf['keyword']))
        rows = 0
        for i, key in enumerate(result_idf['keyword']):
            self.result_tableIDF
            self.result_tableIDF.setSpan(rows, 0, 1, 1)
            self.result_tableIDF.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(result_idf['keyword'][i])))
            self.result_tableIDF.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(result_idf['term_Frequency'][i])))
            self.result_tableIDF.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(str(result_idf['document_Frequency'][i])))
            self.result_tableIDF.setItem(rows, 3, QtWidgets.QTableWidgetItem(
                str(result_idf['d_over_df'][i])))
            self.result_tableIDF.setItem(
                rows, 4, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(result_idf['idf'][i]))))
            self.result_tableIDF.setItem(rows, 5, QtWidgets.QTableWidgetItem(
                str("{:0.2f}".format(result_idf['idf_plus'][i]))))

            # janky func to format 2 decimal
            weight_print = ""
            for number in result_idf['weight_keys'][i]:
                weight_print += str("{:0.2f}".format(number)) + ", "
            # end of janky func

            self.result_tableIDF.setItem(
                rows, 6, QtWidgets.QTableWidgetItem(str(weight_print)))
            rows += 1

        self.result_tableIDF2.setRowCount(len(result_idf['tfidf_coef_result']))
        rows = 0
        for key, value in result_idf['tfidf_coef_result'].items():
            self.result_tableIDF2.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(key)))
            self.result_tableIDF2.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(value))))
            rows += 1

    def __setJaccardTable(self, result):
        jaccard_result_text: str = ""
        for idx, docs in enumerate(result['term_Similarity']):
            # print nama file
            jaccard_result_text += f"file : {self.documents[idx].filename}\n"
            # print A intersect B
            jaccard_result_text += "A \u2229 B :"
            jaccard_result_text += "{ "
            for item, sub in docs.items():
                if(list(docs)[-1] == item):
                    jaccard_result_text += str(item)+" "
                else:
                    jaccard_result_text += str(item)+", "
            jaccard_result_text += "}\n"

            # print A U B
            jaccard_result_text += "A U B :"
            jaccard_result_text += "{ "
            for item, sub in result['union_docs'][idx].items():
                if(list(result['union_docs'][idx])[-1] == item):
                    jaccard_result_text += str(item)+" "
                else:
                    jaccard_result_text += str(item)+", "
            jaccard_result_text += "}\n"

            # print result
            jaccard_result_text += f"result : {len(docs.items())}/{len(result['union_docs'][idx])} = {result['jaccard_coef_result'][self.documents[idx].filename]}\n\n"

        self.txt_jaccard_result.setText(jaccard_result_text)

        self.result_tablejaccard.setRowCount(
            len(result['jaccard_coef_result']))
        rows = 0
        for key, value in result['jaccard_coef_result'].items():
            self.result_tablejaccard.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(key)))
            self.result_tablejaccard.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(value))))
            rows += 1

    def __setNGramTable(self, result):
        ngram_result_text: str = ""
        for idx, docs in enumerate(result['ngram_similarity']):
            # print nama file
            ngram_result_text += f"file : {self.documents[idx].filename}\n"
            # print A intersect B
            ngram_result_text += "A \u2229 B :"
            ngram_result_text += "{ "
            for item, sub in docs.items():
                if(list(docs)[-1] == item):
                    ngram_result_text += str(item)+" "
                else:
                    ngram_result_text += str(item)+", "
            ngram_result_text += "}\n"

            # print A U B
            ngram_result_text += "A U B :"
            ngram_result_text += "{ "
            for item, sub in result['union_docs_gram'][idx].items():
                if(list(result['union_docs_gram'][idx])[-1] == item):
                    ngram_result_text += str(item)+" "
                else:
                    ngram_result_text += str(item)+", "
            ngram_result_text += "}\n"

            # print result
            ngram_result_text += f"result : {len(docs.items())}/{len(result['union_docs_gram'][idx])} = {result['ngram_coef_result'][self.documents[idx].filename]}\n\n"

        self.txt_ngram_result.setText(ngram_result_text)

        self.result_table_ngram.setRowCount(len(result['ngram_coef_result']))
        rows = 0
        for key, value in result['ngram_coef_result'].items():
            self.result_table_ngram.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(key)))
            self.result_table_ngram.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(value))))
            rows += 1

    def __setCosineTable(self, result: 'dict'):
        cosine_result_text = ""

        for key, value in result['similarity'].items():
            cosine_result_text += f"filename = {key} \n"
            for term_docs in result['term_frequency_v2']:
                for index in range(len(term_docs)):
                    if(index == 0):
                        cosine_result_text += f"keyword tf :{term_docs[index]} \n"
                    elif(index == 1):
                        cosine_result_text += f"{key} tf {term_docs[index]} \n\n"

        self.txt_cosine_result.setText(cosine_result_text)

        self.result_tablecosine.setRowCount(len(result['similarity']))
        rows = 0
        for key, value in result['similarity'].items():
            self.result_tablecosine.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(key)))
            self.result_tablecosine.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(value))))
            rows += 1

    # def __setCosineTable(self, result):
    #     cosine_result_text:str = ""
    #     for idx,docs in enumerate(result['term_Similarity']):
    #         #print nama file
    #         cosine_result_text += f"file : {self.documents[idx].filename}\n"
    #         #print A intersect B
    #         cosine_result_text += "A \u2229 B :"
    #         cosine_result_text += "{ "
    #         for item,sub in docs.items():
    #             if(list(docs)[-1] == item):
    #                 cosine_result_text += str(item)+" "
    #             else:
    #                 cosine_result_text += str(item)+", "
    #         cosine_result_text += "}\n"

    #         #print A U B
    #         cosine_result_text += "A U B :"
    #         cosine_result_text += "{ "
    #         for item,sub in result['union_docs'][idx].items():
    #             if(list(result['union_docs'][idx])[-1] == item):
    #                 cosine_result_text += str(item)+" "
    #             else:
    #                 cosine_result_text += str(item)+", "
    #         cosine_result_text += "}\n"

    #         #print result
    #         cosine_result_text += f"result : {len(docs.items())}/{len(result['union_docs'][idx])} = {result['jaccard_coef_result'][self.documents[idx].filename]}\n\n"

        # self.txt_cosine_result.setText(cosine_result_text)

        # self.result_tablecosine.setRowCount(len(result['ngram_coef_result']))
        # rows = 0
        # for key,value in result['ngram_coef_result'].items():
        #     self.result_tablecosine.setItem(
        #         rows, 0, QtWidgets.QTableWidgetItem(str(key)))
        #     self.result_tablecosine.setItem(
        #         rows, 1, QtWidgets.QTableWidgetItem(str("{:0.2f}".format(value))))
        #     rows += 1


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
sys.exit(app.exec_())
