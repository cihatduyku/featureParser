#!/usr/bin/env python
#-*-coding:utf-8-*-
import re
import xlsxwriter
import os
import datetime
import numpy as np


rx_dict = {
    'Feature': re.compile(r'Feature:(?P<Feature>.*)\n'),
    'Scenario': re.compile(r'Scenario:(?P<Scenario>.*)\n'),
    'Background': re.compile(r'Background:(?P<Background>.*)\n'),
    'And': re.compile(r'And (?P<And>.*)'),
    'QA': re.compile(r'QA:(?P<QA>.*)\n'),    
  }

def _parse_line(line):
  
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match

    return None, None

def parse_file(dirname,file,worksheet):
    
    QA="Undefined"

    filepath=os.path.join(dirname, file)
    
    # open the file and read through it line by line
    with open(filepath, 'r',encoding="utf-8") as file_object:
        lines = file_object.readlines()
        
        i = 0
        senaryoSayisi=0
        while i < len(lines):
            key, match = _parse_line(lines[i])
            
            if key == 'Feature':
                _feature = match.group('Feature')
                   

            if key == 'QA':
                QA = match.group('QA').strip()
    
            
            if key == 'Scenario':
                _scenario = match.group('Scenario')
                senaryoSayisi += 1

            i+= 1

        today = datetime.datetime.now()  
        week = today.isocalendar()[1]
        columns=([QA,senaryoSayisi,today.strftime("%x %X"),week])
       
      
    return columns

if __name__== "__main__":

    dirname, filename = os.path.split(os.path.abspath(__file__))
     
    #try:
    #    os.mkdir(dirname+'/excels/')
    #except OSError:
    #    print ('/excels/ oluşturulamadı...')
    
    workbook = xlsxwriter.Workbook(dirname+'/Logs.xlsx')
    worksheet = workbook.add_worksheet()
    
    row = 0
    col=0
    columns = (['QA','Senaryo Sayısı','Log Tarihi','Log Haftası'])
    
    for item in (columns):
        worksheet.write(row, col,     item)
        col += 1
    
    row=1
    col=0
    
    files = []
    excelData= []
    data=[]
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dirname):
        for file in f:
            if '.feature' in file:
                files.append(os.path.join(r, file))
                data=parse_file(dirname, file, worksheet)
                
                if not excelData:
                    excelData.append(data)
                else:
                    temp=np.array(excelData)
                    result = np.where(temp == data[0])
              
                    if not len(result[0]):
                        excelData.append(data)
                    else:
                        excelData[int(result[0])][1]+=data[1]

    print(excelData)
    
    for name, number,date,week in (excelData):
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, number)
        worksheet.write(row, col + 2, date)
        worksheet.write(row, col + 3, week)
        row += 1

    workbook.close()
