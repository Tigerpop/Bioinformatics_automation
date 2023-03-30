# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
import quality_control as qc
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']    # /working_tmp  
sample_dir = config['sample']['sample_dir']
human_genome_index = config['reference_document']['human_genome_index']
sample_dir = config['sample']['sample_dir'] 
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

sample_list = config['sample']['sample_list']
bed_list = config['bed']['bed_list']
sample_list = re.findall( r"\'(.*?)\'",sample_list)
bed_list = re.findall( r"\'(.*?)\'",bed_list)
bed = bed_list[sample_list.index(sample)].split(":")[1]
bed_key = bed_list[sample_list.index(sample)].split(":")[0]

print('bed is :'+bed)



print(sample_dir+"/"+sample_path)

# 给原始文件改名E150000469_L01_2022WSSW003294-T_2.fq.gz -> 2022WSSW003294-T_2.fq.gz
os.chdir(sample_dir+'/'+sample_path)
name_list = os.listdir('./')
if name_list[0][0]=='E':
    for name in name_list:
        newname = "_".join(name.split("_")[-2:])
        os.rename(name,newname)

# a = bcx 抛出异常的测试。

tmp_dir = generate_location + '/'+sample_path
fa_gz_1 = sample_dir+'/'+sample_path+"/"+sample+'_1.fq.gz'
fa_gz_2 = sample_dir+'/'+sample_path+'/'+sample+'_2.fq.gz'
out_extract_1 = tmp_dir+'/'+sample+'_1.extract.fq.gz'
out_extract_2 = tmp_dir+'/'+sample+'_2.extract.fq.gz'
print(fa_gz_1,fa_gz_2)

if not os.path.exists(f"{generate_location}/{sample_path}"):
    os.system(f"mkdir -p {generate_location}/{sample_path}")
os.chdir(tmp_dir)

father = sample_path.split("/")[0]
print(f'{sample_dir}/{father}')
print(os.listdir(f'{sample_dir}/{father}'))
if (bed_key == 'BCP650' or bed_key == 'NBC650')  and len(os.listdir(f'{sample_dir}/{father}'))==2:       # 做一下 NGScheckmate 的质控，看看是不是一套。
    QC = qc.tool()
    TN_similarity = QC.NGScheckmate(sample_path,sample_dir,generate_location)
    if TN_similarity < 0.75:
        with open(f'{tmp_dir}/quality_control/Quality_Control.txt','w')as f0:                      # 不符合条件，就停止后续流程。
            f0.write('NGScheckmate 结果质控不合格！！'+"\n")
            f0.write('TN_similarity: '+str(TN_similarity)+'\n')
        exit(4)
    with open(f'{tmp_dir}/quality_control/Quality_Control.txt','a+')as f0:
        f0.write('NGScheckmate 结果质控合格！！'+"\n")
        f0.write('TN_similarity: '+str(TN_similarity)+'\n')
    
cmd = f'fastp -i {fa_gz_1} \
      -I {fa_gz_2} \
      -o {out_extract_1} \
      -O {out_extract_2} \
      -w 8 \
      -l 30  > fastp.log 2>&1'
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit(3)
    
QC = qc.tool()
base_quality,inser_size_peak,duplication_rate = QC.process_fastp_log(sample,sample_path,generate_location)     # 质量控制。
if int(inser_size_peak) < 2:
    with open(f'{tmp_dir}/quality_control/Quality_Control.txt','a+')as f0:                      # 不符合条件，就停止后续流程。
        f0.write('fastp 结果质控不合格！！'+"\n")
        f0.write('base_quality: '+str(base_quality)+'\n')
        f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
        f0.write('duplication_rate: '+str(duplication_rate)+'\n')
    exit(4)
with open(f'{tmp_dir}/quality_control/Quality_Control.txt','a+')as f0:
    f0.write('fastp 结果质控合格！！'+"\n")
    f0.write('base_quality: '+str(base_quality)+'\n')
    f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
    f0.write('duplication_rate: '+str(duplication_rate)+'\n')


    

