# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

##################################
# # 以下为全流程后的注释部分。
# filter_merge_vcf = generate_location+"/"+sample_path+"/"+sample+".merge.vcf"
filter_merge_vcf = generate_location+"/"+sample_path+"/"+sample+".pollpass.vcf"
out = generate_location+"/"+sample_path+"/"+sample+".anno"
# [annovar]
annovar_path = config['annovar']['annovar_path']
tool = config['annovar']['tool']
parameters_pool = config['annovar']['parameters_pool']

# print(filter_merge_vcf)
# print(out)
# print(parameters_pool)

cmd = "{annovar_path}/{tool} \
       	{filter_merge_vcf}  \
      	-out {out} \
      	{parameters_pool}"
cmd=cmd.format(annovar_path=annovar_path,tool=tool,filter_merge_vcf=filter_merge_vcf,out=out,parameters_pool=parameters_pool)
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(4)
    
    
    
    
    
    
# 以上为全流程注释部分。
##################################


# # 以下为不切分染色体call突变后直接注释。
# file_vcf = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".vcf"
# out = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".anno"
# annovar_path = config['annovar']['annovar_path']
# tool = config['annovar']['tool']
# parameters_pool = config['annovar']['parameters_pool']
# cmd = "{annovar_path}/{tool} \
#        	{file_vcf}  \
#       	-out {out} \
#       	{parameters_pool}"
# cmd=cmd.format(annovar_path=annovar_path,tool=tool,file_vcf=file_vcf,out=out,parameters_pool=parameters_pool)
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()
# if p.returncode != 0:
#     exit(4)





# ################################3
# os.chdir("/home/chenyushao/py_execute")
# cmd1 = "source /home/chenyushao/py_execute/activate_env_fq_umi.sh "
# cmd3 = "conda info --envs"
# 
# p = subprocess.Popen(cmd1,shell=True)
# p.communicate()


# ################################
# annovar_path=/opt/annovar
# filter_merge_vcf_dir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# 
# $annovar_path/table_annovar.pl \
#        	$filter_merge_vcf_dir/${sample}.filter_merge.vcf  \
#        	$annovar_path/humandb/ \
# 	-buildver hg19 \
# 	-out $filter_merge_vcf_dir/${sample}.anno \
# 	-remove \
# 	-protocol refGene,cytoBand,clinvar_20220320 \
# 	-operation g,r,f \
# 	-nastring . \
# 	-vcfinput \
# 	-polish
