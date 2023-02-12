# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']    # /working_tmp  
human_genome_index = config['reference_document']['human_genome_index']
parent_name = sample_parent.split('fastq_data/')[1]   # 
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


tmp_dir = generate_location + '/'+parent_name+'/'+sample
input = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".bwa_mem.bam"
inputbai = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".bwa_mem.bam.bai"
input1 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".markdup.bam"
inputbai1 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".markdup.bam.bai"
output = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".markdup.bam"

os.chdir(tmp_dir)

cmd = "samtools index -@ 16 \
	{input} \
	{inputbai} ".format(input=input,inputbai=inputbai)
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(4)

cmd = f'picard MarkDuplicates \
I={input} \
O={output} \
M=sample_name.markdup_metrics.txt '
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit('picard_markdup is false !!!')
    
cmd = f"samtools index -@ 16 \
	{input1} \
	{inputbai1} "
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(4)
