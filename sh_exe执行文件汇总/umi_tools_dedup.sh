#!/bin/bash
# sample=2022WSSW005215-T

input=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.bwa_mem.bam
inputdir=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
output=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.dedup.bam

samtools index -@ 16 \
	$input \
	$inputdir/${sample}.bwa_mem.bam.bai 

umi_tools dedup  \
	--output-stats=deduplicated  \
	--stdin=$input  \
	--stdout=$output

cp $inputdir/${sample}.bwa_mem.bam $inputdir/${sample}.undedup.bam
cp $inputdir/${sample}.bwa_mem.bam.bai $inputdir/${sample}.undedup.bam.bai
