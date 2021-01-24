# -*- coding: utf-8 -*-
import os
import pandas as pd
coding = 'utf-8' 
path1 = './file'
path2 = './file-utf-8'
path_list = os.listdir(path1)
num=1
def Code(p,n):   #转化为utf-8
    f=pd.read_csv(p,encoding='gbk',delimiter='\t')
    f.to_csv(path2+'/'+str(n)+'.txt', encoding=coding,index=None)
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
def delete(n):  #删除字符
    ifn = path2+'/'+str(n)+'.txt'
    ofn = path2+'/'+str(n-1)+'.txt'
    infile = open(ifn,'r',encoding='utf-8')
    outfile = open(ofn,'w',encoding='utf-8')
    for eachline in infile.readlines():
        #去掉文本行里面的空格、\t、\n）
        lines = filter(lambda ch: ch not in '　　\t\r★ ', eachline)
        lists = list(lines)
        s=''.join(lists)
        #print(s)
        s=strQ2B(s)
        outfile.write(s)
    infile.close()
    outfile.close()
for i in path_list:
    p=path1+'/'+i
    Code(p,num)
    delete(num)
    num+=1
