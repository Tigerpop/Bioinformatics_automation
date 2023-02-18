# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys,copy
from multiprocessing import Process,Pool
import pandas as pd 
import numpy as np
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg19_fasta = config['reference_document']['fasta']
toolbox_and_RefFile = config['reference_document']['toolbox_and_RefFile']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

def pollution_filter():
    df = pd.read_csv(toolbox_and_RefFile+"/"+'pollution_storehouse.txt',sep='\t')
    num_list = ['1537', '1567', '1568', '1596', '1597', '3292', '3294', '3295', '4409']
    vaf_list = [f'VAF_{num}' for num in num_list]
    vaf_list.extend(['frequency', 'sum', 'avg', 'max', 'min'])
    for vaf_ele in vaf_list:                                             # 每一个字符串 2.3% 改为float类型方便计算。 最后为了美观还能再改回去。
        df[vaf_ele] = df[vaf_ele].str.strip("%").astype(float) / 100
    df_avg = df[['Chr','Start','avg']]
    df_avg['Chr_Start'] = df['Chr']+"_"+df['Start'].astype(str)
    chr_start_list = df_avg['Chr_Start'].tolist()
    poll_avg_list = df_avg['avg'].tolist()
    print(chr_start_list)
    # print(poll_avg_list)
    # print(df_avg)
    
    
    merge_vcf = generate_location+"/"+sample_path+"/"+sample+".merge.vcf"
    poll_pass_vcf = generate_location+"/"+sample_path+"/"+sample+".pollpass.vcf"

    
    with open(merge_vcf,'r')as f0,open(poll_pass_vcf,'w')as f1:
        i,j,k=0,0,0
        for fields in f0:
            j += 1
            lines = fields.split('\t')
            if len(lines)>1 and lines[0][0]!="#":       # 进入主体。
                Chr,Start = lines[0],str(lines[1])
                Chr_Start = Chr+"_"+Start
                print(Chr_Start,' ',i)
                if Chr_Start in chr_start_list :        # 出现在污染库中。
                    i += 1
                    print('在pollution_restore中。i=',i)
                    line = lines[7]
                    DP = float(re.findall(r";DP=(\d+?);",line)[0])
                    AO_list = list(map(float,re.findall(r';AO=(.+?);',line)[0].split(',')))
                    AO = sum(AO_list)/len(AO_list)
                    VAF = AO/DP
                    if poll_avg_list[chr_start_list.index(Chr_Start)]*2 > VAF:   # vaf 小于 污染库此位置平均值的2倍。
                        print('真实被过滤掉,位置在:',Chr_Start)
                        k += 1
                        # 过滤掉此行。
                        continue 
            f1.write(fields) 
        print('一共有%d个位置出现在污染库中,%d被过滤掉。'%(i,k))  
        print('vcf文件一共大约有%d个位置。'%j)


if __name__ == '__main__':
    pollution_filter()
