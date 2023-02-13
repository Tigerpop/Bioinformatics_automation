#!/bin/bash 
team_dir=/home/chenyushao/cumulative_download/datelog/${sample_parent}
# sample=2022WSSW004468-N

wholename="$(ls ${team_dir}/${sample} | grep '1.fq.gz' )"   
wname=${wholename%_*}
inputpath_1=$team_dir/${sample}/${wname}_1.fq.gz
inputpath_2=$team_dir/${sample}/${wname}_2.fq.gz

cd /home/chenyushao/sh_temp生成文件汇总
mkdir -p ${sample_parent}/${sample}
outputpath_1=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.1.fq.gz
outputpath_2=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.2.fq.gz

umi_tools extract --extract-method=string \
  		  --bc-pattern=NNNNN \
  		  --bc-pattern2=NNNNN \
  		  --stdin=$inputpath_1 \
  	    --stdout=$outputpath_1 \
  	   	--read2-in=$inputpath_2 \
  		  --read2-out=$outputpath_2 \
  		  --ignore-read-pair-suffixes 
  		  # -L /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.extracted.log 
