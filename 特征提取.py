import pandas as pd
import os
import re
from 提取函数库 import *

TEST = True
PROD = False

# 0 1 2 3
VERBOSE  = 0

MAX_FILE_COUNT = 200

if TEST:
    input_file_path = './testset_v1'

if PROD:
    input_file_path = './rawdata'



def unify_feature_name(name):
    if name == "地点":
        name = "地区"
    return name

def readTestFile(file_path):
    # 读取测试集，用来迭代开发时验证程序的正确性
    if VERBOSE>=0: print("Reading " + file_path)
    raw_text = open(file_path,'r').read()
    result = re.split(r"\#预期特征\n",raw_text,1)
    try:
        article_section, feature_section = result
    except Exception as e:
        print("无法读取预期特征 {}".format(file_path))
    features = {}
    for line in feature_section.split('\n'):
        line = line.strip()
        if line and not re.match(r'\s*#',line) and line.count('|') >= 2:
            feature_name, feature_value, rest = re.split(r"\s*\|\s*", line, 3)
            # feature_name = unify_feature_name(feature_name)
            features[feature_name] = feature_value
        else:
            # 无法读取
            pass
    return article_section, features


def readRawFile(filepath):
    # 读取清洗过的原始数据， 用来提取和输出特征
    lines = []
    return lines


# 地点

# 为每一个特征单独创建特征提取函数
feature_fun_map = {
                    "性别": 提取性别,
                    "年龄": 提取年龄,
                    "地区": 提取地区,
                    "文化程度" : 提取文化程度,
                    "盗窃数额": 提取盗窃数额,
                    "前科": 提取前科,
                    "自首": 提取自首,
                    "坦白": 提取坦白,
                    "退赔": 提取退赔,
                    "认罪认罚": 提取认罪认罚,
                    "罚金": 提取财产刑,}

accuracy_stats = { name: [0,0] for name in feature_fun_map.keys()}



def 统计判决如下(txts):
    rate = sum([ 1 for txt in txts if "判决如下" in txt])/len(txts)
    print("{}% 的文章含有判决如下".format(rate*100))

if __name__ == "__main__":
    print("数据读取路径: ",input_file_path)
    if TEST:
        for filename in os.listdir(input_file_path)[:MAX_FILE_COUNT]:
            extracted_features = {}
            try:
                article_section, expected_features = readTestFile(os.path.join(input_file_path,filename))
            except Exception as e:
                print("测试集无法识别: {}".format(filename))
                continue
            for key, fun in feature_fun_map.items():
                extracted_features[key] = fun(article_section)
            # RE 调试点
            temp = re.search(r"(\S*)[省|市].*法院.*", article_section, re.M + re.X)
            if VERBOSE>=1: print("特征数量: {}".format(len(expected_features)))
            for name in feature_fun_map.keys():
                if name not in extracted_features:
                    print("Feature not extracted: {}".format(name))
                    continue
                accuracy_stats[name][1] += 1
                if name not in expected_features:
                    print("Unexpected feature: {}".format(name))
                    continue
                value = expected_features[name]
                if name not in extracted_features:
                    if VERBOSE>=1: print("无法提取 {},\t     预期值 {}".format(name, value))
                elif extracted_features[name] != value:
                    if VERBOSE>=1: print("提取错误 {},\t     预期值 {},\t     提取值 {}".format(name, value, extracted_features[name]))
                else:
                    accuracy_stats[name][0] += 1
                    if VERBOSE>=1: print("提取正确 {},\t     预期值 {},\t     提取值 {}".format(name, value, extracted_features[name]))
        print("\n统计分析\n")
        统计判决如下(["判决如下", "判决如下1"])
    print("提取准确度")
    for name, stats in accuracy_stats.items():
        print("{}:\t {}/{} = {}".format(name,stats[0],stats[1],stats[0]/stats[1]))
    if PROD:
        pass



