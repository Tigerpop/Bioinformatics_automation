# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

input = generate_location+"/"+sample_path+"/"+sample+".bwa_mem.bam"
inputbai = generate_location+"/"+sample_path+"/"+sample+".bwa_mem.bam.bai"
input1 = generate_location+"/"+sample_path+"/"+sample+".dedup.bam"
inputbai1 = generate_location+"/"+sample_path+"/"+sample+".dedup.bam.bai"
output = generate_location+"/"+sample_path+"/"+sample+".dedup.bam"

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
