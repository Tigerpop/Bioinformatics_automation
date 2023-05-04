# -*- coding: utf-8 -*-
import subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')


sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
bed_key = sys.argv[4]
ref_fasta = sys.argv[5]

def build_bam_file(): # 直接根据 panel 固定 10个 文件，放在refhub 中，因为现在是人工固定好了，所以这一步直接跳过，以后可以用某种算法加以改进。
    pass 
  
def run_DeCoN():
    tmp_dir = f"{generate_location}/{sample_path}/"+"decon_generate"
    decon_bed_0 = f'/refhub/hg19/target/{bed_key}/Target_Regions.bed'
    decon_bed_1 = f'/refhub/hg19/target/{bed_key}/customNumbering.txt'
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    cmd_0 = f"Rscript /opt/DECoN/ReadInBams.R \
            --bams /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/{bed_key}_bam_file.txt \
            --bed {decon_bed_0} \
            --fasta {ref_fasta} \
            --out {tmp_dir}/DECoNtest > ReadInBams.log 2>&1"
    cmd_1 = f"Rscript /opt/DECoN/IdentifyFailures.R  \
            --RData DECoNtest.RData   \
            --exons {decon_bed_1} \
            --mincorr .98 \
            --mincov 100 \
            --out DECoNtest > IdentifyFailures.log 2>&1"
    cmd_2 = f"Rscript /opt/DECoN/makeCNVcalls.R \
            --RData DECoNtest.RData \
            --exons {decon_bed_1} \
            --out DECoNtestCalls > makeCNVcalls.log 2>&1"
    for i in range(3):
        p = subprocess.Popen(locals()['cmd_'+f"{i}"],shell=True)
        p.communicate()
  
if __name__=='__main__':
    build_bam_file()
    run_DeCoN()
    # cnv 的人工处理规则是：Read_ratio > 2 也就是 cnv_number >4 ,
    # 同时，只报 duplicate 内容，
    # cnv_number 四舍五入取整数部分 作为 word 报告中的丰度值，
    # 这个BC17_word.py 中需要 小幅度改动一下。
