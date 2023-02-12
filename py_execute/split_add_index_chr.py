# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample

extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'


file_path = generate_location+"/"+parent_name+"/"+sample
chr_split = file_path+"/"+"chr_split"

os.chdir(file_path)
if not os.path.exists(chr_split):
    os.makedirs(chr_split)
os.system(f"cp {file_path}/{sample}.{dedup_or_markdup}.bam chr_split/")
os.chdir(chr_split)
cmd = f"bamtools split -in {chr_split}/{sample}.{dedup_or_markdup}.bam  -reference"
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(1)
cmd = f"samtools index -@ 2 {chr_split}/{sample}.{dedup_or_markdup}.REF_chrX.bam {chr_split}/{sample}.{dedup_or_markdup}.REF_chrX.bam.bai"
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(1)
cmd = f"samtools index -@ 2 {chr_split}/{sample}.{dedup_or_markdup}.REF_chrY.bam {chr_split}/{sample}.{dedup_or_markdup}.REF_chrY.bam.bai"
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(1)
for i in range(1,23):
    cmd = f"samtools index -@ 2 {chr_split}/{sample}.{dedup_or_markdup}.REF_chr{i}.bam {chr_split}/{sample}.{dedup_or_markdup}.REF_chr{i}.bam.bai"
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(1)
# ########################################
# file_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# cd $file_path
# if [ ! -d "$file_path/chr_split"  ]; then
#         mkdir -p $file_path/chr_split
# fi
# 
# cp ${sample}.dedup.bam chr_split/
# cd chr_split
# 
# inputpath=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/chr_split
# 
# bamtools split -in $inputpath/${sample}.dedup.bam  -reference
# 
# samtools index -@ 2 $inputpath/${sample}.dedup.REF_chrX.bam $inputpath/${sample}.dedup.REF_chrX.bam.bai
# samtools index -@ 2 $inputpath/${sample}.dedup.REF_chrY.bam $inputpath/${sample}.dedup.REF_chrY.bam.bai
# for ((i=1;i<=22;i++))
# do
#     samtools index -@ 2 $inputpath/${sample}.dedup.REF_chr$i.bam $inputpath/${sample}.dedup.REF_chr$i.bam.bai
# done
