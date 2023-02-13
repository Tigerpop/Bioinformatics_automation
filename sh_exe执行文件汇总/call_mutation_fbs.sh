#!/bin/bash
# sample=2022WSSW005215-T

cd /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}
mkdir split_vcf
cd chr_split
bam_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/chr_split
output_path=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/split_vcf
fasta=/home/chenyushao/wes_cancer/data/hg19/ucsc.hg19.fasta

echo "x"
freebayes -f $fasta --min-alternate-count=2 \
  --min-alternate-fraction=0.01  \
  $bam_path/${sample}.dedup.REF_chrX.bam > $output_path/${sample}.dedup.REF_chrX.vcf &
echo "y"
freebayes -f $fasta --min-alternate-count=2 \
  --min-alternate-fraction=0.01 \
  $bam_path/${sample}.dedup.REF_chrY.bam > $output_path/${sample}.dedup.REF_chrY.vcf &

seq 1 22 | xargs -n"$((22/22))" |
{ while read line
  do {
    for i in $line
    do
    echo $i
    freebayes -f $fasta --min-alternate-count=2 \
    --min-alternate-fraction=0.01 \
    $bam_path/${sample}.dedup.REF_chr$i.bam > $output_path/${sample}.dedup.REF_chr$i.vcf  
    done
  } &
    done
  wait
}
