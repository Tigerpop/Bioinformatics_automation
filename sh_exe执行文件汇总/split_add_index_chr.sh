#!/bin/bash
# sample=2022WSSW005215-T

file_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
cd $file_path
if [ ! -d "$file_path/chr_split"  ]; then
        mkdir -p $file_path/chr_split
fi

cp ${sample}.dedup.bam chr_split/
cd chr_split

inputpath=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/chr_split

bamtools split -in $inputpath/${sample}.dedup.bam  -reference

samtools index -@ 2 $inputpath/${sample}.dedup.REF_chrX.bam $inputpath/${sample}.dedup.REF_chrX.bam.bai
samtools index -@ 2 $inputpath/${sample}.dedup.REF_chrY.bam $inputpath/${sample}.dedup.REF_chrY.bam.bai
for ((i=1;i<=22;i++))
do
    samtools index -@ 2 $inputpath/${sample}.dedup.REF_chr$i.bam $inputpath/${sample}.dedup.REF_chr$i.bam.bai
done

