# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
import pandas as pd
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


os.chdir(generate_location+"/"+parent_name+"/"+sample)
# pd.set_option('display.max_columns', None)  # 免缩略。
# 19个字段。
retain_list = ['Chr','Start','End','Ref','Alt',\
               'Func.smallrefGene','Gene.smallrefGene','AAChange.smallrefGene','ExonicFunc.smallrefGene','cytoBand',\
               'CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG',\
               'avsnp150','SIFT_score','SIFT_pred','Otherinfo11']
process_list = ['Chr','Start','End','Ref','Alt',\
               'Func.smallrefGene','Gene.smallrefGene','RNA','EXON','NCchange',\
                'AAchange','ExonicFunc.smallrefGene','cytoBand',\
               'CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG',\
               'avsnp150','SIFT_score','SIFT_pred','AO','DP','VAF']
def process():
    df_anno = pd.read_csv( sample+'.filter.hg19_multianno.txt', sep='\t')
    if df_anno.shape[1] <= 25 :
        print('终止，因为已经处理过了。')
        return    
    df_retain = df_anno[retain_list]
    i = 0
    df_retain['AO'],df_retain['DP'],df_retain['VAF'] = None,None,None
    df_retain['RNA'] = df_retain['AAChange.smallrefGene'].str.split(':', expand=True)[1]
    df_retain['EXON'] = df_retain['AAChange.smallrefGene'].str.split(':', expand=True)[2]
    df_retain['NCchange'] = df_retain['AAChange.smallrefGene'].str.split(':', expand=True)[3]
    df_retain['AAchange'] = df_retain['AAChange.smallrefGene'].str.split(':', expand=True)[4]
    for element_list in df_retain['Otherinfo11'].str.split(';',expand=False):
        for element in element_list:
            if element.split('=')[0] == 'AO':
                # print(element)
                df_retain['AO'].iloc[i] = element.split('=')[1]
            if element.split('=')[0] == 'DP':
                # print(element)
                df_retain['DP'].iloc[i] = element.split('=')[1]
        vaf_list = []
        for ii in range(len(df_retain['AO'].iloc[i].split(','))):
            vaf_list.append("%.2f%%"%(int(df_retain['AO'].iloc[i].split(',')[ii])*100/int(df_retain['DP'].iloc[i])))
        df_retain['VAF'].iloc[i] = ','.join(vaf_list)
        i += 1
    # 删除 'Otherinfo11'等字段，用完了就删掉，并调整字段顺序。
    df_result = df_retain[process_list]
    print(df_result)
    df_result.to_csv( sample+'.process.filter.hg19_multianno.txt',sep='\t', index=False)

if __name__=="__main__":
    process()

