# -*- coding: utf-8 -*-
import pandas as pd
import re, os, sys
import warnings
from typing import TypeVar

warnings.filterwarnings('ignore')

sample = sys.argv[1]  # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
annover_txt = sys.argv[4]

useful_17_gene = ['AKT1', 'ALK', 'BCL2L11', 'BRAF', \
                  'EGFR', 'ERBB2', 'KRAS', 'MAP2K1', \
                  'MET', 'NRAS', 'NTRK1', 'NTRK2', \
                  'NTRK3', 'RET', 'ROS1', 'PTEN', \
                  'PIK3CA']
retain_list = ['Chr', 'Start', 'End', 'Ref', 'Alt', \
               'Func.smallrefGene', 'Gene.smallrefGene', 'AAChange.smallrefGene', 'ExonicFunc.smallrefGene', 'cytoBand', \
               'CLNALLELEID', 'CLNDN', 'CLNDISDB', 'CLNREVSTAT', 'CLNSIG', \
               'avsnp150', 'SIFT_score', 'SIFT_pred', 'Otherinfo11']
process_list = ['Chr', 'Start', 'End', 'Ref', 'Alt', \
                'Func.smallrefGene', 'Gene.smallrefGene', 'RNA', 'EXON', 'NCchange', \
                'AAchange', 'ExonicFunc.smallrefGene', 'cytoBand', \
                'CLNALLELEID', 'CLNDN', 'CLNDISDB', 'CLNREVSTAT', 'CLNSIG', \
                'avsnp150', 'SIFT_score', 'SIFT_pred', 'AO', 'DP', 'VAF']


def anno_filter():
    try:
        temp_file = annover_txt.replace('anno', 'filter')
        # 我们使用了 TypeVar 来定义一个泛型类型 T，它的约束是 str 类型。
        T = TypeVar('T', int, str)

        def Renaming_to_Chinese(english_Name: T) -> str:  # 这样的dict写法其实是为了避免if else 嵌套太多，python又没有case的办法。
            options = {
                'nonsynonymous SNV': '错义突变', 'synonymous SNV': '同义突变',
                'frameshift deletion': '移码缺失', 'nonframeshift deletion': '非移码缺失',
                'frameshift insertion': '移码插入', 'nonframeshift insertion': '非移码插入',
                'stopgain': '终止子获得', 'stoploss': '终止子缺失'
            }
            return options.get(english_Name, f'对应的中文翻译不存在，英文单词为{english_Name}。')

        with open(annover_txt, 'r')as f1, open(temp_file, 'w')as f2:
            firstline = f1.readline().strip("\n")
            # print([firstline])  # 可见 ['Chr\tStart\tEnd\tRef\tAlt\tFunc.refGene\tGene.refGene\tGeneDetail.refGene\tExonicFunc.refGene\t... 由 \t 分割。
            # 用一个字典来完成字段名称存储。
            filed_dict = {}
            fileds = firstline.split("\t")
            print(fileds)
            f2.write(firstline + "\n")
            for lines_str in f1:  # 从第二行开始读。
                lines = lines_str.strip("\n").split("\t")
                for i in range(len(lines)):
                    filed_dict[fileds[i]] = lines[i]
                if filed_dict['Gene.smallrefGene'] in useful_17_gene:  # 这是过滤17基因的模式。
                    # if filed_dict['AAChange.smallrefGene'] != ".":        # 注释掉以后，保留下了非 exonic的 行。
                    if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
                        English_Name = str(filed_dict['ExonicFunc.smallrefGene']) if filed_dict['ExonicFunc.smallrefGene']!='.' else '无'
                        Chinese_Name = Renaming_to_Chinese(English_Name)
                        lines_str = lines_str.replace(English_Name, Chinese_Name)
                        f2.write(lines_str)
    except:
        # print("anno_filter 过滤脚本出现异常。")
        sys.stderr.write("anno_filter 过滤脚本出现异常。\n")
        exit(1)


def process_anno_filter():
    temp_file = annover_txt.replace('anno', 'filter')
    df_anno = pd.read_csv(temp_file, sep='\t')
    if df_anno.shape[1] <= 25:
        print('终止，因为已经处理过了。')
        return
    df_retain = df_anno[retain_list]
    i = 0
    df_retain['AO'], df_retain['DP'], df_retain['VAF'] = None, None, None
    df_retain['RNA'] = \
    df_retain[df_retain['AAChange.smallrefGene'] != '.']['AAChange.smallrefGene'].str.split(':', expand=True)[1]
    df_retain['EXON'] = \
    df_retain[df_retain['AAChange.smallrefGene'] != '.']['AAChange.smallrefGene'].str.split(':', expand=True)[2]
    df_retain['NCchange'] = \
    df_retain[df_retain['AAChange.smallrefGene'] != '.']['AAChange.smallrefGene'].str.split(':', expand=True)[3]
    df_retain['AAchange'] = \
    df_retain[df_retain['AAChange.smallrefGene'] != '.']['AAChange.smallrefGene'].str.split(':', expand=True)[4]
    for element_list in df_retain['Otherinfo11'].str.split(';', expand=False):
        for element in element_list:
            if element.split('=')[0] == 'AO':
                # print(element)
                df_retain['AO'].iloc[i] = max(
                    list(map(int, element.split('=')[1].split(','))))  # 这里其实是有多个值的 AO，我们取了最大值。
            if element.split('=')[0] == 'DP':
                # print(element)
                df_retain['DP'].iloc[i] = element.split('=')[1]
        vaf_list = []
        # for ii in range(len(df_retain['AO'].iloc[i].split(','))):  # 这里其实是有多个值的 AO，我们全取就这样写。
        #     vaf_list.append(
        #         "%.2f%%" % (int(df_retain['AO'].iloc[i].split(',')[ii]) * 100 / int(df_retain['DP'].iloc[i])))
        ii = df_retain['AO'].iloc[i]
        vaf_list.append(
            "%.2f%%" % (ii * 100 / int(df_retain['DP'].iloc[i])))
        df_retain['VAF'].iloc[i] = ','.join(vaf_list)
        i += 1
    # 删除 'Otherinfo11'等字段，用完了就删掉，并调整字段顺序。
    df_result = df_retain[process_list]
    print(df_result)
    process_anno_filter_txt = temp_file.replace('filter', 'process')
    df_result.to_csv(process_anno_filter_txt, sep='\t', index=False)

def isolate_germline_txt():
    process_file = annover_txt.replace('anno', 'process')
    germline_file = annover_txt.replace('anno', 'germline')
    print('看这里： ',process_file)
    print('看这里： ',germline_file)
    df = pd.read_csv(process_file, sep='\t')
    print(df)
    # percentage_float = float(str(df['VAF']).strip('%')) / 100
    # df['VAF'].str.strip('%').astype(float) / 100
    # 这里用到了 pandas的query 方法，做成类似sql的查询写法。
    df_germline = df.query("40 <= VAF.str.strip('%').astype('float') <= 60 or VAF.str.strip('%').astype('float') >= 90")
    df_somatic = df.query("VAF.str.strip('%').astype('float') < 40 or 60 < VAF.str.strip('%').astype('float') <90")

    df_somatic.to_csv(process_file, sep='\t', index=False)
    df_germline.to_csv(germline_file, sep='\t', index=False)

if __name__ == '__main__':
    anno_filter()
    process_anno_filter()
    isolate_germline_txt()
