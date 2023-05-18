import re

NAME_RULES = [
    {
        "SampleType": "标准样本",
        "Formula": "^STD.*$"
    },
    {
        "SampleType": "标准曲线最低点（STD-1）",
        "Formula": "^STD.*-1$"
    },
    {
        "SampleType": "标准样本中的正常样本集合",
        "Formula": "^STD.*[-345]$"
    },
    {
        "SampleType": "质控样本",
        "Formula": "^QC[1-9]*$"
    },
    {
        "SampleType": "空白样本",
        "Formula": "^BLANK.*$"
    },
    {
        "SampleType": "QC0样本",
        "Formula": "^QC0$"
    },
    {
        "SampleType": "临床样本",
        "Formula": "^[0-9]+$"
    },
    {
        "SampleType": "所有样本",
        "Formula": ".*"
    }
]


# # 定义个SampleNameRule类，用于存储样本名的规则
# class SampleNameRule:
#     def __init__(self, sample_type, formula):
#         self.sample_type = sample_type
#         self.formula = formula

#     def __str__(self):
#         return 'key: {}, sample_type: {}, formula: {}'.format(self.sample_type, self.formula)
    
#     def __hash__(self):
#         return hash(self.sample_type + self.formula)
    
# 获取默认的样本名规则集合
def get_default_sample_name_rules():
    # 将 NAME_RULES 转换成 dict
    name_rules = {}
    for rule in NAME_RULES:
       name_rules[rule["SampleType"]] = rule["Formula"]
    return name_rules 

# 保存样本名规则 to Json file. maybe not used now.
def save_name_ruls() :
    # with open('name_rules.json', 'w') as f:
    #     json.dump(NAME_RULES, f)
    return


# 测试函数对formula进行测试
def test_formula():
    str = "STD1-1"
    for rule in NAME_RULES:
        if re.match(rule["Formula"], str):
            print(rule["SampleType"])
            # break

    print("not found")

# test_formula()