#!/bin/bash
# source activate call_mutation_fbs
# python -V
# 只要 在终端 source activate_env_call_mutation_fbs.sh 
# 就能把脚本外的终端变成 这个虚拟环境。
# 我们实际上是在python总脚本中 ，用subprocess紫禁城中运行了source activate_env_call_mutation_fbs.sh。

conda env list
sample_path=$1
bed_key=$2

echo $bed_key
if [[ $bed_key = "BC17" ]];then
  source activate call_mutation_fbs
  echo "fbs is start!"
  python connect_env_call_mutation_fbs.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate cnv_factera_delly
  python -V
  echo "factera is start!"
  python factera.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    echo 'factera have some problem.'
    exit $returncode
  fi
  conda deactivate
  python -V
  echo "decon is start!"
  python decon_map_bam.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  # source activate cnv_factera_delly
  # python -V
  # echo "cnvnator is start!"
  # python cnvnator.py $sample_path
  # returncode=$?
  # if [[ $returncode -ne 0 ]];then
  #   conda deactivate
  #   conda env list
  #   exit $returncode
  # fi
  # conda deactivate
  python collect.py $sample_path
  
elif [[ $bed_key = "Q120" ]] || [[ $bed_key = "SD160" ]];then
  source activate call_mutation_fbs
  echo "fbs is start!"
  python connect_env_call_mutation_fbs.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate cnv_factera_delly
  python -V
  echo "factera is start!"
  python factera.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    echo 'factera have some problem.'
    exit $returncode
  fi
  conda deactivate
  python -V
  echo "decon is start!"
  python decon_map_bam.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  # source activate cnv_factera_delly
  # python -V
  # echo "cnvnator is start!"
  # python cnvnator.py $sample_path
  # returncode=$?
  # if [[ $returncode -ne 0 ]];then
  #   conda deactivate
  #   conda env list
  #   exit $returncode
  # fi
  # conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "chemo is start!"
  python chemo.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "msisensor is start!"
  python msisensor.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  python collect.py $sample_path

elif [[ $bed_key = "NBC650" ]] || [[ $bed_key = "BCP650" ]];then
  source activate call_mutation_fbs
  echo "fbs is start!"
  python connect_env_call_mutation_fbs.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate cnv_factera_delly
  python -V
  echo "factera is start!"
  python factera.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    echo 'factera have some problem.'
    exit $returncode
  fi
  conda deactivate
  python -V
  echo "decon is start!"
  python decon_map_bam.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  # source activate cnv_factera_delly
  # python -V
  # echo "cnvnator is start!"
  # python cnvnator.py $sample_path
  # returncode=$?
  # if [[ $returncode -ne 0 ]];then
  #   conda deactivate
  #   conda env list
  #   exit $returncode
  # fi
  # conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "chemo is start!"
  python chemo.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "msisensor is start!"
  python msisensor.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate optitype
  python -V
  echo "optitype is start!"
  python optitype.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  python antigen_vcf.py $sample_path
  python neoantigen.py $sample_path
  python collect.py $sample_path

elif [[ $bed_key = "NBC650-T" ]] || [[ $bed_key = "BCP650-T" ]];then
  source activate cnv_factera_delly
  echo "varscan is start!"
  python varscan.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate cnv_factera_delly
  python -V
  echo "factera is start!"
  python factera.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    echo 'factera have some problem.'
    exit $returncode
  fi
  conda deactivate
  python -V
  echo "decon is start!"
  python decon_map_bam.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  source activate cnv_factera_delly
  python -V
  echo "cnvnator is start!"
  python cnvnator.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "msisensor is start!"
  python msisensor.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  source activate call_mutation_fbs
  python -V
  echo "chemo is start!"
  python chemo.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  python collect.py $sample_path
  
elif [[ $bed_key = "NBC650-N" ]] || [[ $bed_key = "BCP650-N" ]];then
  source activate cnv_factera_delly
  echo "varscan is start!"
  python varscan.py $sample_path
  returncode=$?
  if [[ $returncode -ne 0 ]];then
    conda deactivate
    conda env list
    exit $returncode
  fi
  conda deactivate
  python collect.py $sample_path
  
fi

# conda deactivate
conda env list

# # shell 读取config.ini 文件稍微有点麻烦。
# config_ini="/home/chenyushao/py_execute/config.ini"
# Mutation_detection_choose=`awk -F '=' '/\[Mutation_detection\]/{a=1}a==1&&$1~/choose/{print $2;exit}' $config_ini`
# echo $Mutation_detection_choose
# if [ $Mutation_detection_choose = "snv_indel" ];then
#   source activate call_mutation_fbs
#   python -V
#   echo "fbs is start!"
#   python connect_env_call_mutation_fbs.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "sv" ];then
#   source activate cnv_factera_delly 
#   python -V
#   echo "factera is start!"
#   python factera.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     echo 'factera have some problem.'
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "hla" ];then
#   source activate optitype
#   python -V
#   echo "optitype is start!"
#   python optitype.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "msi" ];then
#   source activate call_mutation_fbs
#   python -V
#   echo "msisensor is start!"
#   python msisensor.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "decon" ];then
#   source activate call_mutation_fbs
#   python -V
#   echo "decon is start!"
#   python decon_map_bam.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "chemo" ];then
#   source activate call_mutation_fbs
#   python -V
#   echo "chemo is start!"
#   python chemo.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# elif [ $Mutation_detection_choose = "cnv" ];then
#   # 激活cnv需要的环境。
#   source activate cnv_factera_delly
#   python -V
#   echo "cnvnator is start!"
#   python cnvnator.py $sample_path
#   returncode=$?
#   if [[ $returncode -ne 0 ]];then
#     conda deactivate 
#     conda env list
#     exit $returncode
#   fi
# fi
#     
# conda deactivate 
# conda env list



