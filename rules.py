
JSON_RULES = [
    {
        "No": "1",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "RT（分析物-内标）的绝对值≤0.02min；",
        "Param1": "",
        "Param2": "0.02",
        "Param3": ""
    },
    {
        "No": "2",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "RT（保留时间-开始时间）≤0.1min；",
        "Param1": "",
        "Param2": "0.1",
        "Param3": ""
    },
    {
        "No": "3",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "RT（结束时间-保留时间）≤0.1min；",
        "Param1": "",
        "Param2": "0.1",
        "Param3": ""
    },
    {
        "No": "4",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "分析物和内标峰宽≤0.3min；",
        "Param1": "",
        "Param2": "0.3",
        "Param3": ""
    },
    {
        "No": "5",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "分析物和内标半峰宽≤0.15min；",
        "Param1": "",
        "Param2": "0.15",
        "Param3": ""
    },
    {
        "No": "6",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "分析物和内标的峰不对成性：0.8~2；",
        "Param1": "0.8",
        "Param2": "2",
        "Param3": ""
    },
    {
        "No": "7",
        "Type": "色谱峰积分",
        "Scope": "所有样本",
        "Formula": "分析物和内标的积分完整性：0.9~1。",
        "Param1": "0.9",
        "Param2": "1",
        "Param3": ""
    },
    {
        "No": "8",
        "Type": "保留时间偏差",
        "Scope": "所有样本",
        "Formula": "RT（单个样本-均值）绝对值≤0.1min或在-0.1~0.1min之间",
        "Param1": "-0.1",
        "Param2": "0.1",
        "Param3": ""
    },
    {
        "No": "9",
        "Type": "标准曲线准确度",
        "Scope": "STD",
        "Formula": "每个STD样本的准确度均在85-115%之间，若有标准曲线样本准确度超出该范围，则按照偏差从大到小标识样本，并提示检查积分或者依次剔除样本",
        "Param1": "85",
        "Param2": "115",
        "Param3": ""
    },
    {
        "No": "10",
        "Type": "标准曲线数量",
        "Scope": "STD",
        "Formula": "有效标曲样本(准确度均在85-115%之间)不少于总标准曲线样本数量的75%",
        "Param1": "85",
        "Param2": "115",
        "Param3": "75"
    },
    {
        "No": "11",
        "Type": "标准曲线斜率",
        "Scope": "STD",
        "Formula": "≥0.99",
        "Param1": "0.99",
        "Param2": "",
        "Param3": ""
    },
    {
        "No": "12",
        "Type": "残留",
        "Scope": "Blank",
        "Formula": "分析物峰面积≤标准曲线最低点（STD1）峰面积均值g的20%；",
        "Param1": "",
        "Param2": "20",
        "Param3": ""
    },
    {
        "No": "13",
        "Type": "残留",
        "Scope": "Blank",
        "Formula": "内标峰面积≤内标峰面积均值的5%",
        "Param1": "",
        "Param2": "5",
        "Param3": ""
    },
    {
        "No": "14",
        "Type": "内标干扰",
        "Scope": "QC0",
        "Formula": "分析物峰面积≤标准曲线最低点（STD1）峰面积均值的20%",
        "Param1": "",
        "Param2": "20",
        "Param3": ""
    },
    {
        "No": "15",
        "Type": "内标峰面积",
        "Scope": "临床样本",
        "Formula": "每个临床样本内标峰面积在所有临床样本内标峰面积均值的50~150%之间",
        "Param1": "50",
        "Param2": "150",
        "Param3": ""
    },
    {
        "No": "16",
        "Type": "定量/定性比值",
        "Scope": "临床样本",
        "Formula": "当临床样本qn和ql通道信噪比均≥10时， 分析物qn/ql通道峰面积比值应在标准曲线的三个点（STD3~5）/或者通过验证得来的比值分析物峰面积比值均值的80~120%之间；所有分析物均需执行该操作",
        "Param1": "80",
        "Param2": "120",
        "Param3": ""
    }
]

# 定义个Rule的类
class Rule:
    def __init__(self, no, type, scope, formula, param1, param2, param3):
        self.no = no
        self.type = type
        self.scope = scope
        self.formula = formula
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def __str__(self):
        return "规则%s: 类型(%s), 样本范围(%s), 检验内容（%s）" % (self.no, self.type, self.scope, self.formula)

    # 定义可散列的方法
    def __hash__(self):
        return hash(self.no + self.type + self.scope + self.formula)

def get_default_rules():
    default_rules = []
    for jsonrule in JSON_RULES:
        rule = Rule(jsonrule["No"], jsonrule["Type"], jsonrule["Scope"], jsonrule["Formula"], jsonrule["Param1"], jsonrule["Param2"], jsonrule["Param3"])
        default_rules.append(rule)
        
    return default_rules