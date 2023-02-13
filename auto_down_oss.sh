#! /bin/bash
# 还是需要先ossutil64 config 配置一下，我在脚本中没有把配置过程写进来。

read -p "请输入oss地址" oss
# read -p "新建一个要存放的位置" path
path=/home/chenyushao/cumulative_download/datelog
# path=/fastq_data

# 其实只要让 md5中的唯一标识符放在名字前，就能让名字变成唯一标识符。
# 再把整理脚本中，有精简文件夹就不移动的逻辑改一下，改成精简文件夹中唯一标识符已经存在，就不移动。
auto_download() {
        ossutil64 ls $oss | awk -F " " '{print $(NF)}' | grep "^oss://.*[/]$" > ./temp_dir_download
        ossutil64 ls $oss | awk -F " " '{print $(NF)}' | grep "^oss://.*[^/]$" > ./temp_file_download
        have_or_not="nothave"
        # shell中使用管道会生成一个子shell，在子shell中使用while、for循环的代码也是在子shell中执行的，所以在循环中的修改的变量只在子shell中有效，当循环结束时，会回到主shell，子shell中修改的变量不会影响主shell中的变量
        while read line
        do
          if [[ $line == *MD5* ]];then
      	    have_or_not="have"
      	    echo "MD5 存在"
          fi
        done < ./temp_file_download
        echo $have_or_not
        if [[ $have_or_not == "nothave" ]];then
          echo "MD5 文件不存在，退出任务。"
          exit 8
        fi
        # 读oss路径，并放在临时文件夹。     
        while  read row 
        do                             
        ossutil64 cp $row $path/
        done < ./temp_file_download
        
        while read row 
        do
        if [[ ${row##*RawData/} == "" ]];then
          continue
        fi
        oldIFS=$IFS
        IFS="/"
        array=($row)
        dir=${array[-1]}
        IFS=$oldIFS
        newpath=$path"/"$dir
        ossutil64 cp -r $row $newpath 
        done < ./temp_dir_download
        
        while read row 
        do
        if [[ ${row##*RawData/} == "" ]];then
          continue
        fi
        temp_name=${row##*RawData/}
        temp_name=${temp_name%/*}
        # echo $temp_name
        cp -r $path/RawData/$temp_name  $path/
        done < ./temp_dir_download
}
auto_download

bash ~/reorganize_download_file.sh  # 前面下载好了，交给整理脚本整理一下。 
