#!/bin/bash
export sample_parent='2022WSSW004388-T'

sample_dir=/home/chenyushao/cumulative_download/datelog
cd $sample_dir/$sample_parent

# 预处理 
son_list=`ls $sample_dir/$sample_parent`
file_count=0
for son in $son_list
do  
    if [[ -f $son ]];then
        file_count=$(($file_count+1))
    fi
done
echo "若没有文件，说明文件已经被预处理；文件个数为:"$file_count
if [[ $file_count != 0 ]];then 
    echo "begin,开始预处理。"
    ls $sample_dir/$sample_parent | awk -F " " '{print $1}' | grep '_1.fq.gz' | awk -F "_1." '{print$1}' > temp_name
    while read row 
        do
        mkdir -p $row
        filelist=`ls $sample_dir/$sample_parent`
        for file in $filelist
            do
            echo $row $file
            if [[ $file == *$row* ]] && [[ $row != $file ]]; then
                mv $file $row/
            fi
            done
        done < ./temp_name
    rm -rf ./temp_name
else 
    echo "已经预处理，so跳过预处理步骤。"
fi


# 遍历sample_parent文件夹。对样本编号下所有sample依次运行自动化脚本；
echo "遍历sample_parent文件夹。对样本编号下所有sample依次运行自动化脚本；"
cd  /home/chenyushao/sh_exe执行文件汇总
son_list=`ls $sample_dir/$sample_parent`
for son in $son_list
do  
    echo $son
    export sample=$son    # 直接临时写入环境，让下属的脚本都有这个变量；

    cmds=(
    connect_env_fq_umi.sh
    connect_env_call_mutation_fbs.sh
    )
    for cmd in ${cmds[@]}
    do
      env_sh=${cmd:12}
      envs=${env_sh%.*}
      source /opt/miniconda3/etc/profile.d/conda.sh     # 这样才能在脚本中激活conda。
      conda activate $envs

      echo "开始执行 "$envs"虚拟环境中的脚本 ： start!"
      bash ${cmd}
      if [ $? -ne 0 ]; then
        echo  "注意！！！"${cmd}" failed!"
        echo "注意： "$envs"虚拟环境中的脚本出现问题。 "
        exit
      else
        echo "注意！！！"${cmd}" succeed!"
        echo $envs"虚拟环境中的脚本运行完毕。 "
      fi

      conda deactivate 
    done

done







