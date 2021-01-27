# -*- coding: utf-8 -*-
import docx
import os
from win32com import client as wc
def doc_to_docx(p):  #doc转docx
    doc = word.Documents.Open(p) 
    doc.SaveAs("{}x".format(p), 12)
    doc.Close() 
def docx_to_txt(p,n):  #docx转txt
    file = docx.opendocx(p)
    text = docx.getdocumenttext(file)
    file = open(path1+'\\'+'湖南-无认罪认罚'+str(n)+'.txt','w',encoding="utf-8")
    for i in range(len(text)):
        file.write(str(text[i]))
        file.write('\n')
    file.close();

num=0
path1 = 'C:\\Users\\HH\\Desktop\\大三上\\法学\\湖南-无认罪认罚-3829'
path_list = os.listdir(path1)
word = wc.Dispatch("Word.Application") 
for i in path_list:
    if 'txt' in i:
        continue
    p=path1+'\\'+i
    print(p)
    doc_to_docx(p)
    os.remove(p)
    docx_to_txt(p+'x',num)
    os.remove(p+'x')
    num+=1
word.Quit()
