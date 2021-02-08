import pandas as pd
import os
import re
from 提取函数库 import *

TEST = True
PROD = False

if TEST:
    input_file_path = './testset'

if PROD:
    input_file_path = './rawdata'

def readTestFile(file_path):
    # 读取测试集，用来迭代开发时验证程序的正确性
    raw_text = open(file_path,'r').read()
    article_section, feature_section = re.split(r"#\s*预期特征\s*\n",raw_text,2)
    features = {}
    for line in feature_section.split('\n'):
        line = line.strip()
        if line and not re.match(r'\s*#',line) and line.count('|') >= 2:
            feature_name, feature_value, rest = re.split(r"\s*\|\s*", line, 3)
            features[feature_name] = feature_value
    return article_section, features


def readRawFile(filepath):
    # 读取清洗过的原始数据， 用来提取和输出特征
    lines = []
    return lines


# 地点

# 为每一个特征单独创建特征提取函数
feature_fun_map = {
                    "地点": 提取地点,
                    "犯罪数额": 提取犯罪数额,
                    "前科": 提取前科,
                    "自首": 提取自首,
                    "坦白": 提取坦白,
                    "退赔": 提取退赔,
                    "认罪认罚": 提取认罪认罚,

                    "财产刑": 提取财产刑,}

def 统计判决如下(txts):
    rate = sum([ 1 for txt in txts if "判决如下" in txt])/len(txts)
    print("{}% 的文章含有判决如下".format(rate*100))

if __name__ == "__main__":
    print("数据读取路径: ",os.getcwd())
    if TEST:
        for filename in os.listdir(input_file_path):
            extracted_features = {}
            article_section, expected_features = readTestFile(os.path.join(input_file_path,filename))
            print(article_section)
            for key, fun in feature_fun_map.items():
                extracted_features[key] = fun(article_section)
            # RE 调试点
            temp = re.search(r"(\S*)[省|市].*法院.*", article_section, re.M + re.X)
            for name, value in expected_features.items():
                if name not in extracted_features:
                    print("无法提取 {},\t     预期值 {}".format(name, value))
                elif extracted_features[name] != value:
                    print("提取错误 {},\t     预期值 {},\t     提取值 {}".format(name, value, extracted_features[name]))
                else:
                    print("提取正确 {},\t     预期值 {},\t     提取值 {}".format(name, value, extracted_features[name]))
        print("\n统计分析\n")
        统计判决如下(["判决如下", "判决如下1"])

    if PROD:
        pass



