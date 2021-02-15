import re


def 提取性别(input):
    re_templates = [
        r"(男|女)",
    ]
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"

def 提取年龄(input):
    m = re.search(r"(0-9)岁", input, re.M + re.X)
    if m:
        return m.groups()[0]
    m = re.search(r"([0-9]*)年.*出生", input, re.M + re.X)
    if m:
        year_of_birth = int(m.groups()[0])
        return 2021 - year_of_birth - 1
    return "未知"

def 提取文化程度(input):
    re_templates = [
        r"(小学|初中|高中|本科|研究生)文化",
    ]
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"


def 提取地区(input):
    re_templates = [
        r":(\S*)[省|市].*法院.*",
        r"(\S*)[省|市].*法院.*"
    ]
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"

def 测试提取地点():
    assert 提取地点("\n 四川省珙县人民法院\n") == "四川"
    assert 提取地点("湖南省珙县人民法院") == "湖南"
    assert 提取地点("北京市朝阳区人民法院") == "北京"
    assert 提取地点("审理法院:重庆市垫江县人民法院") == "重庆"

def 提取盗窃数额(input):
    return "未知"

def 布尔编码(value):
    return "有" if value else "无"


def 提取前科(input):
    result = False
    if re.search("无前科|初犯",input):
        result = False
    if re.search("有前科|再犯|有前科劣迹",input):
        result = True
    return 布尔编码(result)


def 提取自首(input):
    result = False
    if re.search("自首",input):
        result = True
    return 布尔编码(result)

def 提取坦白(input):
    result = False
    if re.search("坦白",input):
        result = True
    return 布尔编码(result)


def 提取退赔(input):
    result = False
    if re.search("退赔", input):
        result = True
        return "有"

    return "未知"


def 提取认罪认罚(input):
    result = False
    if re.search("认罪|认罚", input):
        result = True
    return 布尔编码(result)

def 提取自由刑(input):

    return

def 提取财产刑(input):
    result = re.search("罚金人民币(.*)元",input)
    if result:
        return result.groups()[0]
    return "未知"

if __name__ == "__main__":
    测试提取地点()