#!/bin/bash
# source activate call_mutation_fbs
# python -V
# 只要 在终端 source activate_env_call_mutation_fbs.sh 
# 就能把脚本外的终端变成 这个虚拟环境。
# 我们实际上是在python总脚本中 ，用subprocess紫禁城中运行了source activate_env_call_mutation_fbs.sh。

conda env list

# import configparser,subprocess,re,os
# config = configparser.ConfigParser()
# config.read('config.ini')
# Mutation_detection_choose = config['Mutation_detection']['choose']

# shell 读取config.ini 文件稍微有点麻烦。
config_ini="/home/chenyushao/py_execute/config.ini"
Mutation_detection_choose=`awk -F '=' '/\[Mutation_detection\]/{a=1}a==1&&$1~/choose/{print $2;exit}' $config_ini`
echo $Mutation_detection_choose
if [ $Mutation_detection_choose = "snv_indel" ];then
  source activate call_mutation_fbs
  python -V
  echo "fbs is start!"
  python connect_env_call_mutation_fbs.py
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate 
    conda env list
    exit $returncode
  fi
elif [ $Mutation_detection_choose = "sv" ];then
  source activate cnv_factera_delly 
  python -V
  echo "factera is start!"
  python factera.py
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate 
    conda env list
    echo 'factera have some problem.'
    exit $returncode
  fi
elif [ $Mutation_detection_choose = "hla" ];then
  source activate optitype
  python -V
  echo "optitype is start!"
  python optitype.py
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate 
    conda env list
    exit $returncode
  fi
elif [ $Mutation_detection_choose = "msi" ];then
  source activate call_mutation_fbs
  python -V
  echo "msisensor is start!"
  python msisensor.py
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate 
    conda env list
    exit $returncode
  fi
elif [ $Mutation_detection_choose = "cnv" ];then
  # 激活cnv需要的环境。
  source activate cnv_factera_delly
  python -V
  echo "cnvnator is start!"
  python cnvnator.py
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate 
    conda env list
    exit $returncode
  fi
fi
    
conda deactivate 
conda env list



