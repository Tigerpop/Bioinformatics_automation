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

tumor_bam = generate_location+"/"+parent_name+"/"+sample +"/"+sample+".{dedup_or_markdup}.bam"
process_dir = generate_location+"/"+parent_name+"/"+sample 
fasta_dir = config['reference_document']['fasta_dir']+"/"
cmd1 = config['cnvnator']['parameters_pool1']
cmd2 = config['cnvnator']['parameters_pool2']
cmd3 = config['cnvnator']['parameters_pool3']
cmd4 = config['cnvnator']['parameters_pool4']
cmd5 = config['cnvnator']['parameters_pool5']
cmd6 = config['cnvnator']['parameters_pool6']

cmd1 = cmd1 + " " + tumor_bam + " -chrom $(seq 1 22) X Y  "
cmd2 = cmd2 + fasta_dir
# os.chdir("/home/chenyushao/py_generate/2022WSSW005712/2022WSSW005712-T/E100065646_L01_2022WSSW005712-T")
os.chdir(process_dir)

for i in range(1,6):  # 6 么有使用。
    cmd = "cmd"+str(i)
    p = subprocess.Popen(locals()[cmd],shell=True)
    p.communicate()
    if p.returncode != 0:
        exit("cnvnator false")
    
# cd /home/chenyushao/draft
# tumor_dir=/home/chenyushao/sh_temp生成文件汇总/2021WSSW000188-T/E150000432_L01_2021WSSW000188-T/
# tumor_bam=$tumor_dir/E150000432_L01_2021WSSW000188-T.dedup.bam
# fasta_dir=/home/chenyushao/wes_cancer/data/hg19   # /ucsc.hg19.fasta
# 
# cnvnator -root file.root -genome hg19 -tree $tumor_bam    
# 
# cnvnator -root file.root -genome hg19 -his 1000 -d $fasta_dir 
# 
# cnvnator -root file.root -genome hg19 -stat 1000 
# 
# cnvnator -root file.root -genome hg19 -partition 1000 
# 
# cnvnator -root file.root -genome hg19 -call 1000  > cnv.call.txt
# 
# 
# # 还能用自带的工具转成 vcf格式:cnvnator2VCF.pl cnv.call.txt >cnv.vcf
