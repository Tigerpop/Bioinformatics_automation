#coding=utf8
import configparser,subprocess,re,os,sys
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

input_file = generate_location+"/"+sample_path+"/"+sample+".anno.{hg_19_or_38}_multianno.txt".format(hg_19_or_38=hg_19_or_38)
out_file = generate_location+"/"+sample_path+"/"+sample+".filter.{hg_19_or_38}_multianno.txt".format(hg_19_or_38=hg_19_or_38)

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
            # if filed_dict['Gene.smallrefGene'] in useful_17_gene:       # 这是不再过滤17基因的模式。
            if filed_dict['AAChange.smallrefGene'] != ".":
                if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
                    f2.write(lines_str)
            # if filed_dict['Gene.smallrefGene'] in useful_17_gene:       # 这是过滤17基因的模式。
            #     if filed_dict['AAChange.smallrefGene'] != ".":
            #         if filed_dict['ExonicFunc.smallrefGene'] != "synonymous SNV":
            #             f2.write(lines_str)
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
    
    
