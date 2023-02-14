# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg19_fasta = config['reference_document']['fasta']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]


extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'
    

split_vcf_path = generate_location+"/"+sample_path+"/"+"split_vcf"
output_dir = generate_location+"/"+sample_path

def shell_func(i,sample=sample):
    cmd1 = f"bgzip -c {sample}.{dedup_or_markdup}.REF_chr{i}.vcf > {sample}.{dedup_or_markdup}.REF_chr{i}.vcf.gz"
    cmd2 = f"bcftools index -t {sample}.{dedup_or_markdup}.REF_chr{i}.vcf.gz"
    # cmd1,cmd2 = cmd1.format(sample=sample,i=i),cmd2.format(sample=sample,i=i)
    p = subprocess.Popen(cmd1,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(3)
    p = subprocess.Popen(cmd2,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(3)
    
if __name__=="__main__":
    os.chdir(split_vcf_path)
    test_list = [i for i in range(1,23)]
    test_list.extend(["X","Y"])
    pool = Pool(processes=12)
    for i in test_list:
        pool.apply_async(shell_func,(i,))
    pool.close()
    pool.join()

    cmd = f"bcftools merge -m snps -f PASS,. --force-samples \
    {sample}.{dedup_or_markdup}.REF_chr1.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr2.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr3.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr4.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr5.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr6.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr7.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr8.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr9.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr10.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr11.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr12.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr13.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr14.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr15.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr16.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr17.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr18.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr19.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr20.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr21.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chr22.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chrX.vcf.gz \
    {sample}.{dedup_or_markdup}.REF_chrY.vcf.gz \
    > {sample}.merge.vcf"
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(3)
    cmd = f"cp {split_vcf_path}/{sample}.merge.vcf {output_dir}/"
    p = subprocess.Popen(cmd.format(split_vcf_path=split_vcf_path,sample=sample,output_dir=output_dir),shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(3)
    # filter 
    # os.chdir(output_dir)
    # cmd = "bcftools filter -e 'FORMAT/DP>99' {output_dir}/{sample}.merge.vcf > {output_dir}/{sample}.filter_merge.vcf" 
    # returncode = subprocess.call(cmd.format(output_dir=output_dir,sample=sample),shell=True)
    # if returncode != 0:
    #     exit(3)
    
# ######################################
# split_vcf_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/split_vcf
# output_dir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# cd $split_vcf_path 
# bgzip -c ${sample}.dedup.REF_chrX.vcf > ${sample}.dedup.REF_chrX.vcf.gz
# bcftools index -t ${sample}.dedup.REF_chrX.vcf.gz
# bgzip -c ${sample}.dedup.REF_chrY.vcf > ${sample}.dedup.REF_chrY.vcf.gz
# bcftools index -t ${sample}.dedup.REF_chrY.vcf.gz
# for ((i=1;i<=22;i++))
# do
#     bgzip -c ${sample}.dedup.REF_chr$i.vcf > ${sample}.dedup.REF_chr$i.vcf.gz
#     bcftools index -t ${sample}.dedup.REF_chr$i.vcf.gz
# done
# 
# 
# bcftools merge -m snps -f PASS,. --force-samples \
# ${sample}.dedup.REF_chrX.vcf.gz \
# ${sample}.dedup.REF_chrY.vcf.gz \
# ${sample}.dedup.REF_chr1.vcf.gz \
# ${sample}.dedup.REF_chr2.vcf.gz \
# ${sample}.dedup.REF_chr3.vcf.gz \
# ${sample}.dedup.REF_chr4.vcf.gz \
# ${sample}.dedup.REF_chr5.vcf.gz \
# ${sample}.dedup.REF_chr6.vcf.gz \
# ${sample}.dedup.REF_chr7.vcf.gz \
# ${sample}.dedup.REF_chr8.vcf.gz \
# ${sample}.dedup.REF_chr9.vcf.gz \
# ${sample}.dedup.REF_chr10.vcf.gz \
# ${sample}.dedup.REF_chr11.vcf.gz \
# ${sample}.dedup.REF_chr12.vcf.gz \
# ${sample}.dedup.REF_chr13.vcf.gz \
# ${sample}.dedup.REF_chr14.vcf.gz \
# ${sample}.dedup.REF_chr15.vcf.gz \
# ${sample}.dedup.REF_chr16.vcf.gz \
# ${sample}.dedup.REF_chr17.vcf.gz \
# ${sample}.dedup.REF_chr18.vcf.gz \
# ${sample}.dedup.REF_chr19.vcf.gz \
# ${sample}.dedup.REF_chr20.vcf.gz \
# ${sample}.dedup.REF_chr21.vcf.gz \
# ${sample}.dedup.REF_chr22.vcf.gz \
# > ${sample}.merge.vcf
# 
# cp $split_vcf_path/${sample}.merge.vcf $output_dir/

# merge_vcf_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
# cd $merge_vcf_path
# bcftools filter -e "FORMAT/DP>99" $merge_vcf_path/${sample}.merge.vcf > $merge_vcf_path/${sample}.filter_merge.vcf 
