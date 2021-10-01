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
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('SKTI Tugas 2.ui', self)

        self.btnOpenFile = self.findChild(QtWidgets.QPushButton, 'openFilebtn')
        self.btnOpenFile.clicked.connect(self.OpenFile)
        self.btnCheckKeys = self.findChild(QtWidgets.QPushButton, 'checkKeysbtn')
        self.btnCheckKeys.clicked.connect(self.CheckKey) 

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

        for i,keyword in enumerate(self.Keywords.toPlainText().split()):
            text_hasil += f"key {i} : {keyword}\n"
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
        text_hasil += f"dwF\n{document_Frequency}\n"
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
        print("D/df")
        print(D_over_df)

        ################### IDF
        import math

        idf_keys = []
        for i,keys in enumerate(document_Frequency):
            idf_keys.append(math.log(D_over_df[i],10))## todo
        text_hasil += f"IDF\n{idf_keys}\n"
        print("IDF")
        print(idf_keys)

        ################### IDF+1
        idf_plus = []
        for num in idf_keys:
            idf_plus.append(num+1)
        text_hasil += f"idf+1\n{idf_plus}\n"
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
        print("Weight")
        print(Weight_keys)


        self.Hasil = self.findChild(QtWidgets.QTextEdit, 'txt_hasil')
        self.Hasil.setPlainText(text_hasil)
        

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