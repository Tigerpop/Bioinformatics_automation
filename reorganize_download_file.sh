#!/bin/bash
repository=/home/chenyushao/cumulative_download/datelog
# repository=/fastq_data

process_fq_gz() {
  if [[ `ls $repository/*.fq.gz|wc -l` == 0 ]];then
    echo "*.fq.gz已经处理完毕，结束第一个整理方法。"
    return 1
  fi
  ls $repository/*.fq.gz > $repository/temp_file
  while read line
  do 
    potential_dir=${line%_*}
    potential_dir=${potential_dir##*_}
    filename=${line##*/}
    echo $line
    echo $filename
    echo $potential_dir
    if [[ -d "$repository/$potential_dir" ]];then
      echo "潜在文件夹已经存在。"
      inner_fqgz=`ls -Rl $repository/$potential_dir | grep $filename`
      outer_fqgz=`ls -l $repository | grep $filename`
      if [[ `echo $inner_fqgz |wc -l` == 1  ]];then
        echo "潜在文件夹中已经存在该文件。"
          if [[ `echo $inner_fqgz |awk '{print $5}'` -ge `echo $outer_fqgz |awk '{print $5}'` ]];then
            echo "且潜在文件夹中该文件size>=该文件size。所以删除外部对应*.fq.gz文件。"
            rm -rf $repository/$filename
          else 
            echo "潜在文件夹中该文件size<该文件size,所以删除潜在文件夹中对应*.fq.gz文件，把外部的移动进去。"
            rm -rf $repository/$potential_dir/$filename
            mv $repository/$filename  $repository/$potential_dir/
          fi
      else
        echo "潜在文件夹中不存在该文件，把文件移动进去。"
        mv $repository/$filename  $repository/$potential_dir/
      fi
    else
      echo "潜在文件夹不存在，创建它,并把文件移动进去。"
      mkdir $repository/$potential_dir
      mv $repository/$filename  $repository/$potential_dir/
    fi
  done < $repository/temp_file
  rm -rf $repository/temp_file
}

process_T_N() {
  if [[ `ls $repository|grep "\-.$"|wc -l` == 0 ]];then
    echo "TN结尾文件夹已经处理完毕，结束第二个整理方法。"
    return 1
  fi
  ls -F $repository | grep '\-./$' > $repository/temp_file
  # ls -F $repository/RawData | grep '\-./$' >> $repository/temp_file
  new_creation_dir=0
  while read line
  do
    simplify_dir=${line%%-*}
    line=${line%%/*}
    #echo $line
    echo $simplify_dir
    if [[ ! -d "$repository/$simplify_dir" ]];then
      echo "不存在精简文件夹，创建。"
      mkdir -p $repository/$simplify_dir
    elif [ $new_creation_dir != $simplify_dir  ];then
      echo "已经存在同名精简文件夹，在原始同名精简文件夹后加before+日期。"
      date=`date +%Y-%m-%d`
      mv $repository/$simplify_dir $repository/$simplify_dir"-before-"$date
      mkdir -p $repository/$simplify_dir
    fi
    # 以后这里要修改。
    mv $repository/$line  $repository/$simplify_dir/
    echo "把"$repository/$line" 移动到 "$repository/$simplify_dir
    new_creation_dir=$simplify_dir
    echo "TN执行次数"
    # rm -rf $repository/$line 
  done < $repository/temp_file
  #rm -rf $repository/temp_file
}

# 处理刚刚下载的总母文件夹下直接放置的fa.gz文件的情况。
# process_direct_fagz() {
#   
# }
process_fq_gz
process_T_N
# process_direct_fagz