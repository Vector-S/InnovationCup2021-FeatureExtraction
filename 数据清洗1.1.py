# -*- coding: utf-8 -*-
import os
import pandas as pd
import chardet
import csv
coding = 'utf-8' 
path1 = './file'
path2 = './file-utf-8'
path3 = './file-complete'
path_list = os.listdir(path1)
num=1
def Code(p,n):   #转化为utf-8
    print(n)
    f_2 = open(p, 'rb')
    str_1 = f_2.read()
    chardet_1 = chardet.detect(str_1)
    print(chardet_1['encoding'])
    if chardet_1['encoding']=='utf-8':
        f=pd.read_csv(p,encoding='utf-8',delimiter='\t',quoting=1)
        f.to_csv(path2+'/'+n, encoding=coding,index=None)
    else:
        f=pd.read_csv(p,encoding='gbk',delimiter='\t',quoting=1)
        f.to_csv(path2+'/'+n, encoding=coding,index=None)
    f_2.close()
    #print(f)
def strQ2B(ustring):   #全角转半角
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
def delete(n):  #处理字符
    ifn = path2+'/'+n
    ofn = path3+'/'+n
    infile = open(ifn,'r',encoding='utf-8')
    outfile = open(ofn,'w',encoding='utf-8')
    lines=infile.readlines()
    i=0
    while i<len(lines):
        #去掉文本行里面的空格、\t、\n）
        line = filter(lambda ch: ch not in '　　\t\r★ ', lines[i])
        lists = list(line)
        s=''.join(lists)
        if i<len(lines)-2 and lines[i+1]=='：\n':  #规范化冒号
            #print(lines[i+1])
            s1=lines[i+1]
            s2=lines[i+2]
            s=s[0:len(s)-1]+s1[0:len(s1)-1]+s2
            i+=2
        elif s[len(s)-2:len(s)]=='：\n':
            #print(1)
            s1=lines[i+1]
            s=s[0:len(s)-1]+s1
            i+=1
        if s[len(s)-3]=='。':  #句号收尾
            s=s[0:len(s)-2]+'\n'
        elif s[len(s)-2] in '?？！!':
            s=s[0:len(s)-2]+'。'+'\n'
        s=strQ2B(s)
        #print(s)
        outfile.write(s)
        i+=1
    infile.close()
    outfile.close()   
    
for i in path_list:
    p=path1+'/'+i
    Code(p,i)
    delete(i)
    num+=1


