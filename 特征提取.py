import pandas as pd
import os
from 提取函数库 import *

TEST = True
PRODUCTION = False

if TEST:
    input_file_path = './testset'

if PRODUCTION:
    input_file_path = './rawdata'

def readTestFile(filepath):
    # 读取测试集，用来迭代开发时验证程序的正确性
    lines = []
    features = {}

    return lines, features


def readRawFile(filepath):
    # 读取清洗过的原始数据， 用来提取和输出特征
    lines = []
    return lines


# 地点


# 为每一个特征单独创建特征提取函数
feature_fun_map = {
                    "地点": 提取地点,
                    "犯罪数额": 提取犯罪数额,
                    "前科": 提取前科}

def 检测判决如下(txts):
    rate = sum([ 1 for txt in txts if "判决如下" in txt])/len(txts)
    print("{}% 的文章含有判决如下".format(rate*100))

if __name__ == "__main__":
    print("program start")
    print(os.getcwd())
    for filename in os.listdir(input_file_path):
        features = {}
        lines = readTestFile(os.path.join(input_file_path,filename))
        for key, fun in feature_fun_map.items():
            features[key] = fun(lines)
    检测判决如下(["判决如下", "判决如下1"])


