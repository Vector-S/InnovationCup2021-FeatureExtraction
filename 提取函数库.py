import re
import datetime
import pycnnum
import pandas as pd

# https://gitee.com/tsfnzjy120/LawDataAnalysis/blob/master/paper_parser/settings.py

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
    m = re.search(r"(\d+)年(\d+)月(\d+)日.*出?生于?", input, re.M + re.X)
    m2 = re.search(r"裁判日期\:\s*([0-9\.]+)\s*\n",input, re.M + re.X)
    if m:
        DOB = datetime.date(int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]))
        if m2:
            DOJ = datetime.datetime.strptime(m2.groups()[0],"%Y.%m.%d").date()
            result = (DOJ - DOB).days // 365
        else:
            result = (datetime.date.today()- DOB).days//365
        if result == 0:
            return "未知"
        return str(result)
    m = re.search(r"(\d+)岁", input, re.M + re.X)
    if m:
        return m.groups()[0]
    return "未知"

def 提取文化程度(input):
    re_templates = [
        r"(小学|初中|高中|本科|中专|大专|专科|大学|研究生|博士)(毕业|文化|肄业)",
        r"(文盲)",
    ]
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"


def 提取聋哑(input):
    result = False
    if re.search("聋|哑",input):
        result = True
    return 布尔编码(result)

def 提取盲人(input):
    result = False
    if re.search("盲人|失明",input):
        result = True
    return 布尔编码(result)

def 提取残疾人(input):
    result = False
    if re.search("残疾|残障",input):
        result = True
    return 布尔编码(result)

def 提取精神病人(input):
    result = False
    if re.search("精神病",input):
        result = True
    return 布尔编码(result)

def 提取地区(input):
    all_value = '|'.join(PROVINCE_DICT.keys())
    re_templates = [
        r"({})[省|市].*法院.*".format(all_value)
    ]
    for template in re_templates:
        m = re.search(template, input, re.M + re.X)
        if m:
            return m.groups()[0]
    return "未知"

PROVINCE_DICT = {
    '北京': 11, '天津': 12, '河北': 13, '山西': 14, '内蒙古': 15,
    '辽宁': 21, '吉林': 22, '黑龙江': 23,
    '上海': 31, '江苏': 32, '浙江': 33, '安徽': 34, '福建': 35, '江西': 36, '山东': 37,
    '河南': 41, '湖北': 42, '湖南': 43, '广东': 44, '广西': 45, '海南': 46,
    '重庆': 50, '四川': 51, '贵州': 52, '云南': 53, '西藏': 54,
    '陕西': 61, '甘肃': 62, '青海': 63, '宁夏': 64, '新疆': 65
}

def 测试提取地区():
    assert 提取地区("\n 四川省珙县人民法院\n") == "四川"
    assert 提取地区("湖南省珙县人民法院") == "湖南"
    assert 提取地区("北京市朝阳区人民法院") == "北京"
    assert 提取地区("审理法院:重庆市垫江县人民法院") == "重庆"


