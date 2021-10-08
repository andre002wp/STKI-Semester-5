from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem
import sys
import os
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from document import Document
from inverted_index import BooleanModelInvertedIndex
from incident_matrix import BooleanModelIncidentMatrix


class Ui(QtWidgets.QMainWindow):
    table_result: QTableWidget
    tbl_inverted: QTableWidget
    tbl_incident: QTableWidget

    widget_docs_list: QtCore.QObject

    documents: list[Document] = None
    inverted_strategy: BooleanModelInvertedIndex = None
    incident_strategy: BooleanModelIncidentMatrix = None

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

        self.table_result = self.findChild(
            QtWidgets.QTableWidget, 'result_table')
        self.table_result.setColumnWidth(0, 250)
        self.table_result.setColumnWidth(0, 250)
        self.table_result.setColumnWidth(1, 400)
        self.table_result.setColumnWidth(2, 100)
        self.table_result.setColumnWidth(3, 100)
        self.table_result.setColumnWidth(4, 100)
        self.table_result.setColumnWidth(5, 100)
        self.table_result.setColumnWidth(6, 300)

        self.tbl_inverted = self.findChild(
            QtWidgets.QTableWidget, 'inverted_index_table')
        self.tbl_incident = self.findChild(
            QtWidgets.QTableWidget, 'incident_matrix_table')

        self.show()

    def OpenFile(self):
        files = QFileDialog.getOpenFileNames(
            self, "select txt File", os.getcwd(), "Text Files (*.txt)")

        self.documents = []

        # Preprocessing
        filelist = ""
        for file in files[0]:
            _d = Document.from_file(file)
            self.documents.append(_d)
            _d_as_str = str(_d)

            filelist += f"{_d.filename} {_d_as_str}\n\n=======================\n\n"
        self.widget_docs_list.setText(str(filelist))

        self.doInvertedIndex()
        self.doIncidentMatrix()

    def doInvertedIndex(self):
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

    def doIncidentMatrix(self):
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

        # Set nama kolom
        # self.tbl_incident.Column

    def CheckKey(self):
        pass
    #     text_hasil = ""
    #     self.Keywords = self.findChild(QtWidgets.QTextEdit, 'txt_keyword')
    #     self.selected_keyword = self.Keywords.toPlainText()
    #     self.selected_keyword = self.selected_keyword.split()

    #     keys = []
    #     for i,keyword in enumerate(self.Keywords.toPlainText().split()):
    #         keys.append(keyword)
    #         text_hasil += f"key {i} : {keyword}\n"
    #     self.result['keyword'] = keys
    #     print(self.Keywords.toPlainText())

    #     with open('stopword_tweet_pilkada_DKI_2017.csv', mode='r') as file:
    #         openStopword = csv.reader(file,delimiter='\n')
    #         for row in openStopword:
    #             self.stopwords.append(row)

    #     tokens_doc = []
    #     merge = set()
    #     for file in self.openFileDialog:
    #         # Check whether file is in text format or not
    #         if file.endswith(".txt"):
    #             file_path = f"{file}"
    #             # call read text file function
    #             tokens_doc.append(self.read_text_file(file_path))
    #             print("\nRead from filepath = ",file_path)
    #             print(f"dokumen {len(tokens_doc)} :\n",tokens_doc[len(tokens_doc)-1])
    #             text_hasil += f"Read from filepath : {file_path}\n"

    #     for item in tokens_doc:
    #         merge.update(item)

    #     text_hasil += f"total document = {len(tokens_doc)}\n"
    #     print(f"total document = {len(tokens_doc)}")
    #     ####### TFFFFFFFFF
    #     term_Frequency = []
    #     for key in self.selected_keyword:
    #         temp_TF_d_keyword = []
    #         for document in tokens_doc:
    #             temp_count = 0 # im lazy(basically says that)
    #             for tokens in document:
    #                 if (key == tokens):
    #                     temp_TF_d_keyword.append(document[tokens])
    #                     temp_count += 1
    #             if (temp_count == 0): # im lazy
    #                 temp_TF_d_keyword.append(0)# im lazy
    #         term_Frequency.append(temp_TF_d_keyword)
    #     text_hasil += f"TF\n{term_Frequency}\n"
    #     self.result['TF'] = term_Frequency
    #     print("TF")
    #     print(term_Frequency)

    #     ####### dFFFFFFF

    #     document_Frequency = []
    #     for key_frequency in term_Frequency:
    #         count = 0
    #         for frequency in key_frequency:
    #             if (frequency>0):
    #                 count += 1
    #         document_Frequency.append(count)
    #     text_hasil += f"dF\n{document_Frequency}\n"
    #     self.result['dF'] = document_Frequency
    #     print("dwF")
    #     print(document_Frequency)

    #     ########## D/df

    #     #### todo kalo token yang dicari gaada di semua dokumen gmn ?

    #     D_over_df = []
    #     for keys in document_Frequency:
    #         try:
    #             D_over_df.append(len(tokens_doc)/keys)## todo
    #         except:
    #             D_over_df.append(0)## todo
    #     text_hasil += f"D/df\n{D_over_df}\n"
    #     self.result['D_over_df'] = D_over_df
    #     print("D/df")
    #     print(D_over_df)

    #     ################### IDF
    #     import math

    #     idf_keys = []
    #     for i,keys in enumerate(document_Frequency):
    #         try:
    #             idf_keys.append(math.log(D_over_df[i],10))## todo
    #         except:
    #             idf_keys.append(0)## todo

    #     text_hasil += f"IDF\n{idf_keys}\n"
    #     self.result['IDF'] = idf_keys
    #     print("IDF")
    #     print(idf_keys)

    #     ################### IDF+1
    #     idf_plus = []
    #     for num in idf_keys:
    #         idf_plus.append(num+1)
    #     text_hasil += f"idf+1\n{idf_plus}\n"
    #     self.result['idf_plus'] = idf_plus
    #     print("idf+1")
    #     print(idf_plus)

    #     ################### W= tf* (IDF+1)
    #     Weight_keys = []
    #     for i,keys in enumerate(term_Frequency):
    #         temp_weight_for_key_in_doc = []
    #         for document in keys:
    #             temp_weight_for_key_in_doc.append(document*idf_plus[i])
    #         Weight_keys.append(temp_weight_for_key_in_doc)
    #     text_hasil += f"Weight\n{Weight_keys}\n"
    #     self.result['Weight'] = Weight_keys
    #     print("Weight")
    #     print(Weight_keys)

    #     self.setTable()

    # def setTable(self):
    #     self.result_table.setRowCount(len(self.result['keyword'])+2)
    #     rows = 0
    #     for i, key in enumerate(self.result['keyword']):
    #         self.result_table.setSpan(rows, 0, 1, 1)
    #         self.result_table.setItem(
    #             rows, 0, QtWidgets.QTableWidgetItem(str(self.result['keyword'][i])))
    #         self.result_table.setItem(
    #             rows, 1, QtWidgets.QTableWidgetItem(str(self.result['TF'][i])))
    #         self.result_table.setItem(
    #             rows, 2, QtWidgets.QTableWidgetItem(str(self.result['dF'][i])))
    #         self.result_table.setItem(rows, 3, QtWidgets.QTableWidgetItem(
    #             str(self.result['D_over_df'][i])))
    #         self.result_table.setItem(
    #             rows, 4, QtWidgets.QTableWidgetItem(str(self.result['IDF'][i])))
    #         self.result_table.setItem(rows, 5, QtWidgets.QTableWidgetItem(
    #             str(self.result['idf_plus'][i])))
    #         self.result_table.setItem(
    #             rows, 6, QtWidgets.QTableWidgetItem(str(self.result['Weight'][i])))
    #         rows += 1

    #     self.result_table.setSpan(rows, 0, 1, 6)
    #     self.result_table.setItem(
    #         rows, 0, QtWidgets.QTableWidgetItem(f"Toootalsss : "))
    #     self.result_table.setSpan(rows+1, 0, 1, 6)
    #     self.result_table.setItem(
    #         rows+1, 0, QtWidgets.QTableWidgetItem(f"Dokument paling relevan : ulala"))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
sys.exit(app.exec_())
