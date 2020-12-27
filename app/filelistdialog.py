# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 23:17:27 2020

@author: adwait
"""

import logging
import os
import time
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel, \
    QTextEdit, QLineEdit, QComboBox, QSizePolicy, QFileDialog


class FileListDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.resize(350, 100)
        self.setWindowTitle("Generate file list")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.home()
        
    def home(self):
        folderLabel = QLabel('Folder path', self)
        formatLabel = QLabel('Extension', self)
        self.sortLabel = QLabel('Sort by', self)
        self.sortComboBox = QComboBox(self)
        self.sortComboBox.addItems(['Date modified', 'Name'])
        
        
        self.createBtn = QPushButton("Create list")
        self.createBtn.clicked.connect(self.create_list)
        
        self.loadBtn = QPushButton("Load list")
        self.loadBtn.clicked.connect(self.close_dialog)
        self.loadBtn.setEnabled(False)

        
        self.layout.addWidget(folderLabel, 0, 1, 1, 1)
        self.layout.addWidget(formatLabel, 0, 2, 1, 1)
        self.layout.addWidget(self.sortLabel, 1, 1, 1, 1)
        self.layout.addWidget(self.sortComboBox, 1, 0, 1, 1)
        self.layout.addWidget(self.createBtn, 1, 0, 1, 1)
        self.layout.addWidget(self.loadBtn, 1, 0, 1, 1)
        
        #filename dictionary. keys: file_type::file number, vals: [folder_path, format_string]
        self.filename_dict = {'Video': {}, 'Data': {}} 
        self.num_dict = {'Video': 0, 'Data': 0} #number of defined files (or rows)
        
        self.add_widgets('Video')
        self.add_widgets('Data')
    
    #add row of new video/data input widgets
    def add_widgets(self, file_type):
        self.num_dict[file_type] += 1
        self.filename_dict[file_type][self.num_dict[file_type]] = ['', '']
        
        label = f'{file_type} {self.num_dict[file_type]}'
        fileLabel = QLabel(label)
        
        folderPathText =  QTextEdit()
        # folderPathText.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        
        formatLine =  QLineEdit()
        formatLine.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        
        browseBtn = QPushButton("Browse..")
        browseBtn.clicked.connect(lambda: self.open_directory(folderPathText, label))
        
        folderPathText.textChanged.connect(lambda: self.update_filename_dict(self.num_dict[file_type],
                                                                     file_type,
                                                                     folderPathText.toPlainText(),
                                                                     formatLine.text()))
        formatLine.textChanged.connect(lambda: self.update_filename_dict(self.num_dict[file_type],
                                                                     file_type,
                                                                     folderPathText.toPlainText(),
                                                                     formatLine.text()))

        plusBtn = QPushButton("+")
        minusBtn = QPushButton("-")
        
        if self.num_dict[file_type] == 1:
            minusBtn.setEnabled(False)
        
        widget_list = [fileLabel, folderPathText, formatLine, browseBtn, 
                       plusBtn, minusBtn]
        
        plusBtn.clicked.connect(lambda: self.add_or_remove('+', widget_list,
                                                           self.num_dict[file_type],
                                                           file_type))
        minusBtn.clicked.connect(lambda: self.add_or_remove('-', widget_list,
                                                            self.num_dict[file_type],
                                                            file_type))
        
        row_num =  sum(self.num_dict.values())
        self.layout.addWidget(fileLabel, row_num, 0, 1, 1)
        self.layout.addWidget(folderPathText, row_num, 1, 1, 1)
        self.layout.addWidget(formatLine, row_num, 2, 1, 1)
        self.layout.addWidget(browseBtn, row_num, 3, 1, 1)
        self.layout.addWidget(plusBtn, row_num, 4, 1, 1)
        self.layout.addWidget(minusBtn, row_num, 5, 1, 1)
        self.layout.addWidget(self.sortLabel, row_num + 1, 0, 1, 1)
        self.layout.addWidget(self.sortComboBox, row_num + 1, 1, 1, 1)
        self.layout.addWidget(self.createBtn, row_num + 1, 3, 1, 1)
        self.layout.addWidget(self.loadBtn, row_num + 1, 4, 1, 2)
        
    def add_or_remove(self, action, wid_list, rownum, file_type):
        if action == '+':
            self.add_widgets(file_type)
        elif action == '-':
            for wid in wid_list:
                self.layout.removeWidget(wid)
                wid.deleteLater()
            self.num_dict[file_type] -= 1
            del self.filename_dict[file_type][rownum]
            # if self.num_dict[file_type] == 0:
            #     self.layout.removeWidget(self.varListBtn)
            #     self.layout.addWidget(self.makeVarAdd, 1, 1, 1, 1)
            #     self.layout.addWidget(self.makeVarOk, 1, 0, 1, 1)
            self.resize(350, 100)
    
    def open_directory(self, wid, label):
        folderpath = QFileDialog.getExistingDirectory(caption = f'Select {label} folder')
        wid.setText(folderpath + '/')
        
    
    def update_filename_dict(self, rownum, file_type, folder_path, format_string):
        # if var_name != '' and formula != '':
        self.filename_dict[file_type][rownum] = [folder_path, format_string]
        logging.debug(f'{self.filename_dict}')
   
    #create file list
    def create_list(self):
        df = pd.DataFrame()
        for key1 in self.filename_dict.keys():
            for key2 in self.filename_dict[key1].keys():
                colname = f'{key1} {key2}'
                folderpath = self.filename_dict[key1][key2][0]
                file_extension = self.filename_dict[key1][key2][1]
                if os.path.exists(folderpath) == True:
                    with os.scandir(folderpath) as folder:
                        c_list = ['Name', 'Extension', 'Date modified', colname, 'isdir']                    
                        file_data = np.transpose([[os.path.basename(file.path),
                                                   os.path.splitext(file.path)[1],
                                                   os.path.getmtime(file.path),
                                                   file.path, file.is_dir()]
                                                  for file in folder])
                        df_file = pd.DataFrame(dict(zip(c_list, file_data)))
                        df_file = df_file[df_file['isdir'] == 'False']
                        if file_extension != '':
                            df_file = df_file[df_file['Extension'] == file_extension]
                        df_file.sort_values(by = self.sortComboBox.currentText(), inplace = True)
                        df_file.reset_index(inplace = True)
                        df = df.join(df_file[colname], how = 'outer')
        df['Data OK?'] = ''
        df['Comments'] = ''
        #rename indices to start from 1
        df.rename(index = dict(zip(range(0, df.shape[0]), range(1, df.shape[0]+1))),
                  inplace = True)
        list_path, _ = QFileDialog.getSaveFileName(caption = 'Save file list as..')
        if list_path[-5:] != '.xlsx':
            list_path += '.xlsx'
        df.to_excel(list_path, index_label = 'Measurement number')
        logging.info(f'File list saved in {list_path}')
        self.loadBtn.setEnabled(True)
                    
    
    def close_dialog(self):
        # datadf_newvar = self.dataTransformList[-1].copy()
        # for key in self.filename_dict.keys():
        #     datadf_newvar = self.summary.create_var(var_name = self.filename_dict[key][0],
        #                                                    formula = self.filename_dict[key][1],
        #                                                    datadf = datadf_newvar)
        # self.dataTransformList.append(datadf_newvar)
        # stepnum = str(len(self.transformList))
        # self.transformList.append(stepnum +':Create variable')
        # self.update_dropdown_params()

        # self.datadf_filtered = self.summary.filter_df(self.datadf, 
        #                                               self.filter_dict)
        self.done(0)