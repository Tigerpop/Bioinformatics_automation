#!/bin/bash
# sample=2022WSSW005215-T

split_vcf_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/split_vcf
output_dir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
cd $split_vcf_path 
bgzip -c ${sample}.dedup.REF_chrX.vcf > ${sample}.dedup.REF_chrX.vcf.gz
bcftools index -t ${sample}.dedup.REF_chrX.vcf.gz
bgzip -c ${sample}.dedup.REF_chrY.vcf > ${sample}.dedup.REF_chrY.vcf.gz
bcftools index -t ${sample}.dedup.REF_chrY.vcf.gz
for ((i=1;i<=22;i++))
do
    bgzip -c ${sample}.dedup.REF_chr$i.vcf > ${sample}.dedup.REF_chr$i.vcf.gz
    bcftools index -t ${sample}.dedup.REF_chr$i.vcf.gz
done


bcftools merge -m snps -f PASS,. --force-samples \
${sample}.dedup.REF_chrX.vcf.gz \
${sample}.dedup.REF_chrY.vcf.gz \
${sample}.dedup.REF_chr1.vcf.gz \
${sample}.dedup.REF_chr2.vcf.gz \
${sample}.dedup.REF_chr3.vcf.gz \
${sample}.dedup.REF_chr4.vcf.gz \
${sample}.dedup.REF_chr5.vcf.gz \
${sample}.dedup.REF_chr6.vcf.gz \
${sample}.dedup.REF_chr7.vcf.gz \
${sample}.dedup.REF_chr8.vcf.gz \
${sample}.dedup.REF_chr9.vcf.gz \
${sample}.dedup.REF_chr10.vcf.gz \
${sample}.dedup.REF_chr11.vcf.gz \
${sample}.dedup.REF_chr12.vcf.gz \
${sample}.dedup.REF_chr13.vcf.gz \
${sample}.dedup.REF_chr14.vcf.gz \
${sample}.dedup.REF_chr15.vcf.gz \
${sample}.dedup.REF_chr16.vcf.gz \
${sample}.dedup.REF_chr17.vcf.gz \
${sample}.dedup.REF_chr18.vcf.gz \
${sample}.dedup.REF_chr19.vcf.gz \
${sample}.dedup.REF_chr20.vcf.gz \
${sample}.dedup.REF_chr21.vcf.gz \
${sample}.dedup.REF_chr22.vcf.gz \
> ${sample}.merge.vcf

cp $split_vcf_path/${sample}.merge.vcf $output_dir/
