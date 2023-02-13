#!/bin/bash
# sample=2022WSSW005215-T

export LC_ALL=C
human_genome_index=/home/chenyushao/wes_cancer/data/hg19/gatk_hg19
extract_fq_1=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.1.fq.gz
extract_fq_2=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.2.fq.gz
output=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.bwa_mem.bam

bwa mem -t 16 \
  $human_genome_index  \
  $extract_fq_1  \
  $extract_fq_2  \
  -o /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.unsort.bam

samtools sort -@ 16 -o $output /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.unsort.bam
