# QC control 数据分析的 Main 文件。 
# 基于 Python 的 tkinter 进行主操作界面的构造
# 主界面 布局如下：
#  第一行 为布局居中的Label， H1 大的黑体字： 徐中心质控数据分析工具
#  第二行： Label为 “原始数据选择：”， 后边为一个文件输入框，点击可以选择文件
#  第三行： 居中的2个按钮。 一个是 “数据分析”按钮， 一个是 “分析配置”按钮
#  第四行： Label为“分析输出：”，布局靠右
#  第五行： 多行的文本输出框。
#  点击“数据分析”， 在第五行的文本输出框里进行 选中的文件名输出。
#  点击“配置管理”， 弹出一个新窗口，新窗口上显示一个TABLE，为5列，10行。列名为：NO, 内容， 审核公式， 参数， 样本集， 是否启用 

import tkinter as tk
from csv_helper import txt2csv
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from rules import get_default_rules
from rule_helper import check_rules
from name_helper import get_default_sample_name_rules
import datetime
import os

class QCControlApp:
    def __init__(self, master):
        self.master = master
        master.title("徐中心质控数据分析小工具")
        # 设定窗口大小 1080*720
        # 设定窗口大小为屏幕大小
        master.state("zoomed")
        # master.geometry("1080x720")
        
        row_index=0
        column_size=5

        # First row
        self.title_label = tk.Label(master, text="徐中心质控数据分析小工具", font=("Helvetica", 24))
        # 占据整个窗口大小，并居中
        self.title_label.grid(row=row_index, column=0, columnspan=column_size-1, sticky="nsew", padx=10, pady=10)
        self.owner_info = tk.Button(master, text="?", command=self.about)
        self.owner_info.grid(row=row_index, column=4, sticky="e", padx=10)
        row_index += 1

        # 插入一个横线 作为分割 , 宽度为屏幕宽度
        self.line = tk.Canvas(master, width=1024, height=2, bg="black")
        self.line.grid(row=row_index, column=0, columnspan=column_size, sticky="nsew", pady=10)
        row_index += 1

        # Second row
        self.file_label = tk.Label(master, text="原始数据选择：")
        self.file_label.grid(row=row_index, column=0, sticky="w", padx=10)
        self.file_button = tk.Button(master, text="选择文件", command=self.select_file)
        self.file_button.grid(row=row_index, column=1,sticky="w", padx=0)
        self.analyze_button = tk.Button(master, text="数据分析", command=self.analyze)
        self.analyze_button.grid(row=row_index, column=2, sticky="w", padx=0)
        self.config_sample_button = tk.Button(master, text="样本配置", command=self.config_sample)
        self.config_sample_button.grid(row=row_index, column=3,  sticky="w", padx=0)
        self.config_button = tk.Button(master, text="分析配置", command=self.config)
        self.config_button.grid(row=row_index, column=4,  sticky="w", padx=0)
        row_index += 1

        # Third row
        self.output_file = tk.Label(master, text="")
        self.output_file.grid(row=row_index, column=0, columnspan=column_size, sticky="w", padx=10)
        row_index += 1

        # 插入一个虚线  作为分割
        self.line2 = tk.Canvas(master, height=1, bg="grey")
        self.line2.grid(row=row_index, column=0, columnspan=column_size, sticky="nsew", pady=10)
        row_index += 1

        # Fourth row
        self.output_label = tk.Label(master, text="分析输出：", anchor="e")
        self.output_label.grid(row=row_index, column=0, columnspan=column_size-1, sticky="w", padx=10)
        # 插入一个Button 用于清空输出
        self.clear_button = tk.Button(master, text="清空输出", command=self.clear_output)
        self.clear_button.grid(row=row_index, column=4, sticky="e", padx=10)
        row_index += 1

        # Fifth row
        self.output_text = tk.Text(master)
        self.output_text.grid(row=row_index, column=0, columnspan=column_size, sticky="nsew", padx=10, pady=10)
        master.rowconfigure(row_index, weight=1)
        row_index += 1

    def select_file(self):
        # 检查当前日期是否晚于 2023-12-31， 如果是则弹出messagebox
        if datetime.datetime.now() > datetime.datetime(2023, 12, 31):
            messagebox.showerror("错误", "软件已经过期，请联系开发者")
            return

        file_path = filedialog.askopenfilename()
        self.output_file.config(text=file_path)

    def analyze(self):
        txt_file = app.output_file.cget("text")
        if not txt_file:
            messagebox.showerror("错误", "请先选择一个文件")
            return
        txt2csv(txt_file)
        # 在 out_put 中追加一行输入 txt_file 已经转换成 csv 数据
        self.output_text.insert(tk.END, f"1. {txt_file} 已经转换成 csv 数据\n")

        # 进行规则分析
        self.output_text.insert(tk.END, f"2. 开始检查数据有效性....")
        file_name = os.path.splitext(txt_file)[0]
        # 对下边一行代码进行异常catch处理
        # try :
        #     check_result = check_rules(file_name, rules, name_rules)
        # except 
        try:
            check_result = check_rules(file_name, rules, name_rules)
            self.output_text.insert(tk.END, f"数据检查完成。详细检查结果请查看文件[{file_name}.xls]\n")
            self.output_text.insert(tk.END, f"\n")

            # 根据check_result 输出结果
            rulekeys = check_result.keys()
            for rulekey in rulekeys:
                # 输出 rulekey
                # print(rulekey)

                match_data = check_result[rulekey]
                if match_data.empty:
                    self.output_text.insert(tk.END, f"[{rulekey}] 未匹配到数据；\n\n")
                    continue
                self.output_text.insert(tk.END, f"[{rulekey}]匹配到的数据如下：\n")
                self.output_text.insert(tk.END, f"{match_data}\n")
                self.output_text.insert(tk.END, f"\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"数据检查过程中发生错误：\n {e}\n")

        
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
    
    def config_sample(self):
        self.config_name_window = tk.Toplevel(self.master)
        self.name_table = tk.Frame(self.config_name_window)
        self.name_table.pack()

        # Column headers
        no_label = tk.Label(self.name_table, text="NO", width=5)
        no_label.grid(row=0, column=0)
        key_label = tk.Label(self.name_table, text="样本类型", width=10)
        key_label.grid(row=0, column=1)
        formula_label = tk.Label(self.name_table, text="样本名规则", width=60)
        formula_label.grid(row=0, column=2)

        # contruct rows according to name_rules（dict object type）
        row_idx = 1
        for key in name_rules.keys():
            no = tk.Label(self.name_table, text=row_idx, width=5)
            no.grid(row=row_idx, column=0)

            name_key = tk.Entry(self.name_table, width=10)
            name_key.insert(0, key)
            name_key.grid(row=row_idx, column=1)
            name_key.config(state="readonly")

            name_formula = tk.Entry(self.name_table, width=60)
            name_formula.insert(0, name_rules[key])
            name_formula.grid(row=row_idx, column=2)
            row_idx += 1

        # for i, name_rule in enumerate(name_rules, start=1):
        #     no = tk.Label(self.name_table, text=i, width=5)
        #     no.grid(row=i, column=0)

        #     content = tk.Entry(self.name_table, width=10)
        #     content.insert(0, name_rule.key)
        #     content.grid(row=i, column=1)
        #     content.config(state="readonly")

        #     sample_type = tk.Entry(self.name_table, width=10)
        #     sample_type.insert(0, name_rule.sample_type)
        #     sample_type.grid(row=i, column=2)
        #     sample_type.config(state="readonly")

        #     formula = tk.Entry(self.name_table, width=60)
        #     formula.insert(0, name_rule.formula)
        #     formula.grid(row=i, column=3)
            
         # 底部添加一个保存按钮 和 恢复默认值 按钮
        save_name_button = tk.Button(self.config_name_window, text="保存", command=self.config_name_save)
        save_name_button.pack(side="right", padx=10)
        reset_name_button = tk.Button(self.config_name_window, text="恢复默认", command=self.config_name_reset)
        reset_name_button.pack(side="right", padx=10)


    def config(self):
        self.config_window = tk.Toplevel(self.master)
        self.table = tk.Frame(self.config_window)
        self.table.pack()

        # Column headers
        no_label = tk.Label(self.table, text="NO", width=5)
        no_label.grid(row=0, column=0)
        content_label = tk.Label(self.table, text="规则类型", width=10)
        content_label.grid(row=0, column=1)
        sample_label = tk.Label(self.table, text="样本集范围", width=10)
        sample_label.grid(row=0, column=2)
        formula_label = tk.Label(self.table, text="审核公式", width=50)
        formula_label.grid(row=0, column=3)
        param_label = tk.Label(self.table, text="参数1", width=10)
        param_label.grid(row=0, column=4)
        param_label = tk.Label(self.table, text="参数2", width=10)
        param_label.grid(row=0, column=5)
        param_label = tk.Label(self.table, text="参数3", width=10)
        param_label.grid(row=0, column=6)
        # enable_label = tk.Label(self.table, text="是否启用", width=5)
        # enable_label.grid(row=0, column=7)

        # contruct rows according to QC_RULES
        # Rows
        for i, rule in enumerate(rules, start=1):
            no = tk.Label(self.table, text=rule.no, width=5)
            no.grid(row=i, column=0)

            content = tk.Entry(self.table, width=10)
            content.insert(0, rule.type)
            content.grid(row=i, column=1)
            content.config(state="readonly")

            # 将样本集范围转换为下拉框
            sample = ttk.Combobox(self.table, width=15)
            keys_as_tuples = [(key,) for key in name_rules.keys()]
            sample["value"] = keys_as_tuples
            sample.set(rule.scope)
            sample.grid(row=i, column=2)

            formula = tk.Entry(self.table, width=50)
            formula.insert(0, rule.formula)
            formula.grid(row=i, column=3)
            formula.config(state="readonly")

            param1 = tk.Entry(self.table, width=10)
            param1.insert(0, rule.param1)
            param1.grid(row=i, column=4)

            param2 = tk.Entry(self.table, width=10)
            param2.insert(0, rule.param2)
            param2.grid(row=i, column=5)

            param3 = tk.Entry(self.table, width=10)
            param3.insert(0, rule.param3)
            param3.grid(row=i, column=6)

            # 添加一列 checkbox，默认为选中状态
            # enable_var = tk.BooleanVar(value=True)
            # enable_ck = tk.Checkbutton(self.table, width=5, variable=enable_var, onvalue=True)
            # enable_ck.config(state="normal")
            # enable_ck.select()
            # enable_var.set(True)
            # enable_ck.grid(row=i, column=7)
        
        # 底部添加一个保存按钮 和 恢复默认值 按钮
        save_button = tk.Button(self.config_window, text="保存", command=self.config_save)
        save_button.pack(side="right", padx=10)
        reset_button = tk.Button(self.config_window, text="恢复默认", command=self.config_reset)
        reset_button.pack(side="right", padx=10)

    # 点击保存按钮的响应方法
    def config_save(self):
        # 保存配置文件
        # 从界面上获取数据
        for i, rule in enumerate(rules):
            # Extract values from widgets
            param1 = self.table.grid_slaves(row=i+1, column=4)[0].get()
            param2 = self.table.grid_slaves(row=i+1, column=5)[0].get()
            param3 = self.table.grid_slaves(row=i+1, column=6)[0].get()
            # enabled = self.table.grid_slaves(row=i+1, column=7)[0].cget("text")
            # enabled = self.table.grid_slaves(row=i+1, column=7)[0].cget("var")
            rule.param1 = param1
            rule.param2 = param2
            rule.param3 = param3
            # rule["Enabled"] = enabled
        # show rules
        for rule in rules:
            print(rule)
        # 关闭窗口
        self.config_window.destroy()

    # 点击恢复默认按钮的响应方法
    def config_reset(self):
        # 重置配置文件
        rules = get_default_rules()
        print("重置配置文件")
        # 关闭窗口
        self.config_window.destroy()
    
    # 点击样本名配置保存按钮的响应方法
    def config_name_save(self):
        # 保存配置文件
        # 从界面上获取数据，更新name_rules： 遍历self.name_table的所有行，获取样本名和规则，更新name_rules
        for row in range(1, self.name_table.grid_size()[1]):
            # Extract values from widgets
            key = self.name_table.grid_slaves(row=row, column=1)[0].get()
            formular = self.name_table.grid_slaves(row=row, column=2)[0].get()
            name_rules[key] = formular
        
        # show rules
        for key, value in name_rules.items():
            print(key, value)
        # 关闭窗口
        self.config_name_window.destroy()
        

    # 点击恢复默认按钮的响应方法
    def config_name_reset(self):
         # 重置配置文件
        name_rules = get_default_sample_name_rules()
        # 关闭窗口
        self.config_name_window.destroy()


    def about(self):
        messagebox.showinfo("关于", "QCControl 1.0\n\n作者：LuYuan\n\nEmail: ron.lu@qq.com")


root = tk.Tk()
app = QCControlApp(root)
rules = get_default_rules()
name_rules = get_default_sample_name_rules()
root.mainloop()