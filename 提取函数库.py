import re


def 提取地点(input):
    re_templates = {
        r"^(.*)[省|市].*法院"
    }
    for template in re_templates:
        m = re.compile(template).match(input)
        if m:
            return m.groups()[0]

def 测试提取地点():
    assert 提取地点("四川省珙县人民法院") == "四川"
    assert 提取地点("湖南省珙县人民法院") == "湖南"
    assert 提取地点("北京市朝阳区人民法院") == "北京"

def 提取犯罪数额(input):
    return


def 提取前科(input):
    result = False
    if re.compile("无前科|初犯").match(input):
        result = False
    if re.compile("有前科|再犯").match(input):
        result = True
    return result


def 提取自首(input):
    return


def 提取坦白(input):
    return


def 提取退赔(input):
    return


def 提取认罪认罚(input):
    return

if __name__ == "__main__":
    测试提取地点()