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


fastq_dir = sample_parent+'/'+sample
tmp_dir = generate_location + '/'+parent_name+'/'+sample
fa_gz_1 = fastq_dir+'/'+sample+'_1.fq.gz'
fa_gz_2 = fastq_dir+'/'+sample+'_2.fq.gz'
out_extract_1 = tmp_dir+'/'+sample+'_1.extract.fq.gz'
out_extract_2 = tmp_dir+'/'+sample+'_2.extract.fq.gz'
# print(fa_gz_1,'\n',fa_gz_2,'\n',out_extract_1,'\n',out_extract_2)

os.system("mkdir -p {gl}/{pn}/{s}".format(gl=generate_location,pn=parent_name,s=sample))
os.chdir(tmp_dir)


cmd = f'fastp -i {fa_gz_1} \
      -I {fa_gz_2} \
      -o {out_extract_1} \
      -O {out_extract_2} \
      -w 8 \
      -l 30  > fastp.log 2>&1' 
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit('fastp is false !!!')
