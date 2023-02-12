# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'


os.chdir(generate_location+"/"+parent_name+"/"+sample)
if not os.path.exists("msisensor_generate"):
    os.mkdir("msisensor_generate")
# os.chdir(generate_location+"/"+parent_name+"/"+sample+"/"+"msisensor_generate")

msisensor_tool = config['msisensor']['tools']
msisensor_pool = config['msisensor']['msisensor_pool']
input_bam = generate_location+"/"+parent_name+"/"+sample +"/"+sample+f".{dedup_or_markdup}.bam"
out_msi = generate_location+"/"+parent_name+"/"+sample+"/"+"msisensor_generate"+"/"+sample+"msi"

cmd1 = f"samtools index -@ 8 {sample}.{dedup_or_markdup}.bam {sample}.{dedup_or_markdup}.bam.bai"
cmd2 = f"{msisensor_tool} \
        {msisensor_pool} \
        -t {input_bam} \
        -o {out_msi}"
for i in range(1,3):
    cmd = "cmd"+str(i)
    p = subprocess.Popen(locals()[cmd],shell=True)
    p.communicate()
    if p.returncode != 0:
        exit('msisensor is false!')



# ########################################################
# #!/bin/bash
# msisensor_dir=/opt/msisensor-ct-master
# bam_dir=/home/chenyushao/sh_temp生成文件汇总
# cd /home/chenyushao/draft
# mkdir msisensor_test
# output_dir=/home/chenyushao/draft/msisensor_test
# 
# samtools index -@ 2 $bam_dir/dedup.bam $bam_dir/dedup.bam.bai
# $msisensor_dir/msisensor-ct msi \
# 	-D \
# 	-M $msisensor_dir/models_hg19_GRCh37 \
# 	-t $bam_dir/dedup.bam \
# 	-o $output_dir/msi
