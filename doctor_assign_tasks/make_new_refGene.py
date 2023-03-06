#coding=utf8
import pandas as pd
import re

def process_LRG():
    lrg_df = pd.read_table('LRG_RefSeqGene', sep='\t')  # 第一行当作 列索引。
    # print(lrg_df)
    # print(len(lrg_df)) # 行。
    with open('LRG_RefSeqGene', 'r')as f0, open('LRG_RefSeqGene_1', 'w')as f1, open('LRG_RefSeqGene_more',
                                                                                    'w')as f2, open(
            'LRG_RefSeqGene_null', 'w')as f3, \
            open('LRG_RefSeqGene_more_without_t1', 'w')as f4:
        fristline = f0.readline()
        f1.write(fristline)
        f2.write(fristline)
        f3.write(fristline)
        f4.write(fristline)
        print([f0.readline()])
    group = lrg_df.groupby('GeneID')
    for key, value in group:
        # print(key)
        # print(value['Category'])
        if 'reference standard' in value['Category'].values:  # Category列中有'reference standard'
            reference_standard_count = value['Category'].value_counts()['reference standard']
            if reference_standard_count == 1:
                # print(value[0:1]['Category'])
                value[value['Category'] == "reference standard"].to_csv('LRG_RefSeqGene_1', sep='\t', index=False,
                                                                        mode='a', header=0)
                # value.to_csv('LRG_RefSeqGene_1', sep='\t', index=False, mode='a', header=0)
            elif reference_standard_count > 1:
                # print([value[0:1]])
                # print(value['p'].iloc[0])
                # # print(key)
                # # print(value)
                # # print(reference_standard_count)
                # print(value[0:1]['Category'])
                value = value[value['Category'] == "reference standard"]
                if 't1' in value['t'].values:
                    # print(value[0:1]['Category'])
                    value[value['t'] == 't1'].to_csv('LRG_RefSeqGene_more', sep='\t', index=False, mode='a', header=0)
                else:
                    # print("出现没有t1的情况。GeneID=%d"%value['GeneID'].iloc[0] )
                    # print(value[0:1]['RNA'])
                    # print(value['RNA'],"is value['RNA']",value['RNA'].iloc[0])
                    if value['GeneID'].iloc[0] != 3222:
                        value[0:1].to_csv('LRG_RefSeqGene_more_without_t1', sep='\t', index=False, mode='a', header=0)
                    else:
                        value[1:2].to_csv('LRG_RefSeqGene_more_without_t1', sep='\t', index=False, mode='a', header=0)
                # value.to_csv('LRG_RefSeqGene_more', sep='\t', index=False,mode='a',header=0)
        else:  # Category列中无'reference standard'
            # print("没有 reference standard")
            # print(value['Category'])
            value[0:1].to_csv('LRG_RefSeqGene_null', sep='\t', index=False, mode='a', header=0)

    df1, df2, df3, df4 = pd.read_csv('LRG_RefSeqGene_1', sep='\t'), pd.read_csv('LRG_RefSeqGene_more', sep='\t') \
        , pd.read_csv('LRG_RefSeqGene_more_without_t1', sep='\t'), pd.read_csv('LRG_RefSeqGene_null', sep='\t')
    unique_RNA_df = pd.concat([df1, df2, df3, df4]).sort_values(by=['GeneID'])

    unique_RNA_df.to_csv('unique_RNA_LRG_RefSeqGene', sep='\t', index=False)

def make_new_refGene():
    unique_RNA_df = pd.read_csv('unique_RNA_LRG_RefSeqGene',sep='\t')
    unique_RNA_df['RNA'] = unique_RNA_df['RNA'].str.split('.').str[0]  # 去掉.后面的版本号。

    refGene_df_19 = pd.read_csv('hg19_refGene.txt', sep='\t',header=None)
    refGene_df_38 = pd.read_csv('hg38_refGene.txt', sep='\t',header=None)

    print(len(unique_RNA_df))
    for index,row in unique_RNA_df.iterrows():
        # print(index,end="\t")
        # print(row['GeneID'],'\t',row['RNA'])   # row['RNA'] 是一个单独的str。
        # print(refGene_df.iloc[:,1:2])
        # print(refGene_df_19[refGene_df_19[1]==row['RNA']])
        refGene_df_19[refGene_df_19[1] == row['RNA']].to_csv('new_unique_hg19_refGene.txt',sep='\t', index=False, mode='a', header=0)
        refGene_df_38[refGene_df_38[1] == row['RNA']].to_csv('new_unique_hg38_refGene.txt', sep='\t', index=False, mode='a', header=0)


if __name__=="__main__":
    process_LRG()
    make_new_refGene()
