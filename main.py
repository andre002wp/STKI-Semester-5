from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QTextEdit
import sys
import os
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from TF_IDF import TF_IDF

from document import Document
from inverted_index import BooleanModelInvertedIndex
from incident_matrix import BooleanModelIncidentMatrix


class Ui(QtWidgets.QMainWindow):
    table_result: 'QTableWidget'
    tbl_inverted: 'QTableWidget'
    tbl_incident: 'QTableWidget'

    widget_docs_list: 'QtCore.QObject'

    lbl_incident_result: 'QLabel'

    documents: 'list[Document]' = None
    inverted_strategy: 'BooleanModelInvertedIndex' = None
    incident_strategy: 'BooleanModelIncidentMatrix' = None
    txt_keyword : 'QTextEdit' = None

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
        self.lbl_incident_result = self.findChild(
            QtWidgets.QLabel, 'lbl_incident_result')

        self.result_tableIDF = self.findChild(
            QtWidgets.QTableWidget, 'tf_idf_table')
        self.result_tableIDF.setColumnWidth(0, 250)
        self.result_tableIDF.setColumnWidth(0, 250)
        self.result_tableIDF.setColumnWidth(1, 400)
        self.result_tableIDF.setColumnWidth(2, 100)
        self.result_tableIDF.setColumnWidth(3, 100)
        self.result_tableIDF.setColumnWidth(4, 100)
        self.result_tableIDF.setColumnWidth(5, 100)
        self.result_tableIDF.setColumnWidth(6, 300)

        self.tbl_inverted = self.findChild(
            QtWidgets.QTableWidget, 'inverted_index_table')
        self.tbl_incident = self.findChild(
            QtWidgets.QTableWidget, 'incident_matrix_table')

        self.txt_keyword = self.findChild(QtWidgets.QTextEdit, 'txt_keyword')

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
        self.doTFIDF()

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

    def doTFIDF(self):
        self.tfidf = TF_IDF()
        self.tfidf.index(self.documents)


    def CheckKey(self):
        q = self.txt_keyword.toPlainText()
        if self.incident_strategy == None:
            print("Load file dulu")
            return

        # result = self.incident_strategy.query(q)
        result2 = self.tfidf.query(q)
        # incident_result = ""
        # for it in result:
        #     incident_result += it.filename + "\n"
        # self.lbl_incident_result.setText(incident_result)

        self.setIDFTable(result2)

    def setIDFTable(self,result2):
        self.result_tableIDF.setRowCount(len(result2['keyword'])+2)
        rows = 0
        for i, key in enumerate(result2['keyword']):
            self.result_tableIDF.setSpan(rows, 0, 1, 1)
            self.result_tableIDF.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(result2['keyword'][i])))
            self.result_tableIDF.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(result2['term_Frequency'][i])))
            self.result_tableIDF.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(str(result2['document_Frequency'][i])))
            self.result_tableIDF.setItem(rows, 3, QtWidgets.QTableWidgetItem(
                str(result2['d_over_df'][i])))
            self.result_tableIDF.setItem(
                rows, 4, QtWidgets.QTableWidgetItem(str(result2['idf'][i])))
            self.result_tableIDF.setItem(rows, 5, QtWidgets.QTableWidgetItem(
                str(result2['idf_plus'][i])))
            self.result_tableIDF.setItem(
                rows, 6, QtWidgets.QTableWidgetItem(str(result2['weight_keys'][i])))
            rows += 1

        self.result_tableIDF.setSpan(rows, 0, 1, 6)
        self.result_tableIDF.setItem(
            rows, 0, QtWidgets.QTableWidgetItem(str("Toootalsss : ")))
        self.result_tableIDF.setItem(
            rows, 6, QtWidgets.QTableWidgetItem(str(result2['Toootalsss'])))
        self.result_tableIDF.setSpan(rows+1, 0, 1, 7)
        self.result_tableIDF.setItem(
            rows+1, 0, QtWidgets.QTableWidgetItem(str(f"Dokument paling relevan : {result2['most_relevance']}")))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
sys.exit(app.exec_())
