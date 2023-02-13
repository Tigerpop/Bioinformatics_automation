#!/bin/bash
# export sample=2022WSSW005215-T # 直接临时写入环境，让下属的脚本都有这个变量；

cmds=(
umitools_extract.sh
bwa_文件对比.sh
umi_tools_dedup.sh
)
for cmd in ${cmds[@]}
do
  echo ${cmd}" start!"
  bash ${cmd}
  if [ $? -ne 0 ]; then
    echo  ${cmd}" failed!"
    exit 6
  else
    echo ${cmd}" succeed!"
  fi
done
