# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

sample_dir = generate_location+"/"+sample_path


if not os.path.exists(f'{generate_location}/{hg_19_or_38}.2bit'):
    print('f{hg_19_or_38}.2bit文件不存在，现在生成。')
    fatotwobit = config['faToTwoBit']['fatotwobit']
    parameters_pool = config['faToTwoBit']['parameters_pool']
    cmd = f"{fatotwobit} \
    {parameters_pool}"
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(2)
else:
    print(f'{hg_19_or_38}.2bit文件已经存在')

os.chdir(sample_dir)
if not os.path.exists("factera_generate"):
    os.mkdir("factera_generate")

tumor_bam = sample_dir+"/"+sample+".bwa_mem.bam"
cmd1 = f"cp {tumor_bam} {tumor_bam}.bai {sample_dir}/factera_generate/ "
os.chdir("./factera_generate")
p = subprocess.Popen(cmd1,shell=True)
p.communicate()
if p.returncode != 0:
    exit(2)

tumor_bam = sample_dir+"/factera_generate"+"/"+sample+".bwa_mem.bam"
factera_path = config['factera']['factera_path']
tool = config['factera']['tool']
parameters_pool = config['factera']['parameters_pool']
cmd = f"{factera_path}/{tool} \
      {tumor_bam} \
      {parameters_pool}"
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(2)

cmd = f'rm -rf {tumor_bam} {tumor_bam}.bai '
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(2)
    
    
    
    
# list_dir = os.listdir(generate_location+"/"+parent_name+"/"+sample)
# for file in list_dir:
#     if re.search("factera",file) and file!="factera_generate":
#         p = subprocess.Popen("mv {} {}".format(file,"factera_generate"),shell=True)
#         p.communicate()
#         if p.returncode != 0:
#             exit(2)
            
            
# #####################################
# # 先做一个2bit文件方便找索引。
# cd /home/chenyushao/draft
# if [[ ! -f "hg19.2bit"  ]];then
#     /opt/factera/faToTwoBit \
#     /home/chenyushao/wes_cancer/data/hg19/ucsc.hg19.fasta \
#     /home/chenyushao/draft/hg19.2bit
#     echo "新建2bit文件"
# else
#     echo "2bit 文件已经存在"
# fi 
# 
# # 这个指定位置自己设定的的bed文件领导放在如下文件夹位置；
# # 可以在ucsc 网站的 liftover 模块下完成 hg19与hg38 相互之间格式的转换；
# # 可以在网站内直接转好，也能下载liftover的转换工具，自己命令用。
# tumor_dir=/home/chenyushao/sh_temp生成文件汇总/2021WSSW000188-T/E150000432_L01_2021WSSW000188-T/
# tumor_bam=$tumor_dir/E150000432_L01_2021WSSW000188-T.dedup.bam
# samtools index -@ 8  $tumor_bam  $tumor_bam.bai
# # mkdir factera_warehouse
# /opt/factera/factera.pl \
#     $tumor_bam \
#     /public/kitbed/BC17/BC17.raw.hg19.bed \
#     /home/chenyushao/draft/hg19.2bit \
#     -o /home/chenyushao/draft/factera_warehouse   # 很奇怪不能指定存储位置。
