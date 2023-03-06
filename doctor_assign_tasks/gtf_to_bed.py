# coding=utf8
import pandas as pd
import re
useful_17_gene = ['AKT1', 'ALK', 'BCL2L11', 'BRAF', \
                  'EGFR', 'ERBB2', 'KRAS', 'MAP2K1', \
                  'MET', 'NRAS', 'NTRK1', 'NTRK2', \
                  'NTRK3', 'RET', 'ROS1', 'PTEN', \
                  'PIK3CA']

def process():
    df_LRG = pd.read_csv('LRG_RefSeqGene', sep='\t')
    print(df_LRG)
    with open('hg38_gtf','r')as f0,open('hg38_filter_GTF.txt','a+')as f1:
        line = f0.readline().strip("\n")
        # print(line)
        while line:
            elements = line.split("\t")
            RNA = re.findall(r'\"(.+?)\"', elements[-1])[0]               # 正则提取出 NM_001376542 。
            Chr = elements[0]
            start = elements[3]
            end = elements[4]
            is_exon = elements[2]
            direction = elements[6]
            # 利用这个 RNA 到unique_RNA_LRG_RefSeqGene 中提取 基因名。
            df_LRG['RNA'] = df_LRG['RNA'].str.split(".",expand=True)[0]   # 去除 RNA 版本号。
            # print(df_LRG[df_LRG['RNA']==RNA])
            if not df_LRG[df_LRG['RNA']==RNA].empty and is_exon=='exon':  # 注意 empty 和 None 不一样。提取 基因名
                Genename = df_LRG[df_LRG['RNA'] == RNA]['Symbol'].iloc[0]
                # print(Genename)
                bag = []
                bag.extend([Chr,start,end,Genename,RNA,direction,is_exon])
                f1.write("\t".join(bag)+'\n')
            line = f0.readline().strip("\n")

def filter_17gene():
    with open('hg38_filter_GTF_add_exon_num.txt', 'r')as f0, open('hg38_filter_just_save_17_GTF.txt', 'a+')as f1:
        line = f0.readline().strip("\n")
        while line:
            print(line)
            Genename = line.split("\t")[3]
            if Genename in useful_17_gene:
                f1.write(line+'\n')
            line = f0.readline().strip("\n")

def make_3_and_4_field():
    with open('hg38_filter_just_save_17_GTF.txt', 'r')as f0, open('hg38_three_field.bed', 'a+')as f1 ,\
            open('hg38_four_field.bed','a+')as f2:
        line = f0.readline().strip("\n")
        while line:
            print(line)
            elements = line.split("\t")
            chr = elements[0]
            start = elements[1]
            end = elements[2]
            Genename = elements[3]
            is_exon = elements[6]
            bag = []
            bag.extend([chr,start,end])
            f1.write("\t".join(bag)+'\n')
            bag.append(Genename)   # +'_'+is_exon)
            f2.write("\t".join(bag)+'\n')
            line = f0.readline().strip("\n")

def add_exon_num():
    # 没有column行我们读的时候定义一下。
    df = pd.read_csv('hg38_filter_GTF.txt', sep='\t',header=None,\
                        names=['chr','start','end','genename','rna','direction','is_exon'])
    df_grouped = df.groupby('direction')
    df_positive = df_grouped.get_group('+')
    df_negative = df_grouped.get_group('-')
    # 这个写法类似鱼 sql 中的 row_numbel() over() 窗口函数 排序标记的作用。
    # 注意是先选定排序字段，再按照分组搞。这样比较方便。
    # 注意 此时的 groupby 不能直接跟 字段名，而要写series形式。'https://blog.csdn.net/weixin_44166997/article/details/105004873?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-105004873-blog-90760692.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-105004873-blog-90760692.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=1'
    df_positive['group_sort'] = df_positive['start'].groupby(df_positive['genename']).rank(ascending=1,method='first').astype('int64').astype('str')    # ascending 0是降序 1是生序。
    df_negative['group_sort'] = df_negative['start'].groupby(df_negative['genename']).rank(ascending=0,method='first').astype('int64').astype('str')
    df_positive['is_exon'] = df_positive['is_exon']+"_"+df_positive['group_sort']
    df_positive = df_positive.drop(columns=['group_sort'])
    df_negative['is_exon'] = df_negative['is_exon']+"_"+df_negative['group_sort']
    df_negative = df_negative.drop(columns=['group_sort'])   
    # print(df_positive.info())
    print(df_positive)
    print(df_negative)
    # 'https://cloud.tencent.com/developer/ask/sof/96816'
    df_result = pd.concat([df_positive,df_negative])
    df_result1 = df_result[~(df_result.chr.isin(['chrX','chrY']))]              #  ~是求反集。
    df_result1['chr_num'] = df_result1['chr'].str.extract(r'(\d+)').astype(int) # 仅仅处理1-22基因，xy后面加上去。
    df_result1 = df_result1.sort_values(by=['chr_num','start'])

    if not df_result[df_result['chr']=='chrX'].empty:                           # 处理xy。
        df_resultX = df_result[df_result.chr.isin(['chrX'])]
        df_resultX = df_resultX.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1,df_resultX])
    if not df_result[df_result['chr']=='chrY'].empty:
        df_resultY = df_result[df_result.chr.isin(['chrY'])]
        df_resultY = df_resultY.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1,df_resultY])
    df_result1 = df_result1.drop(columns=['chr_num'])                           # 删除排序工具字段。
    useful_chr_list = ['chr'+str(i) for i in range(1,23)]
    useful_chr_list.extend(['chrX','chrY'])
    df_result1 = df_result1[df_result1.chr.isin(useful_chr_list)]               # 删除1-22 x y 之外的chr。
    df_result1.to_csv('hg38_filter_GTF_add_exon_num.txt',sep='\t',index=False,header=0)
    
def make_all_4_field():
    with open('hg38_filter_GTF_add_exon_num.txt', 'r')as f0, open('hg38_all_four_field.bed', 'a+')as f1:
        line = f0.readline().strip("\n")
        while line:
            print(line)
            elements = line.split("\t")
            chr = elements[0]
            start = elements[1]
            end = elements[2]
            Genename = elements[3]
            bag = []
            bag.extend([chr,start,end,Genename])
            f1.write("\t".join(bag)+'\n')
            line = f0.readline().strip("\n")
    
if __name__ == "__main__" :
    process()
    add_exon_num()
    filter_17gene()
    make_3_and_4_field()
    make_all_4_field()

