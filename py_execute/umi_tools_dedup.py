# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


input = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".bwa_mem.bam"
inputbai = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".bwa_mem.bam.bai"
input1 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".dedup.bam"
inputbai1 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".dedup.bam.bai"
output = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".dedup.bam"

cmd = "samtools index -@ 16 \
	{input} \
	{inputbai} ".format(input=input,inputbai=inputbai)
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(4)
cmd ="umi_tools dedup  \
	--output-stats=deduplicated  \
	--stdin={input}  \
	--stdout={output}".format(input=input,output=output)
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(4)
    
cmd = f"samtools index -@ 16 \
	{input1} \
	{inputbai1} "
p = subprocess.Popen(cmd,shell=True)
p.communicate()
print("okokokok")

# ####################################
# input=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.bwa_mem.bam
# inputdir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# output=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.dedup.bam
# 
# samtools index -@ 16 \
# 	$input \
# 	$inputdir/${sample}.bwa_mem.bam.bai
# # 
# umi_tools dedup  \
# 	--output-stats=deduplicated  \
# 	--stdin=$input  \
# 	--stdout=$output
# 
# cp $inputdir/${sample}.bwa_mem.bam $inputdir/${sample}.undedup.bam
# cp $inputdir/${sample}.bwa_mem.bam.bai $inputdir/${sample}.undedup.bam.bai
