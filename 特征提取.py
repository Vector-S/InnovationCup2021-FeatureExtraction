import pandas as pd
import os
import re
from 提取函数库 import *

TEST = True
CLEAN = False
PROD = True

if PROD:
    TEST =False
# 0 1 2 3
VERBOSE = 0

MAX_FILE_COUNT = -1

target_files = []

FOCUS_FEATURE = ["文化程度", "地区", "认罪态度良好", "前科"]



FOCUS_FEATURE = ["罚金"]

FOCUS_FEATURE = ["年龄"]

FOCUS_FEATURE = ["有期徒刑","拘役","管制","罚金", "盗窃数额"]

FOCUS_FEATURE = ["没收个人财产", "没收个人财产数额"]

version_id = "v1"

if TEST:
    input_file_path = './testset_v1'
    # target_files = ["165.txt"]
    output_file_path = './processed'

if CLEAN:
    clean_file_path = './ilegalfiles'

if PROD:
    # target_files = ["重庆认罪认罚5622.txt"]
    input_file_path = './rawdata/rawdata_v1'
    input_file_path = "/Users/vectorshan/Desktop/清洗后数据/汇总"
    output_file_path = './processed'
    if version_id:
        output_file_path += "/" + version_id
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

def unify_feature_name(name):
    if name == "地点":
        name = "地区"
    if name == "罚金刑":
        name = "罚金"
    if name in ["退赃退赔"]:
        name = "退赔"
    if name == "自然灾害、事故灾害、社会安全事件等突发事件期间,在事件发生地盗窃":
        name = "自然灾害"
    if name == "在医院盗窃病人或者其亲友财物的":
        name = "在医院盗窃"
    if name == "盗窃残疾人、孤寡老人、丧失劳动能力人的财物的":
        name = "盗窃残疾人"
    if name == "盗窃救灾、抢险、防汛、优抚、扶贫、移民、救济款物的":
        name = "盗窃救灾款物"
    if name == "一年内曾因盗窃受过行政处罚":
        name = "一年内盗窃"
    if name == "因盗窃造成严重后果的":
        name = "造成严重后果"
    if name == "携带凶器盗窃":
        name = "携带凶器"
    return name



def unify_feature_value(name,value):
    if value in ["是", "有"]:
        value = "是"
    if value in ["无", "否"]:
        value = "否"
    if value in [""]:
        value = "未知"
    if IsNum(value):
        value = ToNum(value)
    if name in ["盗窃数额","缓刑","没收个人财产数额"] and  value in ["未知", "否", "无"]:
        value = 0
    if name in ["有期徒刑","拘役", "管制"]:
        value = ToMonth(str(value))
    return value

def readTestFile(file_path):
    # 读取测试集，用来迭代开发时验证程序的正确性
    if VERBOSE>=0: print("Reading " + file_path)
    raw_text = open(file_path,'r').read()
    result = re.split(r"\#\s*预期特征\s*\n",raw_text,1)
    try:
        article_section, feature_section = result
    except Exception as e:
        print("无法读取预期特征 {}".format(file_path))
        return
    features = {}
    reasons = {}
    for line in feature_section.split('\n'):
        line = line.strip()
        if line and not re.match(r'\s*#',line) and line.count('|') >= 2:
            feature_name, feature_value, reason = re.split(r"\s*\|\s*", line, 2)
            feature_name = unify_feature_name(feature_name)
            feature_value = unify_feature_value(feature_name, feature_value)
            features[feature_name] = feature_value
            reasons[feature_name] = reason
        else:
            # 无法读取
            pass
    return article_section, features, reasons


def readRawFile(file_path):
    # 读取清洗过的原始数据， 用来提取和输出特征
    if VERBOSE >= 0: print("Reading " + file_path)
    article = open(file_path, 'r').read()
    if "预期特征" in article:
        article = re.split(r"\#\s*预期特征\s*\n",article)[0]
    if "提取结果" in article:
        article = re.split(r"\#\s*提取结果\s*\n",article)[0]
    return article

def ToMonth(value):
    year,month = 0,0
    m = re.search("([\d]+)Y",value)
    if m:
        year = int(m.groups()[0])
    m = re.search("([\d]+)M",value)
    if m:
        month = int(m.groups()[0])
    return year*12 + month

# 地点

# 为每一个特征单独创建特征提取函数

feature_fun_map ={
        "性别" : 提取性别,
        "年龄" : 提取年龄,
        "文化程度" : 提取文化程度,
        "聋哑" : 提取聋哑,
        "盲人" : 提取盲人,
        "残疾人" : 提取残疾人,
        "精神病人" : 提取精神病人,
        "地区" : 提取地区,
        "认罪认罚" : 提取认罪认罚,
        "被害人谅解" : 提取被害人谅解,
        "自首" : 提取自首,
        "坦白" : 提取坦白,
        "认罪态度良好" : 提取认罪态度良好,
        "立功" : 提取立功,
        "退赔" : 提取退赔,
        "自然灾害" : 提取自然灾害,
        "在医院盗窃" : 提取在医院盗窃,
        "盗窃残疾人" : 提取盗窃残疾人,
        "盗窃救灾款物" : 提取盗窃救灾款物,
        "一年内盗窃" : 提取一年内盗窃,
        "造成严重后果" : 提取造成严重后果,
        "前科" : 提取前科,
        "累犯" : 提取累犯,
        "盗窃数额" : 提取盗窃数额,
        "入户" : 提取入户,
        "携带凶器" : 提取携带凶器,
        "扒窃" : 提取扒窃,
        "破坏性手段" : 提取破坏性手段,
        "未遂" : 提取未遂,
        "中止" : 提取中止,
        "多次盗窃" : 提取多次盗窃,
        "免于刑事处罚" : 提取免于刑事处罚,
        "拘役" : 提取拘役,
        "管制" : 提取管制,
        "有期徒刑" : 提取有期徒刑,
        "罚金" : 提取罚金,
        "没收个人财产" : 提取没收个人财产,
        "没收个人财产数额" : 提取没收个人财产数额,
        "缓刑" : 提取缓刑,
        }




