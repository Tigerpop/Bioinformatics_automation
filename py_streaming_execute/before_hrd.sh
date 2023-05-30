#!/bin/bash

# 例子：bash before_hrd.sh sample=2023WSSW001742-T bed=BC17T output=~/py_generate/1743/1743

# 解析参数
for param in "$@"
do
    case "$param" in
        sample=*)
            sample="${param#*=}"
            ;;
        bed=*)
            bed="${param#*=}"
            ;;
        output=*)
            output="${param#*=}"
            ;;
        *)
            echo "未知参数: $param"
            exit 1
            ;;
    esac
done

cd /home/chenyushao/py_streaming_execute
# 执行Python命令
python /home/chenyushao/py_streaming_execute/before_hrd.py "$sample" "$bed" "$output"

# 继续Shell脚本的其他操作...
