# -*- coding: utf-8 -*-
import pandas as pd
import re,os,sys
import warnings
warnings.filterwarnings('ignore')


sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
annover_txt = sys.argv[4]

useful_17_gene = ['AKT1','ALK','BCL2L11','BRAF',\
               'EGFR','ERBB2','KRAS','MAP2K1',\
               'MET','NRAS','NTRK1','NTRK2',\
               'NTRK3','RET','ROS1','PTEN',\
               'PIK3CA']
retain_list = ['Chr','Start','End','Ref','Alt',\
               'Func.smallrefGene','Gene.smallrefGene','AAChange.smallrefGene','ExonicFunc.smallrefGene','cytoBand',\
               'CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG',\
               'avsnp150','SIFT_score','SIFT_pred','Otherinfo11']
process_list = ['Chr','Start','End','Ref','Alt',\
               'Func.smallrefGene','Gene.smallrefGene','RNA','EXON','NCchange',\
                'AAchange','ExonicFunc.smallrefGene','cytoBand',\
               'CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG',\
               'avsnp150','SIFT_score','SIFT_pred','AO','DP','VAF']              
               
def anno_filter():
    try:
        temp_file = annover_txt.replace('anno','filter')
        with open(annover_txt,'r')as f1,open(temp_file,'w')as f2:
            firstline = f1.readline().strip("\n")
            # print([firstline])  # 可见 ['Chr\tStart\tEnd\tRef\tAlt\tFunc.refGene\tGene.refGene\tGeneDetail.refGene\tExonicFunc.refGene\t... 由 \t 分割。
            # 用一个字典来完成字段名称存储。
            filed_dict = {}
            fileds = firstline.split("\t")
            print(fileds)
            f2.write(firstline+"\n")
            for lines_str in f1: # 从第二行开始读。
                lines = lines_str.strip("\n").split("\t")
                for i in range(len(lines)):
                    filed_dict[fileds[i]] = lines[i]
                # if filed_dict['Gene.smallrefGene'] in useful_17_gene:       # 这是不再过滤17基因的模式。
                if filed_dict['AAChange.smallrefGene'] != ".":
                    if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
                        f2.write(lines_str)
    except:
        # print("anno_filter 过滤脚本出现异常。")
        sys.stderr.write("anno_filter 过滤脚本出现异常。\n")
        exit(1)
        
def process_anno_filter():
    temp_file = annover_txt.replace('anno','filter')
    df_anno = pd.read_csv(temp_file, sep='\t')
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
    process_anno_filter_txt = temp_file.replace('filter','process')
    df_result.to_csv( process_anno_filter_txt,sep='\t', index=False)

if __name__=='__main__':
    anno_filter()
    process_anno_filter()
