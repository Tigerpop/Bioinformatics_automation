# -*- coding: utf-8 -*-
import quality_control as qc
import re,os,sys

sample = sys.argv[1] # 第一个参数
log_path = sys.argv[2] 
sample_path = sys.argv[3]
generate_location = sys.argv[4]
bed = sys.argv[5]



# 质量控制。
QC = qc.tool()
mapped,coverage,ontarget,depth,cleandepth = QC.process_bam(sample,log_path,sample_path,generate_location,bed) 
if float(mapped.split("%")[0]) < 0:                                                          
    with open(f'{log_path}/quality_control/Quality_Control.txt','a+')as f0:                      # 不符合条件，就停止后续流程。
        f0.write('dedup_markdup 的bam 结果质控不合格！！'+"\n")
        f0.write('mapped: '+str(mapped)+'\n')
        f0.write('coverage: '+str(coverage)+'\n')
        f0.write('ontarget: '+str(ontarget)+'\n')
        f0.write('depth: '+str(depth)+'\n')
        f0.write('cleandepth: '+str(cleandepth)+'\n')
    exit(1)
with open(f'{log_path}/quality_control/Quality_Control.txt','a+')as f0:
    f0.write('dedup_markdup 的bam 结果质控合格！！'+"\n")
    f0.write('mapped: '+str(mapped)+'\n')
    f0.write('coverage: '+str(coverage)+'\n')
    f0.write('ontarget: '+str(ontarget)+'\n')
    f0.write('depth: '+str(depth)+'\n')
    f0.write('cleandepth: '+str(cleandepth)+'\n')
