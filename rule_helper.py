import pandas as pd
import numpy as np
# from rules import QC_RULES


# 保留时间(分析物)
ana_rt = 'Analyte Retention Time (min)'
# 保留时间(内标)
is_rt = 'IS Retention Time (min)' 
# RT(开始时间)
rt_start_time = 'Analyte Start Time (min)'
# RT(结束时间)
rt_end_time = 'Analyte Stop Time (min)'
# 分析物峰宽
ana_peak_width = 'Analyte Peak Width (min)'
# 分析物半峰宽
ana_half_peak_width = 'Analyte Peak Width at 50% Height (min)'
# 内标峰宽
is_peak_width = 'IS Peak Width (min)'
# 内标半峰宽
is_half_peak_width = 'IS Peak Width at 50% Height (min)'
# 分析物峰不对称性
ana_peak_asymmetry = 'Analyte Peak Asymmetry'
# 内标峰不对称性
is_peak_asymmetry = 'IS Peak Asymmetry'
# 分析物积分完整性
ana_integration_quality = 'Analyte Integration Quality'
# 内标积分完整性
is_integration_quality = 'IS Integration Quality'

# 样本准确度
sample_accuracy = 'Accuracy (%)'

# 分析物基线斜率 (%/min)
ana_slope = "Analyte Slope of Baseline (%/min)"

# 内标基线斜率 (%/min)
is_slope = "IS Slope of Baseline (%/min)"

# 分析物峰面积
ana_peak_area = "Analyte Peak Area (counts)"

# 内标峰面积
is_peak_area = "IS Peak Area (counts)"


# 定义一个主方法，用户check规则的执行。输入参数为csv文件，输出为一个list，list中的每个元素为一个dict，dict中包含了每个规则的执行结果
def check_rules(csv_file_name, rules):
    # 读取csv文件
    df = pd.read_csv(csv_file_name+".csv", sep=',')
    
    # define return object
    result = {}

    for rule in rules:
        # matched_data initiate to empty dataframe
        matched_data = pd.DataFrame()
        # accord rule.No , call different check method
        if rule.no == "1": matched_data = check_rule1(df, rule, csv_file_name)
        elif rule.no == "2": matched_data = check_rule2(df, rule, csv_file_name)
        elif rule.no == "3": matched_data = check_rule3(df, rule, csv_file_name)
        elif rule.no == "4": matched_data = check_rule4(df, rule, csv_file_name)
        elif rule.no == "5": matched_data = check_rule5(df, rule, csv_file_name)
        elif rule.no == "6": matched_data = check_rule6(df, rule, csv_file_name)
        elif rule.no == "7": matched_data = check_rule7(df, rule, csv_file_name)
        elif rule.no == "8": matched_data = check_rule8(df, rule, csv_file_name)
        elif rule.no == "9": matched_data = check_rule9(df, rule, csv_file_name)
        elif rule.no == "10": matched_data = check_rule10(df, rule, csv_file_name)
        elif rule.no == "11": matched_data = check_rule11(df, rule, csv_file_name)
        elif rule.no == "12": matched_data = check_rule12(df, rule, csv_file_name)
        elif rule.no == "13": matched_data = check_rule13(df, rule, csv_file_name)
        elif rule.no == "14": matched_data = check_rule14(df, rule, csv_file_name)
        elif rule.no == "15": matched_data = check_rule15(df, rule, csv_file_name)
        # elif rule.no == "16": check_rule16(df, rule, csv_file_name)
        else : pass
        result[rule] = matched_data
    
    return result