def 提取被害人谅解(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("被害人谅解",input):
        result = True
    return 布尔编码(result)


def 提取自首(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("自首",input):
        result = True
    if re.search("不[构成属于]*自首", input):
        result = False
    return 布尔编码(result)

def 提取坦白(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("坦白|如实供述", input):
        result = True
    if re.search("不[构成属于]*坦白", input):
        result = False

    return 布尔编码(result)


def 提取认罪态度良好(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("认罪态度良好|态度良好|态度较好|态度好",input):
        result = True
    return 布尔编码(result)

def 提取认罪认罚(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("[^不]?认罪|[^不]?认罚|如实供述", input):
        result = True
    if re.search("不[属于]+认罚|不[属于]+认罪",input):
        result = False
    return 布尔编码(result)


def 提取立功(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("立功", input):
        result = True
    return 布尔编码(result)

def 提取退赔(input):
    if "判决如下" in input:
        input = re.split("判决如下",input,1)[0]
    result = False
    if re.search("退赔|退赃|退还|赔偿", input):
        result = True
    return 布尔编码(result)

def 提取自然灾害(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("自然灾害|事故灾害|社会安全事件|突发事件", input):
        result = True
    return 布尔编码(result)

def 提取在医院盗窃(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("医院盗窃|在医院盗窃", input):
        result = True
    return 布尔编码(result)


def 提取盗窃残疾人(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("盗窃残疾人|孤寡老人|丧失劳动能力", input):
        result = True
    return 布尔编码(result)



def 提取盗窃救灾款物(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("救灾款物|移民|扶贫", input):
        result = True
    return 布尔编码(result)

def 提取一年内盗窃(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("一年内盗窃", input):
        result = True
    return 布尔编码(result)

def 提取造成严重后果(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("成严重后果", input):
        result = True
    return 布尔编码(result)

def 提取前科(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("无.*前科|没有.*前科|初犯",input):
        result = False
    if re.search("曾因犯|[^没]有.*犯?罪?前科|有前科劣迹|曾被判|日因犯.*罪|因犯.*罪\,于|刑满释放",input):
        result = True
    return 布尔编码(result)

def 提取累犯(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("累犯|系累犯|是累犯",input):
        result = True
    return 布尔编码(result)



def IsNum(s):
    if not s:
        return False
    try:
        s = s.replace(',', '')
        float(s)
        return True
    except Exception:
        pass
    try:
        s = s.replace(',', '')
        result = pycnnum.cn2num(s)
        return result != 0
    except Exception:
        return False

def ToNum(s):
    s = s.replace(',','')
    try:
        result = int(float(s))
        return result
    except:
        pass
    try:
        result = pycnnum.cn2num(s)
        return result
    except Exception as e:
        raise e



def 提取盗窃数额(input):
    # if "审理查明" in input:
    #     input = re.split("判决如下",input,1)[-1]
    if "判决如下" in input:
        input = re.split("判决如下",input,1)[0]
    # 共计
    re_templates = [
        "共计[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "共价[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "总价[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "累计[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
    ]

    total_amount = 0
    for template in re_templates:
        m = re.findall(template, input, re.M + re.X)
        if m and IsNum(m[0]):
            items = [ToNum(v) for v in m]
            total_amount = max(items)
            break
    if total_amount:
        return total_amount

    # 分计
    re_templates = [
        "认定[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "现金[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "被[盗|窃|偷].*价值[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "[盗|窃|偷]取[^\d]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "价值[人民币]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "[盗|窃|偷][人民币]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元",
        "将[人民币]*([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)余?元.*[盗|窃|偷]走",
    ]
    sum_amount = 0
    for template in re_templates:
        m = re.findall(template, input, re.M + re.X)
        if m:
            sum_amount = 0
            for value in m:
                if IsNum(value):
                    sum_amount += ToNum(value)
            break
    return max(total_amount, sum_amount)

def 测试提取盗窃数额():
    提取盗窃数额(",七部被盗手机经鉴定共计人民币4620元。\n") == 4620

    return
def 提取入户(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("入户",input):
        result = True
    return 布尔编码(result)

def 提取携带凶器(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("凶器",input):
        result = True
    return 布尔编码(result)

def 提取扒窃(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("扒窃",input):
        result = True
    return 布尔编码(result)

def 提取破坏性手段(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("破坏性手段",input):
        result = True
    return 布尔编码(result)

def 提取未遂(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("未遂",input):
        result = True
    return 布尔编码(result)

def 提取中止(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("中止",input):
        result = True
    return 布尔编码(result)

def 提取多次盗窃(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("多次盗窃",input):
        result = True
    return 布尔编码(result)



def 提取免于刑事处罚(input):
    if "本院认为" in input:
        input = re.split("本院认为",input,1)[-1]
    result = False
    if re.search("免于刑事处罚",input):
        result = True
    return 布尔编码(result)

def 提取拘役(input):
    if "判决如下" in input:
        input = re.split("判决如下",input,1)[-1]

    re_templates = [
        "有期徒刑(.*)年(.*)月",
        "有期徒刑(.*)年",
        "有期徒刑(.*)月",
    ]

    m = re.search("拘役([一二两三四五六七八九十]*)年零?([一二两三四五六七八九十]*)个?月", input, re.M + re.X)
    if m and len(m.groups()) == 2:
        year, month = m.groups()[0], m.groups()[1]
        year = ToNum(year)
        month = ToNum(month)
        return year*12 + month

    m = re.search("拘役([一二两三四五六七八九十]*)个?月", input, re.M + re.X)
    if m:
        month = m.groups()[0]
        month = ToNum(month)
        return month

    m = re.search("拘役([一二两三四五六七八九十]*)年", input, re.M + re.X)
    if m:
        year = m.groups()[0]
        year = ToNum(year)
        return year*12
    return 0

def 提取管制(input):
    if "判决如下" in input:
        input = re.split("判决如下",input,1)[-1]

    re_templates = [
        "有期徒刑(.*)年(.*)月",
        "有期徒刑(.*)年",
        "有期徒刑(.*)月",
    ]

    m = re.search("有期管制([一二两三四五六七八九十]+)年零?([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m and len(m.groups()) == 2:
        year, month = m.groups()[0], m.groups()[1]
        year = ToNum(year)
        month = ToNum(month)
        return year*12 + month

    m = re.search("有期管制([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m:
        month = m.groups()[0]
        month = ToNum(month)
        return month

    m = re.search("有期管制([一二两三四五六七八九十]+)年", input, re.M + re.X)
    if m:
        year = m.groups()[0]
        year = ToNum(year)
        return year*12
    return 0

def 提取有期徒刑(input):
    if "判决如下" in input:
        input = re.split("判决如下",input,1)[-1]

    m = re.search("有期徒刑([一二两三四五六七八九十]+)年零?([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m and len(m.groups()) == 2:
        year, month = m.groups()[0], m.groups()[1]
        year = ToNum(year)
        month = ToNum(month)
        return year*12 + month

    m = re.search("有期徒刑([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m:
        month = m.groups()[0]
        month = ToNum(month)
        return month
    m = re.search("有期徒刑([一二两三四五六七八九十]+)年", input, re.M + re.X)
    if m:
        year = m.groups()[0]
        year = ToNum(year)
        return year*12
    return 0

def 提取罚金(input):
    if "判决如下" in input or "判决结果" in input:
        input = re.split("判决如下|判决结果",input,1)[-1]
    # 数字罚金
    re_templates = [
        "罚金人民币([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)元",
        "罚金([0-9,.零一壹二贰两三叁四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿]+)元",
    ]
    for template in re_templates:
        m = re.findall(template, input, re.M + re.X)
        if m:
            result = m[0].replace(',', '')
            if IsNum(result):
                return ToNum(result)
    # 文本罚金
    re_templates = [
        "罚金人民币(.*)元",
    ]
    for template in re_templates:
        m = re.findall(template, input, re.M + re.X)
        if m:
            result = m[0]
            if IsNum(result):
                return ToNum(result)
    return 0

def 提取没收个人财产(input):
    if "判决如下" in input or "判决结果" in input:
        input = re.split("判决[结果]*如下|判决结果",input,1)[-1]
    result = False
    if re.search("没收个人财产",input):
        result = True
    return 布尔编码(result)

def 提取没收个人财产数额(input):
    if "判决如下" in input or "判决结果" in input:
        input = re.split("判决如下|判决结果",input,1)[-1]

    re_templates = [
        "没收个人财产人民币(.*)元",
    ]
    for template in re_templates:
        m = re.findall(template, input, re.M + re.X)

        if m:
            result = m[0].replace(',', '')
            if IsNum(result):
                return ToNum(result)
    return 0

def 提取缓刑(input):
    if "判决如下" in input or "判决结果" in input:
        input = re.split("判决如下|判决结果",input,1)[-1]

    m = re.search("缓刑([一二两三四五六七八九十]+)年零?([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m and len(m.groups()) == 2:
        year, month = m.groups()[0], m.groups()[1]
        year = ToNum(year)
        month = ToNum(month)
        return year*12 + month

    m = re.search("缓刑([一二两三四五六七八九十]+)个?月", input, re.M + re.X)
    if m:
        month = m.groups()[0]
        month = ToNum(month)
        return month

    m = re.search("缓刑([一二两三四五六七八九十]+)年", input, re.M + re.X)
    if m:
        year = m.groups()[0]
        year = ToNum(year)
        return year*12
    return 0


def 校准认罪认罚(filename, value):
    if "认罪认罚" in filename:
        if "无认罪认罚" in filename:
            return "否"
        return "是"
    return value

def 布尔编码(value):
    return "是" if value else "否"

if __name__ == "__main__":
    测试提取地区()
    测试提取盗窃数额()