# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys,datetime
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

# 确定bed名。
sample_list = config['sample']['sample_list']
bed_list = config['bed']['bed_list']
sample_list = re.findall( r"\'(.*?)\'",sample_list)
bed_list = re.findall( r"\'(.*?)\'",bed_list)
bed_key = bed_list[sample_list.index(sample)].split(":")[0]

extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'


os.chdir(generate_location+"/"+sample_path)
if not os.path.exists("msisensor_generate"):
    os.mkdir("msisensor_generate")

msisensor_tool = config['msisensor']['tools']
msisensor_pool = config['msisensor']['msisensor_pool']
input_bam = generate_location+"/"+sample_path +"/"+sample+f".{dedup_or_markdup}.bam"
out_msi = generate_location+"/"+sample_path+"/"+"msisensor_generate"+"/"+sample+"msi"

cmd1 = f"samtools index -@ 10 {sample}.{dedup_or_markdup}.bam {sample}.{dedup_or_markdup}.bam.bai"
if bed_key[-1]!='T':
    cmd2 = f"{msisensor_tool} \
            {msisensor_pool} \
            -t {input_bam} \
            -o {out_msi}"
else:
    sample_path_N,sample_N =  sample_path.replace('-T','-N'),sample.replace('-T','-N')
    normal_bam = generate_location +"/" + sample_path_N + "/" + sample_N + f".{dedup_or_markdup}.bam"
    tumor_bam = generate_location +"/" + sample_path + "/" + sample + f".{dedup_or_markdup}.bam"
    normal_markdup_have_build = generate_location +"/" + sample_path_N + "/"+ 'markdup_have_build'
    start_time = datetime.datetime.now()
    while not os.path.exists(normal_markdup_have_build):
        print("等待文件生成...")
        time.sleep(1)
    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    print(f"对应文件 normal的 markdup.bam 已生成，等待 {time_diff} 秒后退出程序...")
    cmd2 = f"{msisensor_tool} \
            {msisensor_pool} \
            -t {tumor_bam} \
            -n {normal_bam} \
            -o {out_msi}"
for i in range(1,3):
    cmd = "cmd"+str(i)
    p = subprocess.Popen(locals()[cmd],shell=True)
    p.communicate()
    if p.returncode != 0:
        exit('msisensor is false!')



# ########################################################
# #!/bin/bash
# msisensor_dir=/opt/msisensor-ct-master
# bam_dir=/home/chenyushao/sh_temp生成文件汇总
# cd /home/chenyushao/draft
# mkdir msisensor_test
# output_dir=/home/chenyushao/draft/msisensor_test
# 
# samtools index -@ 2 $bam_dir/dedup.bam $bam_dir/dedup.bam.bai
# $msisensor_dir/msisensor-ct msi \
# 	-D \
# 	-M $msisensor_dir/models_hg19_GRCh37 \
# 	-t $bam_dir/dedup.bam \
# 	-o $output_dir/msi
