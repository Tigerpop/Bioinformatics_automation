# -*- coding: utf-8 -*-
import quality_control as qc
import re,os,sys

sample = sys.argv[1] # 第一个参数
log_path = sys.argv[2]
generate_location = sys.argv[3]


QC = qc.tool()
base_quality,inser_size_peak,duplication_rate = QC.process_fastp_log(sample,log_path,generate_location)     # 质量控制。
if int(inser_size_peak) < 60:
    with open(f'{log_path}/quality_control/Quality_Control.txt','a+')as f0:                      # 不符合条件，就停止后续流程。
        f0.write('fastp 结果质控不合格！！'+"\n")
        f0.write('base_quality: '+str(base_quality)+'\n')
        f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
        f0.write('duplication_rate: '+str(duplication_rate)+'\n')
    exit(1)
with open(f'{log_path}/quality_control/Quality_Control.txt','a+')as f0:
    f0.write('fastp 结果质控合格！！'+"\n")
    f0.write('base_quality: '+str(base_quality)+'\n')
    f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
    f0.write('duplication_rate: '+str(duplication_rate)+'\n')
