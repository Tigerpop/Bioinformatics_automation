#!/bin/bash
# sample=2022WSSW005215-T

merge_vcf_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
cd $merge_vcf_path
bcftools filter -e "FORMAT/DP>99" $merge_vcf_path/${sample}.merge.vcf > $merge_vcf_path/${sample}.filter_merge.vcf 
