# -*- coding: utf-8 -*-

import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_dir = config['sample']['sample_dir'] 
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]


inputpath_1 = sample_dir+"/"+sample_path+"/"+sample+"_1.fq.gz"
inputpath_2 = sample_dir+"/"+sample_path+"/"+sample+"_2.fq.gz"
outputpath_1 = generate_location+"/"+sample_path+"/"+sample+".extracted.1.fq.gz"
outputpath_2 = generate_location+"/"+sample_path+"/"+sample+".extracted.2.fq.gz"
os.system(f"mkdir -p {generate_location}/{sample_path}")

print(inputpath_1,outputpath_1)
cmd = f"umi_tools extract --extract-method=string \
  		  --bc-pattern=NNNNN \
  		  --bc-pattern2=NNNNN \
  		  --stdin={inputpath_1} \
  	    --stdout={outputpath_1} \
  	   	--read2-in={inputpath_2} \
  		  --read2-out={outputpath_2} \
  		  --ignore-read-pair-suffixes"
p = subprocess.Popen(cmd,shell=True)
p.communicate()
# 注意，这里要用一个p.returncode 把子进程中是否正常结束，传导到本脚本中。再通过exit()传导到上层脚本中。
if p.returncode != 0:
    exit(2)


# returncode = p.returncode
# if returncode == 0:
#     print( "  successed!" )
# else:
#     print("  failed!")
#     subprocess.call("pause",shell=True)  # 暂停
#     exit(2) # 这里决定了上层脚本中，p.retruncode() 会得到一个2，表示下层脚本未正常结束。
# 
# ###################################
# team_dir=/home/chenyushao/cumulative_download/datelog/${sample_parent}
# 
# 
# wholename="$(ls ${team_dir}/${sample} | grep '1.fq.gz' )"   
# wname=${wholename%_*}
# inputpath_1=$team_dir/${sample}/${wname}_1.fq.gz
# inputpath_2=$team_dir/${sample}/${wname}_2.fq.gz
# 
# cd /home/chenyushao/sh_temp生成文件汇总
# mkdir -p ${sample_parent}/${sample}
# outputpath_1=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.1.fq.gz
# outputpath_2=/home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}_extracted.2.fq.gz
# 
# umi_tools extract --extract-method=string \
#   		  --bc-pattern=NNNNN \
#   		  --bc-pattern2=NNNNN \
#   		  --stdin=$inputpath_1 \
#   	    --stdout=$outputpath_1 \
#   	   	--read2-in=$inputpath_2 \
#   		  --read2-out=$outputpath_2 \
#   		  --ignore-read-pair-suffixes
#   		  # -L /home/chenyushao/sh_temp生成文件汇总/${sample_parent}/${sample}/${sample}.extracted.log 
