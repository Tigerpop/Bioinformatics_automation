# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_location = config['generate']['location']
fasta = config['reference_document']['fasta']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
parent_name = sample_parent.split('fastq_data/')[1]
# sample = "E100063570_L01_2021WSSW001567-T" # 之后总的流程汇总改就改这里。
from samples import sample


extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'
    

# 以下为切分染色体call突变的部分
file_path = generate_location+"/"+parent_name+"/"+sample
bam_path = file_path + "/" + "chr_split"
output_path = file_path + "/" + "split_vcf"
os.chdir(file_path)
if not os.path.exists("split_vcf"):
    os.makedirs("split_vcf")
os.chdir("chr_split")

# --min-coverage 20 \
# --min-alternate-count=5 or 2
# -t /home/chenyushao/py_generate/rs1695.bed
def shell_func(i,fasta=fasta,bam_path=bam_path,sample=sample,output_path=output_path):
    cmd = f"freebayes -f {fasta} --min-alternate-count=5 \
    --min-alternate-fraction=0.01  \
    --min-coverage 20 \
    {bam_path}/{sample}.{dedup_or_markdup}.REF_chr{i}.bam > {output_path}/{sample}.{dedup_or_markdup}.REF_chr{i}.vcf "
    # cmd = cmd.format(fasta=fasta,bam_path=bam_path,sample=sample,output_path=output_path,i=i)
    # subprocess.call(cmd,shell=True)
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(2)

if __name__=="__main__":
    test_list = [i for i in range(1,23)]
    test_list.extend(["X","Y"])
    pool = Pool(processes=12)
    # result = []
    for i in test_list:
        # result.append(pool.apply_async(shell_func,(i,)) )
        pool.apply_async(shell_func,(i,))
    pool.close()
    pool.join()
    # for res in result:
    #     print(res.get())
# # 以上为切分染色体call突变的部分


# # 以下为跳过了dedup和切染色体的步骤，直接对bwa_mem.bam文件call突变的代码。
# file_path = generate_location+"/"+parent_name+"/"+sample
# cmd = "samtools index -@ 8 {file_path}/{sample}.dedup.bam {file_path}/{sample}.dedup.bam.bai".format(file_path=file_path,sample=sample)
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()
# if p.returncode != 0:
#     exit(1)
# def shell_func(hg38_fasta=hg38_fasta,sample=sample,file_path=file_path):
#     cmd = "freebayes -f {hg38_fasta} --min-alternate-count=5 \
#     --min-alternate-fraction=0.01  \
#     --min-coverage 20 \
#     {file_path}/{sample}.dedup.bam > {file_path}/{sample}.vcf "
#     cmd = cmd.format(hg38_fasta=hg38_fasta,sample=sample,file_path=file_path)
#     # subprocess.call(cmd,shell=True)
#     p = subprocess.Popen(cmd,shell=True)
#     p.communicate()
#     if p.returncode != 0:
#         exit(2)
# shell_func()
# # 以上为跳过了dedup和切染色体的步骤，直接对bwa_mem.bam文件call突变的代码。






# print("x")
# cmd = "freebayes -f {fasta} --min-alternate-count=2 \
#   --min-alternate-fraction=0.01  \
#   {bam_path}/{sample}.dedup.REF_chrX.bam > {output_path}/{sample}.dedup.REF_chrX.vcf "


# #############################################
# cd /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# mkdir split_vcf
# cd chr_split
# bam_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/chr_split
# output_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/split_vcf
# fasta=/home/chenyushao/wes_cancer/data/hg19/ucsc.hg19.fasta
# 
# echo "x"
# freebayes -f $fasta --min-alternate-count=2 \
#   --min-alternate-fraction=0.01  \
#   $bam_path/${sample}.dedup.REF_chrX.bam > $output_path/${sample}.dedup.REF_chrX.vcf &
# echo "y"
# freebayes -f $fasta --min-alternate-count=2 \
#   --min-alternate-fraction=0.01 \
#   $bam_path/${sample}.dedup.REF_chrY.bam > $output_path/${sample}.dedup.REF_chrY.vcf &
# 
# seq 1 22 | xargs -n"$((22/22))" |
# { while read line
#   do {
#     for i in $line
#     do
#     echo $i
#     freebayes -f $fasta --min-alternate-count=2 \
#     --min-alternate-fraction=0.01 \
#     $bam_path/${sample}.dedup.REF_chr$i.bam > $output_path/${sample}.dedup.REF_chr$i.vcf  
#     done
#   } &
#     done
#   wait
# }
