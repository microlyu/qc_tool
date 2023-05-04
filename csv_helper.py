#  定义一个处理 txt 的输入文本，找到一行以 ‘Sample Name	Sample ID	Sample Type’ 开头， 将从这一行开始到文件的末尾读取出来作为一个CSV文件，CSV以空格作为分隔符
import os
import pandas as pd

def txt2csv(file_path):
    """
    This function converts a txt file to a csv file.
    It reads the txt file from the line that starts with 'Sample Name	Sample ID	Sample Type'
    and writes the content to a csv file with the same name.
    """
    file_name = os.path.splitext(file_path)[0]

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('Sample Name\tSample ID\tSample Type'):
                csv_content = ''.join(lines[i:])
                csv_file_path = file_name + '.csv'
                with open(csv_file_path, 'w') as csv_file:
                    csv_file.write(csv_content.replace('\t', ','))
                break

    # 读取csv文件，将其转换为excel文件
    # 读取csv文件
    df = pd.read_csv(file_name + '.csv', sep=',')

    # 将数据写入excel文件
    df.to_excel(file_name + '.xlsx', index=False, sheet_name='原始数据')