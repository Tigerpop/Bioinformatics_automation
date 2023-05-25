#!/bin/bash

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        summery=*)
        summary_path="${key#*=}"
        shift
        ;;
        *)
        # 忽略未知参数
        shift
        ;;
    esac
done

# 调用 Python 脚本
python /home/chenyushao/doctor_assign_tasks/build_pollution_repository/build_pollution_warehouse.py "$summary_path"
