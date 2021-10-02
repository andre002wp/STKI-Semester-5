from logging import NullHandler
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv

class Ui(QtWidgets.QMainWindow):
    openFileDialog = []
    selected_keyword = []
    stopwords = []
    result = {}
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('SKTI Tugas 2.ui', self)

        self.btnOpenFile = self.findChild(QtWidgets.QPushButton, 'openFilebtn')
        self.btnOpenFile.clicked.connect(self.OpenFile)
        self.btnCheckKeys = self.findChild(QtWidgets.QPushButton, 'checkKeysbtn')
        self.btnCheckKeys.clicked.connect(self.CheckKey) 

        self.result_table = self.findChild(QtWidgets.QTableWidget, 'result_table')
        self.result_table.setColumnWidth(0,250)
        self.result_table.setColumnWidth(0,250)
        self.result_table.setColumnWidth(1,400)
        self.result_table.setColumnWidth(2,100)
        self.result_table.setColumnWidth(3,100)
        self.result_table.setColumnWidth(4,100)
        self.result_table.setColumnWidth(5,100)
        self.result_table.setColumnWidth(6,300)
        self.show()

    def OpenFile(self):
        # This is executed when the button is pressed
        print('btn Open File Pressed')
        files = QFileDialog.getOpenFileNames(self,"select txt File",os.getcwd(),"Text Files (*.txt)")
        self.openFileDialog = files[0]
        filepath = self.openFileDialog[0]
        print(self.openFileDialog)
        print("\nfilepath 1 = ",filepath)
        print()
    
    def CheckKey(self):
        text_hasil = ""
        self.Keywords = self.findChild(QtWidgets.QTextEdit, 'txt_keyword')
        self.selected_keyword = self.Keywords.toPlainText()
        self.selected_keyword = self.selected_keyword.split()

        keys = []
        for i,keyword in enumerate(self.Keywords.toPlainText().split()):
            keys.append(keyword)
            text_hasil += f"key {i} : {keyword}\n"
        self.result['keyword'] = keys
        print(self.Keywords.toPlainText())

        with open('stopword_tweet_pilkada_DKI_2017.csv', mode='r') as file:
            openStopword = csv.reader(file,delimiter='\n')
            for row in openStopword:
                self.stopwords.append(row)
        

        tokens_doc = []
        merge = set()
        for file in self.openFileDialog:
            # Check whether file is in text format or not
            if file.endswith(".txt"):
                file_path = f"{file}"
                # call read text file function
                tokens_doc.append(self.read_text_file(file_path))
                print(f"dokumen {len(tokens_doc)} :\n",tokens_doc[len(tokens_doc)-1])
                text_hasil += f"Read from filepath : {file_path}\n"
                print("\nRead from filepath = ",file_path)

        for item in tokens_doc:
            merge.update(item)

        text_hasil += f"total document = {len(tokens_doc)}\n"
        print(f"total document = {len(tokens_doc)}")
        ####### TFFFFFFFFF
        term_Frequency = []
        for key in self.selected_keyword:
            temp_TF_d_keyword = []
            for document in tokens_doc:
                temp_count = 0 # im lazy(basically says that)
                for tokens in document:
                    if (key == tokens):
                        temp_TF_d_keyword.append(document[tokens])
                        temp_count += 1
                if (temp_count == 0): # im lazy
                    temp_TF_d_keyword.append(0)# im lazy
            term_Frequency.append(temp_TF_d_keyword)
        text_hasil += f"TF\n{term_Frequency}\n"
        self.result['TF'] = term_Frequency
        print("TF")
        print(term_Frequency)

        ####### dFFFFFFF

        document_Frequency = []
        for key_frequency in term_Frequency:
            count = 0
            for frequency in key_frequency:
                if (frequency>0):
                    count += 1
            document_Frequency.append(count)
        text_hasil += f"dF\n{document_Frequency}\n"
        self.result['dF'] = document_Frequency
        print("dwF")
        print(document_Frequency)

        ########## D/df

        #### todo kalo token yang dicari gaada di semua dokumen gmn ?

        D_over_df = []
        for keys in document_Frequency:
            try:
                D_over_df.append(len(tokens_doc)/keys)## todo
            except:
                D_over_df.append(len(tokens_doc))## todo
        text_hasil += f"D/df\n{D_over_df}\n"
        self.result['D_over_df'] = D_over_df
        print("D/df")
        print(D_over_df)

        ################### IDF
        import math

        idf_keys = []
        for i,keys in enumerate(document_Frequency):
            idf_keys.append(math.log(D_over_df[i],10))## todo
        text_hasil += f"IDF\n{idf_keys}\n"
        self.result['IDF'] = idf_keys
        print("IDF")
        print(idf_keys)

        ################### IDF+1
        idf_plus = []
        for num in idf_keys:
            idf_plus.append(num+1)
        text_hasil += f"idf+1\n{idf_plus}\n"
        self.result['idf_plus'] = idf_plus
        print("idf+1")
        print(idf_plus)

        ################### W= tf* (IDF+1)
        Weight_keys = []
        for i,keys in enumerate(term_Frequency):
            temp_weight_for_key_in_doc = []
            for document in keys:
                temp_weight_for_key_in_doc.append(document*idf_plus[i])
            Weight_keys.append(temp_weight_for_key_in_doc)
        text_hasil += f"Weight\n{Weight_keys}\n"
        self.result['Weight'] = Weight_keys
        print("Weight")
        print(Weight_keys)
        
        self.setTable()

    def setTable(self):
        self.result_table.setRowCount(len(self.result['keyword']))
        rows = 0
        for i,key in enumerate(self.result['keyword']):
            self.result_table.setItem(rows,0,QtWidgets.QTableWidgetItem(str(self.result['keyword'][i])))
            self.result_table.setItem(rows,1,QtWidgets.QTableWidgetItem(str(self.result['TF'][i])))
            self.result_table.setItem(rows,2,QtWidgets.QTableWidgetItem(str(self.result['dF'][i])))
            self.result_table.setItem(rows,3,QtWidgets.QTableWidgetItem(str(self.result['D_over_df'][i])))
            self.result_table.setItem(rows,4,QtWidgets.QTableWidgetItem(str(self.result['IDF'][i])))
            self.result_table.setItem(rows,5,QtWidgets.QTableWidgetItem(str(self.result['idf_plus'][i])))
            self.result_table.setItem(rows,6,QtWidgets.QTableWidgetItem(str(self.result['Weight'][i])))
            rows+=1
        

    def sanitize(self,text):
        text = text.lower()

        # Hapus simbol
        sentence = text.replace("("," ").replace(")"," ").replace("\""," ").replace("?"," ").replace("-", " ").replace("/", " ").replace("\n", " ").replace("."," ")

        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stemmer.stem(sentence)

        return sentence.replace("  ", " ")
    
    def word_count(self,file):
        word_count = dict()
        isi_file =self.sanitize(file)
        words = isi_file.split()
        for word in words:
            if(self.is_stopword(word)==0):
                # print(word,"is not on stopword")
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
                    word_count = dict(sorted(word_count.items(), key=lambda item: item[1],reverse=True))
        return word_count

    def is_stopword(self,word):
        for words in self.stopwords:
            # print(f"is {word} == {words}")
            if(word == words[0]):
                return 1
        return 0

    def read_text_file(self,file_path):
        with open(file_path, 'r') as f:
            isi_file = f.read()
            token = self.word_count(isi_file)
        return token
    


  



    
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
# 5. Run your application's event loop (or main loop)
sys.exit(app.exec_())