def format_function_names(keys):
    print("{")
    for key in keys:
        print("\t\"{}\" : 提取{},".format(key,key))
    print("}")


def exclude_file(article):
    for word in ["共同犯罪","主犯","从犯","共犯","数罪并罚"]:
        if word in article:
            return True
    return False

accuracy_stats = { name: [0,0] for name in feature_fun_map.keys()}

word_stats_list = ["判决如下","裁判日期", "法院认为","数罪并罚","本院认为" ]
word_stats = {word: [0,0] for word in word_stats_list}

def update_word_stats(filename,article):
    for word in word_stats.keys():
        word_stats[word][1]+=1
        if word in article:
            word_stats[word][0] +=1
        else:
            if VERBOSE >= 1: print("{} not in {}".format(word, filename))

def report_word_stats():
    for word, stats in word_stats.items():
        print("{:.1f}% 文章含有 {}".format(stats[0]/stats[1]*100,word))

if __name__ == "__main__":
    print("数据读取路径: ",input_file_path)

    col_names = ["文件名"] + list(feature_fun_map.keys())
    result_dict = { col:[] for col in col_names}

    if TEST:
        for filename in os.listdir(input_file_path)[:MAX_FILE_COUNT]:
            if target_files and filename not in target_files:
                continue
            extracted_features = {}
            try:
                article_section, expected_features, reasons = readTestFile(os.path.join(input_file_path,filename))
            except Exception as e:
                print("测试集无法识别: {} {}".format(filename,e))
                continue
            if exclude_file(article_section):
                print("样本被剔除")
                continue

            registered_features_count = 39
            if len(expected_features) != registered_features_count:
                print("{} 特征数不符， 读取 {}， 预期 {}".format(filename,len(expected_features), registered_features_count))
                if CLEAN:
                    os.rename(os.path.join(input_file_path,filename),os.path.join(clean_file_path,filename))

            # 合法样本, 开始处理

            for key, fun in feature_fun_map.items():
                extracted_features[key] = fun(article_section)
                result_dict[key].append(extracted_features[key])
            result_dict["文件名"].append(filename)
            # RE 调试点
            temp = re.search(r"(\S*)[省|市].*法院.*", article_section, re.M + re.X)

            update_word_stats(filename, article_section)
            if extracted_features["盗窃数额"]<1000:
                print(extracted_features["盗窃数额"])
                continue
            for name in feature_fun_map.keys():
                if name not in extracted_features:
                    print("Feature not extracted: {}".format(name))
                    continue

                accuracy_stats[name][1] += 1
                if name not in expected_features:
                    print("Unexpected feature {} in file {}".format(name,filename))
                    continue
                value = expected_features[name]
                if str(extracted_features[name]) != str(value):
                    if VERBOSE>=1 or name in FOCUS_FEATURE :
                        print("{} 提取错误 {},\t     预期值 {},\t     提取值 {},\t {}".format(filename, name, value, extracted_features[name],reasons[name]))
                else:
                    accuracy_stats[name][0] += 1
                    if VERBOSE>=1: print("提取正确 {},\t     预期值 {},\t     提取值 {}".format(name, value, extracted_features[name]))
        print("\n统计分析\n")



        print("提取准确度")
        for name, stats in accuracy_stats.items():
            print("{}:\t {}/{} = {:.1f}%".format(name, stats[0], stats[1], stats[0]/stats[1]*100))
    if PROD:
        extracted_features = {}
        for filename in os.listdir(input_file_path)[:MAX_FILE_COUNT]:
            if target_files and filename not in target_files:
                continue
            try:
                article = readRawFile(os.path.join(input_file_path, filename))
            except Exception as e:
                print("文件无法读取: {} {}".format(filename, e))
                continue

            update_word_stats(filename, article)

            if exclude_file(article):
                print("样本被剔除")
                continue


            for key, fun in feature_fun_map.items():
                value = fun(article)
                if key == "认罪认罚":
                    value = 校准认罪认罚(filename, value)
                extracted_features[key] = value
                result_dict[key].append(value)
            result_dict["文件名"].append(filename)


            OUTPUT_PROD_LOG= False
            if OUTPUT_PROD_LOG:
                with open(os.path.join(output_file_path,filename),'w') as file:
                    file.write(article)
                    file.write("\n# 提取结果\n\n")
                    for key, value in extracted_features.items():
                        file.write("{} | {}\n".format(key,value))
    result_df = pd.DataFrame(data=result_dict)
    result_df = result_df[(result_df["盗窃数额"] >= 1000) | (result_df["扒窃"] == "是") | (result_df["入户"] == "是") | (result_df["携带凶器"] == "是") | (result_df["多次盗窃"] == "是")]
    result_df = result_df[result_df["地区"].isin({"北京","天津","河北","湖南","重庆"})]
    result_df.reset_index(drop=True,inplace=True)
    print(result_df)
    result_df.to_csv(os.path.join(output_file_path,"final_dataset.csv"))
    report_word_stats()





