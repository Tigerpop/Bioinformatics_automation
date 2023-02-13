#!/bin/bash
# sample=2022WSSW005215-T

annovar_path=/opt/annovar
filter_merge_vcf_dir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}

$annovar_path/table_annovar.pl \
       	$filter_merge_vcf_dir/${sample}.filter_merge.vcf  \
       	$annovar_path/humandb/ \
	-buildver hg19 \
	-out $filter_merge_vcf_dir/${sample}.anno \
	-remove \
	-protocol refGene,cytoBand,clinvar_20220320 \
	-operation g,r,f \
	-nastring . \
	-vcfinput \
	-polish