# 定义一个方法，用于执行规则1的检查 
# "No": "1",
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "RT（分析物-内标）的绝对值≤0.02min；",
# "Param1": "",
# "Param2": "0.02",
# "Param3": ""
def check_rule1(df, rule, excel_file_name):
    # 1.1 获取分析物和内标的RT值, 并计算差值
    df['RT_diff'] = df[ana_rt] - df[is_rt]
    # 1.2 获取差值的绝对值
    df['RT_diff_abs'] = df['RT_diff'].abs()
    # 判断是否有小于0.02的值
    target = float(rule.param2)
    print(target)

    # df['check_result'] = df['RT_diff_abs'].apply(lambda x: 'True' if x <= target else 'False', axis=1)
    tolerance = 1e-6
    df['check_result'] = df['RT_diff_abs'].apply(lambda x: 'True' if x < (target + tolerance) else 'False')
    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']
    # 输出结果
    print(df_false)

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Retention Time (min)' 'IS Retention Time (min)' 'RT_diff' 'RT_diff_abs'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_rt, is_rt, 'RT_diff', 'RT_diff_abs', 'check_result']]
    # 将数据写入excel文件的 sheet名为 rule_1
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, sheet_name='rule_1', index=False)
    
    return df_false


# 规则2的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "RT（保留时间-开始时间）≤0.1min；",
# "Param1": "",
# "Param2": "0.1",
def check_rule2(df, rule, excel_file_name):
    # 计算保留时间的差值
    df['RT_diff'] = df[ana_rt] - df[rt_start_time]
    # 判断是否有小于0.1的值
    target = float(rule.param2)

    tolerance = 1e-6
    df['check_result'] = df['RT_diff'].apply(lambda x: 'True' if x <= (target+tolerance) else 'False')
    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_2
    if df_false.empty:
        print('rule_2: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Retention Time (min)' 'Analyte Start Time (min)' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_rt, rt_start_time, 'RT_diff', 'check_result']]
    
    # 将数据写入excel文件的 sheet名为 rule_2
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_2')
    
    return df_false

# 规则3的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "RT（结束时间-保留时间）≤0.1min；",
# "Param1": "",
# "Param2": "0.1",
def check_rule3(df, rule, excel_file_name):
    # 计算保留时间的差值
    df['RT_diff'] = df[rt_end_time] - df[ana_rt]
    # 判断是否有小于0.1的值
    target = float(rule.param2)

    tolerance = 1e-6
    df['check_result'] = df['RT_diff'].apply(lambda x: 'True' if x <= (target + tolerance) else 'False')
    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_3
    if df_false.empty:
        print('rule_3: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Retention Time (min)' 'Analyte End Time (min)' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_rt, rt_end_time, 'RT_diff', 'check_result']]
    
    # 将数据写入excel文件的 sheet名为 rule_3
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_3')
    
    return df_false

