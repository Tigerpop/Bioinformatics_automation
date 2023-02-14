#!/bin/bash
source activate no_umitools_py
python -V
sample_path=$1

echo $sample_path

# 只要 在终端 source activate_env_fq_umi.sh
# 就能把脚本外的终端变成 这个虚拟环境。
# 我们实际上是在python总脚本中 ，用subprocess紫禁城中运行了source activate_env_fq_umi.sh 。
conda env list

python connect_env_no_umitools_py.py $sample_path
returncode=$?  # 获取上面运行后的返回值。

conda deactivate
conda env list

exit $returncode