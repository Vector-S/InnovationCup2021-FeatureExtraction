import re


def 提取地点(input):
    re_templates = {
        r"(\S*)[省|市].*法院.*"
    }
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"

def 测试提取地点():
    assert 提取地点("\n 四川省珙县人民法院\n") == "四川"
    assert 提取地点("湖南省珙县人民法院") == "湖南"
    assert 提取地点("北京市朝阳区人民法院") == "北京"

def 提取犯罪数额(input):
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
    return result.groups()[0]

if __name__ == "__main__":
    测试提取地点()