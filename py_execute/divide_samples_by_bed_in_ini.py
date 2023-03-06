# coding = utf8 
import re,configparser,os
import pandas as pd 
import numpy as np 
import warnings
warnings.filterwarnings('ignore')
config = configparser.ConfigParser()
config.read('config.ini')
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']

def divide_sample(bed_list):
    bed_key_list = list(map(lambda x: x.split(':')[0],bed_list))
    df_received = pd.read_csv('/received/received.csv',sep=',',header=1) 
    header = '\t'.join(df_received.columns.tolist())
    # print(header)
    temp = []
    [ temp.append(bed_key) for bed_key in bed_key_list if bed_key not in temp]  # 列表推导去重。
    print(temp)                                                                 # ['BC17', 'Q120']
    for bed_key in temp:
        if not os.path.exists(f'/received/{bed_key}_received.csv'):
            with open(f'/received/{bed_key}_received.csv','w')as f0:
                f0.write(header+"\n") 
    
    bc17 = df_received[df_received['探针*']=='BC17']
    bc17.fillna('',inplace=True)
    bc17_list = bc17.values.tolist()                                            # 每一行 做成list。
    row_list = []
    [ row_list.append('\t'.join(l)) for l in bc17_list ]
    # print(row_list)
    
    for bed_key in temp:
        with open(f'/received/{bed_key}_received.csv','a+')as f:
            df = df_received[df_received['探针*']==f'{bed_key}']
            df.fillna('',inplace=True)
            row_list = []
            [ row_list.append('\t'.join(l)) for l in df.values.tolist() ]
            for row in row_list:
                f.write(row+'\n')
                

    
    
    
