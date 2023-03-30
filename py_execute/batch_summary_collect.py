# -*- coding: utf-8 -*-
import pandas as pd
import shutil
from datetime import date
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('/home/chenyushao/py_execute/config.ini')
generate_location = config['generate']['location']

# receive.csv批量运行完之后，用这个脚本来收集一下全部的summary文件。

df_receive = pd.read_csv(f'/received/received.csv',sep=',',header=1)
sample_num_list = df_receive['样本编号*'].tolist()
print(sample_num_list)

for sample in sample_num_list:
    try:  # 用抛出异常的 方法 跳过 报错的样本。
        sample_parent = sample[:-2]
        summary_file = f'{generate_location}/{sample_parent}/{sample}/{sample}.summary.xlsx'
        print(summary_file)
        today=date.today().strftime("%Y%m%d")
        if not os.path.exists(f'/archive/{today}'):
            os.mkdir(f'/archive/{today}')
        shutil.copyfile(summary_file, f'/archive/{today}/{sample}.summary.xlsx')
    except:
        continue 
