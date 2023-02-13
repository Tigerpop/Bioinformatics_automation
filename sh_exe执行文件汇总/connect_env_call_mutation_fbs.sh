#!/bin/bash
# export sample=2022WSSW005215-T # 直接临时写入环境，让下属的脚本都有这个变量；

cmds=(
split_add_index_chr.sh
call_mutation_fbs.sh
merge_vcf.sh
filter_vcf.sh
annovar_filter_merge_vcf.sh
)
for cmd in ${cmds[@]}
do
  echo "注意！！！"${cmd}" start!"
  bash ${cmd}
  if [ $? -ne 0 ]; then
    echo  "注意！！！"${cmd}" failed!"
    exit 8
  else
    echo "注意！！！"${cmd}" succeed!"
  fi
done 
