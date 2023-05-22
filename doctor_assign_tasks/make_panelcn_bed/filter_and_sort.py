#coding=utf8

import pandas as pd
import re

def Remove_reads_less_than_20():
    df_result = pd.read_csv('~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log', sep='\t', header=None, \
        names=['chr', 'start', 'end','gene','exon', 'reads', 'covered_bp_nums', 'area_length', 'coverage_value'])
    df_result = df_result[df_result['reads'].astype(int)>=20]
    df_result.to_csv('~/doctor_assign_tasks/make_panelcn_bed/filter_add_gene_exon_depth.log', sep='\t', index=False, header=None)

def sort_bed():
    df_result = pd.read_csv('~/doctor_assign_tasks/make_panelcn_bed/filter_add_gene_exon_depth.log', sep='\t', header=None, \
        names=['chr', 'start', 'end','gene','exon', 'reads', 'covered_bp_nums', 'area_length', 'coverage_value'])
    # print(df_result)
    df_result1 = df_result[~(df_result.chr.isin(['chrX', 'chrY']))]  # ~是求反集。
    df_result1['chr_num'] = df_result1['chr'].str.extract(r'(\d+)').astype(int)  # 仅仅处理1-22基因，xy后面加上去。
    df_result1 = df_result1.sort_values(by=['chr_num', 'start'])

    if not df_result[df_result['chr'] == 'chrX'].empty:  # 处理xy。
        df_resultX = df_result[df_result.chr.isin(['chrX'])]
        df_resultX = df_resultX.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1, df_resultX])
    if not df_result[df_result['chr'] == 'chrY'].empty:
        df_resultY = df_result[df_result.chr.isin(['chrY'])]
        df_resultY = df_resultY.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1, df_resultY])
    df_result1 = df_result1.drop(columns=['chr_num'])  # 删除排序工具字段。
    useful_chr_list = ['chr' + str(i) for i in range(1, 23)]
    useful_chr_list.extend(['chrX', 'chrY'])
    df_result1 = df_result1[df_result1.chr.isin(useful_chr_list)]  # 删除1-22 x y 之外的chr。
    df_result1.to_csv('~/doctor_assign_tasks/make_panelcn_bed/sorted_filter_add_gene_exon_depth.log', sep='\t', index=False, header=None)

if __name__=='__main__':
    Remove_reads_less_than_20()
    sort_bed()