# 规则4的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "分析物和内标峰宽≤0.3min；",
# "Param1": "",
# "Param2": "0.3",
def check_rule4(df, rule, excel_file_name):
    # 取得峰宽的目标值
    target = float(rule.param2)
    tolerance = 1e-6
    target = target + tolerance
    # 判断分析物的峰宽 或者 内标峰的峰宽 是否都小于目标值
    df['check_result'] = df.apply(lambda x: 'True' if (x[ana_peak_width] <= target and x[is_peak_width] <= target) else 'False', axis=1)
    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_4
    if df_false.empty:
        print('rule_4: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Width (min)' 'IS Peak Width (min)' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_peak_width, is_peak_width, 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_4
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_4')
    
    return df_false

# 规则5的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "分析物和内标半峰宽≤0.15min；",
# "Param1": "",
# "Param2": "0.15",
def check_rule5(df, rule, excel_file_name):
    # 取得半峰宽的目标值
    target = float(rule.param2)
    tolerance = 1e-6
    target = target + tolerance
    # 判断分析物的半峰宽 或者 内标峰的半峰宽 是否都小于目标值
    df['check_result'] = df.apply(lambda x: 'True' if (x[ana_half_peak_width] <= target and x[is_half_peak_width] <= target) else 'False', axis=1)
    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_5
    if df_false.empty:
        print('rule_5: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Width at 50% Height (min)' 'IS Peak Width at 50% Height (min)' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_half_peak_width, is_half_peak_width, 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_5
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_5')
    
    return df_false
    

# 规则6的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "分析物和内标的峰不对成性：0.8~2；",
# "Param1": "0.8",
# "Param2": "2",
def check_rule6(df, rule, excel_file_name):
    # 取得不对成性的目标值
    target_min = float(rule.param1)
    target_max = float(rule.param2)
    tolerance = 1e-6
    target_max = target_max + tolerance
    # 判断分析物不对成性 或者 内标峰不对成性 是否都在目标值范围内
    df['check_result'] = df.apply(lambda x: 'True' if ((target_min <= x[ana_peak_asymmetry] <= target_max) and (target_min <= x[is_peak_asymmetry] <= target_max)) else 'False', axis=1)

    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_6
    if df_false.empty:
        print('rule_6: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Asymmetry' 'IS Peak Asymmetry' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_peak_asymmetry, is_peak_asymmetry, 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_6
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_6')
    
    return df_false

# 规则7的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "分析物和内标的积分完整性：0.9~1。",
# "Param1": "0.9",
# "Param2": "1",
def check_rule7(df, rule, excel_file_name):
    # 取得积分完整性的目标值
    target_min = float(rule.param1)
    target_max = float(rule.param2)
    tolerance = 1e-6
    target_max = target_max + tolerance
    # 判断分析物积分完整性 或者 内标峰积分完整性 是否都在目标值范围内
    df['check_result'] = df.apply(lambda x: 'True' if (target_min <= x[ana_integration_quality] <= target_max) and (target_min <= x[is_integration_quality] <= target_max) else 'False', axis=1)

    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # 如果df_false 中没有数据，则返回，有数据则将数据写入excel文件的 sheet名为 rule_6
    if df_false.empty:
        print('rule_6: 没有不满足规则的数据')
        return df_false

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Integration Quality' 'IS Integration Quality' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_integration_quality, is_integration_quality, 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_7
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_7')
    
    return df_false

# 规则8的检查逻辑
# "Type": "色谱峰积分",
# "Scope": "所有样本",
# "Formula": "RT（单个样本-均值）绝对值≤0.1min",
# "Param1": "",
# "Param2": "0.1",
def check_rule8(df, rule, excel_file_name):
    # 取得RT的目标值
    target = float(rule.param2)
    tolerance = 1e-6
    target = target + tolerance

    # 获取 art的均值
    art_mean = df[ana_rt].mean()
    # df 中天际一个均值列
    df['art_mean'] = art_mean
    # 获取 RT（单个样本-均值）的列
    df["ana_rt_diff"] = df[ana_rt].apply(lambda x: x - art_mean)
    df["ana_rt_diff_abs"] = df["ana_rt_diff"].abs()

    # 判断RT（单个样本-均值）绝对值 是否都小于目标值
    df['check_result'] = df.apply(lambda x: 'True' if abs(x["ana_rt_diff_abs"]) <= target else 'False', axis=1)

    # 获取所有为False的值
    df_false = df[df['check_result'] == 'False']

    # df_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Integration Quality' 'IS Integration Quality' 'RT_diff', 'check_result'
    df_false = df_false[['Sample Name', 'Sample ID', 'Sample Type', ana_rt, 'art_mean', 'ana_rt_diff_abs', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_8
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_false.to_excel(writer, index=True, sheet_name='rule_8')
    
    return df_false


# 规则9的检查逻辑
# "Type": "标准曲线准确度",
# "Scope": "STD",
# "Formula": "每个STD样本的准确度均在85-115%之间，若有标准曲线样本准确度超出该范围，则按照偏差从大到小标识样本，并提示检查积分或者依次剔除样本",
# "Param1": "85",
# "Param2": "115"
def check_rule9(df, rule, excel_file_name):
    # filter df by Sample Name start with STD
    df_std = df[df['Sample Name'].str.startswith('STD')]

    # 取得准确度的目标值
    target_min = float(rule.param1)
    target_max = float(rule.param2)
    tolerance = 1e-6
    target_max = target_max + tolerance

    # 判断准确度是否都在目标值范围内
    df_std['check_result'] = df_std.apply(lambda x: 'True' if (target_min <= x[sample_accuracy] <= target_max) else 'False', axis=1)
    df_std_false = df_std[df_std['check_result'] == 'False']

    # 计算准确度的偏差（实际值-目标值max） 或者 目标值Min-实际值
    df_std_false['accuracy_diff'] = df_std_false.apply(lambda x: x[sample_accuracy] - target_max if x[sample_accuracy] > target_max else target_min - x[sample_accuracy], axis=1) 

    # 按 accuracy_diff 从大到小排序
    df_std_false = df_std_false.sort_values(by=['accuracy_diff'], ascending=False)

    # df_std_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Accuracy (%)' 'accuracy_diff', 'check_result'
    df_std_false = df_std_false[['Sample Name', 'Sample ID', 'Sample Type', sample_accuracy, 'accuracy_diff', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_9
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_std_false.to_excel(writer, index=True, sheet_name='rule_9')
    
    return df_std_false


# 规则10的检查逻辑
# "Type": "标准曲线数量",
# "Scope": "STD",
# "Formula": "有效标曲样本(准确度均在85-115%)不少于总标准曲线样本数量的75%",
# "Param1": "85",
# "Param2": "115"
# "Param2": "75"
def check_rule10(df, rule, excel_file_name):
    # filter df by Sample Name start with STD
    df_std = df[df['Sample Name'].str.startswith('STD')]

    # 获取STD的总数量
    std_total_count = len(df_std)

    # 取得准确度的目标值
    target_min = float(rule.param1)
    target_max = float(rule.param2)
    tolerance = 1e-6
    target_max = target_max + tolerance

    # 获取STD的有效数量
    df_std['Accuracy_Valid'] = df_std.apply(lambda x: 'True' if (target_min <= x[sample_accuracy] <= target_max) else 'False', axis=1)
    std_valid_count = len(df_std[df_std['Accuracy_Valid'] == 'True'])

    df_std_false = df_std[df_std['Accuracy_Valid'] == 'False']

    # 计算有效数量占总数量的百分比
    valid_percent = std_valid_count / std_total_count * 100

    # 判断有效数量占总数量的百分比是否大于目标值
    check_result = 'True' if valid_percent >= float(rule.param3) else 'False'
    df_std_false['valid_percent'] = valid_percent
    df_std_false['check_result'] = check_result

    # df_std 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Accuracy (%)' 'Accuracy_Valid' 'valid_percent', 'check_result'
    df_std_false = df_std_false[['Sample Name', 'Sample ID', 'Sample Type', sample_accuracy, 'Accuracy_Valid', 'valid_percent', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_10
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_std_false.to_excel(writer, index=True, sheet_name='rule_10')

    return df_std_false 

# 规则11的检查逻辑
# "Type": "标准曲线斜率",
# "Scope": "STD",
# "Formula": "≥0.99",
# "Param1": "0.99",
# "Param2": "",
# "Param3": ""
def check_rule11(df, rule, excel_file_name):
    # filter df by Sample Name start with STD
    df_std = df[df['Sample Name'].str.startswith('STD')]

    # 取得斜率的目标值
    target_min = float(rule.param1)

    # 去除ana_slope 列的值为 '#DIV/0' 的非法值
    # df_std = df_std[df_std[ana_slope] != np.nan]  # 这个地方需要注意，如果ana_slope的数据类型是float，那么这里的判断条件就是 != np.nan
    df_std = df_std[df_std[ana_slope] != '#DIV/0!']  # 这个地方需要注意，如果ana_slope的数据类型是str，那么这里的判断条件就是 != '#DIV/0!' 
    
    # 将ana_slope的数据类型转换为 float
    df_std[ana_slope] = df_std[ana_slope].astype('float')

    # 判断斜率是否都在目标值范围内
    df_std['check_result'] = df_std.apply(lambda x: 'True' if (target_min <= x[ana_slope]) else 'False', axis=1)

    df_std_false = df_std[df_std['check_result'] == 'False']

    # df_std_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Slope of Baseline (%/min)' 'check_result'
    df_std_false = df_std_false[['Sample Name', 'Sample ID', 'Sample Type', ana_slope, 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_11
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_std_false.to_excel(writer, index=True, sheet_name='rule_11')
    
    return df_std_false


# 规则12的检查逻辑
#  "Type": "残留",
# "Scope": "Blank",
# "Formula": "分析物峰面积≤标准曲线最低点（STD1）峰面积均值g的20%；",
# "Param1": "",
# "Param2": "20",
# "Param3": ""
def check_rule12(df, rule, excel_file_name):
    # filter df by Sample Name start with Blank
    df_blank = df[df['Sample Name'].str.startswith('BLANK')]

    # 取得STD1的峰面积均值
    df_std1 = df[df['Sample Name'].str.startswith('STD')]
    std1_area_mean = df_std1[ana_peak_area].mean()   # 最小值没有体现 TODO

    # 计算标准曲线最低点（STD1）峰面积均值g的20%
    target_max = std1_area_mean * float(rule.param2) / 100
    df_blank['20% of STD1 Area Mean'] = target_max
    tolerance = 1e-6
    target_max = target_max + tolerance
    
    # 判断分析物峰面积是否都在目标值范围内
    df_blank['check_result'] = df_blank.apply(lambda x: 'True' if (x[ana_peak_area] <= target_max) else 'False', axis=1)

    df_blank_false = df_blank[df_blank['check_result'] == 'False']

    # df_sample_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Area' '20% of STD1 Area Mean' 'check_result'
    df_blank_false = df_blank_false[['Sample Name', 'Sample ID', 'Sample Type', ana_peak_area, '20% of STD1 Area Mean', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_12
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_blank_false.to_excel(writer, index=True, sheet_name='rule_12')
    
    return df_blank_false

# 规则13的检查逻辑
# "Type": "残留",
# "Scope": "Blank",
#   "Formula": "内标峰面积≤内标峰面积均值的5%",
# "Param1": "",
# "Param2": "5",
# "Param3": ""
def check_rule13(df, rule, excel_file_name):
    # filter df by Sample Name start with Blank
    df_blank = df[df['Sample Name'].str.startswith('BLANK')]

    # 取得内标峰面积均值
    df_std1 = df[df['Sample Name'].str.startswith('STD')]
    is_area_mean = df_std1[is_peak_area].mean()

    # 计算内标峰面积均值的5%
    target_max = is_area_mean * float(rule.param2) / 100
    df_blank['5% of IS Area Mean'] = target_max
    tolerance = 1e-6
    target_max = target_max + tolerance
    
    # 判断内标峰面积是否都在目标值范围内
    df_blank['check_result'] = df_blank.apply(lambda x: 'True' if (x[is_peak_area] <= target_max) else 'False', axis=1)

    df_blank_false = df_blank[df_blank['check_result'] == 'False']

    # df_sample_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'IS Peak Area' '5% of IS Area Mean' 'check_result'
    df_blank_false = df_blank_false[['Sample Name', 'Sample ID', 'Sample Type', is_peak_area, '5% of IS Area Mean', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_13
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_blank_false.to_excel(writer, index=True, sheet_name='rule_13')
    
    return df_blank_false

# 规则14的检查逻辑
# "Type": "内标干扰",
# "Scope": "QC0",
# "Formula": "分析物峰面积≤标准曲线最低点（STD1）峰面积均值的20%",
# "Param1": "",
# "Param2": "20",
# "Param3": ""
def check_rule14(df, rule, excel_file_name):
    # filter df by Sample Name start with QC0
    df_qc0 = df[df['Sample Name'].str.startswith('QC0')]

    # 取得STD1的峰面积均值
    df_std1 = df[df['Sample Name'].str.startswith('STD')]
    std1_area_mean = df_std1[ana_peak_area].mean()   # 最小值没有体现 TODO

    # 计算标准曲线最低点（STD1）峰面积均值g的20%
    target_max = std1_area_mean * float(rule.param2) / 100
    df_qc0['20% of STD1 Area Mean'] = target_max
    tolerance = 1e-6
    target_max = target_max + tolerance
    
    # 判断分析物峰面积是否都在目标值范围内
    df_qc0['check_result'] = df_qc0.apply(lambda x: 'True' if (x[ana_peak_area] <= target_max) else 'False', axis=1)

    df_qc0_false = df_qc0[df_qc0['check_result'] == 'False']

    # df_sample_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Area' '20% of STD1 Area Mean' 'check_result'
    df_qc0_false = df_qc0_false[['Sample Name', 'Sample ID', 'Sample Type', ana_peak_area, '20% of STD1 Area Mean', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_14
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_qc0_false.to_excel(writer, index=True, sheet_name='rule_14')
    
    return df_qc0_false

# 规则15的检查逻辑
# "Type": "内标峰面积",
# "Scope": "临床样本",
# "Formula": "每个临床样本内标峰面积在所有临床样本内标峰面积均值的50~150%之间",
# "Param1": "50",
# "Param2": "150",
# "Param3": ""
def check_rule15(df, rule, excel_file_name):
    # filter out 临床样本
    # filter df by Sample Name , construct by only digtal 
    df_unknow = df[df['Sample Name'].str.match(r'^\d+$')]
    

    # 取得所有临床样本内标峰面积均值
    is_area_mean = df_unknow[is_peak_area].mean()

    # 计算所有临床样本内标峰面积均值的50~150%
    target_min = is_area_mean * float(rule.param1) / 100
    target_max = is_area_mean * float(rule.param2) / 100
    df_unknow['50% of IS Area Mean'] = target_min
    df_unknow['150% of IS Area Mean'] = target_max
    tolerance = 1e-6
    target_min = target_min - tolerance
    target_max = target_max + tolerance
    
    # 判断分析物峰面积是否都在目标值范围内
    df_unknow['check_result'] = df_unknow.apply(lambda x: 'True' if (x[is_peak_area] >= target_min and x[is_peak_area] <= target_max) else 'False', axis=1)

    df_unkown_false = df_unknow[df_unknow['check_result'] == 'False']

    # df_sample_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Area' '50% of IS Area Mean' '150% of IS Area Mean' 'check_result'
    df_unkown_false = df_unkown_false[['Sample Name', 'Sample ID', 'Sample Type', is_peak_area, '50% of IS Area Mean', '150% of IS Area Mean', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_15
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_unkown_false.to_excel(writer, index=True, sheet_name='rule_15')
    
    return df_unkown_false

# 规则16的检查逻辑
# "Type": "定量/定性比值",
# "Scope": "临床样本",
# "Formula": "当临床样本qn和ql通道信噪比均≥10时， 分析物qn/ql通道峰面积比值应在标准曲线的三个点（STD3~5）/或者通过验证得来的比值分析物峰面积比值均值的80~120%之间；所有分析物均需执行该操作",
# "Param1": "80",
# "Param2": "120",
# "Param3": ""
def check_rule16(df, rule, excel_file_name):
    # filter out 临床样本
    # filter df by Sample Name , construct by only digtal 
    df_unknow = df[df['Sample Name'].str.match(r'^\d+$')]

    # 取得所有临床样本内标峰面积均值
    ana_area_mean = df_unknow[ana_peak_area].mean()

    # 计算所有临床样本内标峰面积均值的80~120%
    target_min = ana_area_mean * float(rule.param1) / 100
    target_max = ana_area_mean * float(rule.param2) / 100
    df_unknow['80% of Analyte Area Mean'] = target_min
    df_unknow['120% of Analyte Area Mean'] = target_max
    tolerance = 1e-6
    target_min = target_min - tolerance
    target_max = target_max + tolerance
    
    # 判断分析物峰面积是否都在目标值范围内
    df_unknow['check_result'] = df_unknow.apply(lambda x: 'True' if (x[ana_peak_area] >= target_min and x[ana_peak_area] <= target_max) else 'False', axis=1)

    df_unkown_false = df_unknow[df_unknow['check_result'] == 'False']

    # df_sample_false 中保留 'Sample Name'  'Sample ID' 'Sample Type' 'Analyte Peak Area' '80% of Analyte Area Mean' '120% of Analyte Area Mean' 'check_result'
    df_unkown_false = df_unkown_false[['Sample Name', 'Sample ID', 'Sample Type', ana_peak_area, '80% of Analyte Area Mean', '120% of Analyte Area Mean', 'check_result']]

    # 将数据写入excel文件的 sheet名为 rule_16
    with pd.ExcelWriter(excel_file_name + '.xlsx', mode='a') as writer:
        df_unkown_false.to_excel(writer, index=True, sheet_name='rule_16')
    
    return df_unkown_false