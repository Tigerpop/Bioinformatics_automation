#coding=utf8
import configparser,subprocess,re,os
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


input_file = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".anno.{hg_19_or_38}_multianno.txt".format(hg_19_or_38=hg_19_or_38)
out_file = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".filter.{hg_19_or_38}_multianno.txt".format(hg_19_or_38=hg_19_or_38)

useful_17_gene = ['AKT1','ALK','BCL2L11','BRAF',\
               'EGFR','ERBB2','KRAS','MAP2K1',\
               'MET','NRAS','NTRK1','NTRK2',\
               'NTRK3','RET','ROS1','PTEN',\
               'PIK3CA']
try:
    with open(input_file,'r')as f1,open(out_file,'w')as f2:
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
            if filed_dict['Gene.smallrefGene'] in useful_17_gene:
                if filed_dict['AAChange.smallrefGene'] != ".":
                    if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
                        f2.write(lines_str)
except:
    print("anno_filter 过滤脚本出现异常。")
    exit(5) # 装配的第五个脚本。

# with open(input_file,'r')as f1,open(out_file,'w')as f2:
#     firstline = f1.readline().strip("\n")
#     # print([firstline])  # 可见 ['Chr\tStart\tEnd\tRef\tAlt\tFunc.refGene\tGene.refGene\tGeneDetail.refGene\tExonicFunc.refGene\t... 由 \t 分割。
#     # 用一个字典来完成字段名称存储。
#     filed_dict = {}
#     fileds = firstline.split("\t")
#     print(fileds)
#     f2.write(firstline+"\n")
#     for lines_str in f1: # 从第二行开始读。
#         lines = lines_str.strip("\n").split("\t")
#         for i in range(len(lines)):
#             filed_dict[fileds[i]] = lines[i]
#         if filed_dict['Gene.smallrefGene'] in useful_17_gene:
#             if filed_dict['AAChange.smallrefGene'] != ".":
#                 if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
#                     f2.write(lines_str)
    
    
