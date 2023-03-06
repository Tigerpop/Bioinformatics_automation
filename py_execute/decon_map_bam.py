# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
fasta = config['reference_document']['fasta']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]


# 根据 sample 去 sample 属于的 {bed_key}_receive.csv 表中去找同一个bed 的sample文件，循环滚动算decon。
sample_list = config['sample']['sample_list']
bed_list = config['bed']['bed_list']
sample_list = re.findall( r"\'(.*?)\'",sample_list)
bed_list = re.findall( r"\'(.*?)\'",bed_list)
bed_key = bed_list[sample_list.index(sample)].split(":")[0]
bed_key = bed_key.replace('-T','').replace('-N','')
bed = f'/refhub/{hg_19_or_38}/target/{bed_key}/Target_Regions.bed'  # decon 用的bed 一定要是exon处理后的bed。
bed1 = f'/refhub/{hg_19_or_38}/target/{bed_key}/customNumbering.txt'

def build_bam_file():
    tmp_dir = f"{generate_location}/{sample_path}/"+"decon_generate"
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    os.chdir(f"{generate_location}")
    
    # str_pattern = re.compile(r".*[0-9]$")       # 正则出以数字结尾的。sorted 一下以防乱序。
    # listdir = list(filter(lambda x: True if str_pattern.match(x) else False,sorted(os.listdir(f"{generate_location}"))))
    # print(listdir)
    # 
    
    df_received = pd.read_csv(f'/received/{bed_key}_received.csv',sep='\t')
    listdir = sorted( filter(lambda x: x!='null',df_received['样本编号*'].fillna('null',inplace=False).drop_duplicates().tolist() ) )
    print(listdir)
    windows_length = 10                         # 取10个文件的量。一定要保证样本已经运行完成超过此数量，才能运行decon。
    windows_list = [sample]
    sample_index = (listdir.index(sample) + 1)%len(listdir)                     # 循环滚
    while len(windows_list) < windows_length and sample!=listdir[sample_index]: # 循环回来遇到自己了就停下来。
        # print(sample_index,listdir[sample_index])
        # 要保证 bwa_bam文件已经彻底生成。才能把bwa_bam文件 加入进窗口列表。
        print(sample_index)
        sample_father = listdir[sample_index].replace('-T','').replace('-N','')
        try:
            bam_file1 = generate_location+"/"+sample_father+"/"+listdir[sample_index]+"/"+listdir[sample_index]+".dedup.bam"
            bam_file2 = generate_location+"/"+sample_father+"/"+listdir[sample_index]+"/"+listdir[sample_index]+".markdup.bam"
            print(bam_file2)
            if (os.path.exists(bam_file1) or os.path.exists(bam_file2)):
                windows_list.append(listdir[sample_index])           # 考虑到可能是 -T 可能 —N 所以这样写。
            sample_index =  (sample_index + 1)%len(listdir)
        except FileNotFoundError:
            print('跳过一个')
            sample_index =  (sample_index + 1)%len(listdir)
            continue

    print(windows_list)


    os.chdir(tmp_dir)
    with open('./bam_file.txt','w')as f:
        for ele in windows_list:
            parent = ele.replace('-T','').replace('-N','')
            f.write(f"{generate_location}/{parent}/{ele}/"+ele+".bwa_mem.bam"+"\n")
            
def run_DeCoN():
    tmp_dir = f"{generate_location}/{sample_path}/"+"decon_generate"
    os.chdir(tmp_dir)
    cmd_0 = f"Rscript /opt/DECoN/ReadInBams.R \
            --bams ./bam_file.txt \
            --bed {bed} \
            --fasta {fasta} \
            --out {tmp_dir}/DECoNtest > ReadInBams.log 2>&1"
    cmd_1 = f"Rscript /opt/DECoN/IdentifyFailures.R  \
            --RData DECoNtest.RData   \
            --exons {bed1} \
            --mincorr .98 \
            --mincov 100 \
            --out DECoNtest > IdentifyFailures.log 2>&1"
    cmd_2 = f"Rscript /opt/DECoN/makeCNVcalls.R \
            --RData DECoNtest.RData \
            --exons {bed1} \
            --out DECoNtestCalls > makeCNVcalls.log 2>&1"
    for i in range(3):
        p = subprocess.Popen(locals()['cmd_'+f"{i}"],shell=True)
        p.communicate()


if __name__=='__main__':
    print(bed,bed1)
    build_bam_file()
    run_DeCoN()



# ##################################################
# cd  /home/chenyushao/py_generate/test
# 
# Rscript /opt/DECoN/ReadInBams.R \
#         --bams /home/chenyushao/py_generate/test/bam_file.txt \
#         --bed  /home/chenyushao/doctor_assign_tasks/hg19_bed/four_field.bed \
#         --fasta /refhub/hg19/fa/fa/ucsc.hg19.fasta \
#         --out /home/chenyushao/py_generate/test/DECoNtest > ReadInBams.log 2>&1
# 
# Rscript /opt/DECoN/IdentifyFailures.R  \
#         --RData DECoNtest.RData   \
#         --mincorr .98 \
#         --mincov 100 \
#         --out DECoNtest > IdentifyFailures.log 2>&1
# 
# #       --exons	/home/chenyushao/doctor_assign_tasks/four_field.bed \
# 
# 
# Rscript /opt/DECoN/makeCNVcalls.R \
#         --RData DECoNtest.RData \
#         --out DECoNtestCalls > makeCNVcalls.log 2>&1
