# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']    # /working_tmp  
human_genome_index = config['reference_document']['human_genome_index']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]


tmp_dir = generate_location + '/'+sample_path
input = generate_location+"/"+sample_path+"/"+sample+".bwa_mem.bam"
inputbai = generate_location+"/"+sample_path+"/"+sample+".bwa_mem.bam.bai"
input1 = generate_location+"/"+sample_path+"/"+sample+".markdup.bam"
inputbai1 = generate_location+"/"+sample_path+"/"+sample+".markdup.bam.bai"
output = generate_location+"/"+sample_path+"/"+sample+".markdup.bam"

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
