# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
human_genome_index = config['reference_document']['human_genome_index']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    extracted1,extracted2 = "_extracted.1.fq.gz","_extracted.2.fq.gz"
elif extract_mode == 'fastp_mode':
    extracted1,extracted2 = "_1.extract.fq.gz","_2.extract.fq.gz"

extract_fq_1 = generate_location+"/"+sample_path+"/"+sample+extracted1
extract_fq_2 = generate_location+"/"+sample_path+"/"+sample+extracted2
unsort_bam = generate_location+"/"+sample_path+"/"+sample+".unsort.bam"
output = generate_location+"/"+sample_path+"/"+sample+".bwa_mem.bam"


cmd = f"bwa mem -t 16 \
  -Y \
  {human_genome_index}  \
  {extract_fq_1}  \
  {extract_fq_2}  \
  -o {unsort_bam}"
p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
p.communicate() # 一定要有这个等待第一个紫禁城完结，再进行下一个紫禁城。
if p.returncode != 0:
    exit(3)
cmd2 = "samtools sort -@ 16 -o {output} {unsort_bam}".format(output=output,unsort_bam=unsort_bam)
p2 = subprocess.Popen(cmd2,shell=True)
p2.communicate()
if p2.returncode != 0:
    exit(3)

# ###########################################
# export LC_ALL=C
# human_genome_index=/home/chenyushao/wes_cancer/data/hg19/gatk_hg19
# extract_fq_1=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.1.fq.gz
# extract_fq_2=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.2.fq.gz
# output=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.bwa_mem.bam
# 
# bwa mem -t 16 \
#   $human_genome_index  \
#   $extract_fq_1  \
#   $extract_fq_2  \
#   -o /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.unsort.bam
# 
# samtools sort -@ 16 -o $output /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.unsort.bam
