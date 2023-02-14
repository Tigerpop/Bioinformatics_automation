# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']    # /working_tmp  
human_genome_index = config['reference_document']['human_genome_index']
sample_dir = config['sample']['sample_dir'] 
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

print(sample_dir+"/"+sample_path)

# 给原始文件改名E150000469_L01_2022WSSW003294-T_2.fq.gz -> 2022WSSW003294-T_2.fq.gz
os.chdir(sample_dir+'/'+sample_path)
name_list = os.listdir('./')
if name_list[0][0]=='E':
    for name in name_list:
        newname = "_".join(name.split("_")[-2:])
        os.rename(name,newname)

tmp_dir = generate_location + '/'+sample_path
fa_gz_1 = sample_dir+'/'+sample_path+"/"+sample+'_1.fq.gz'
fa_gz_2 = sample_dir+'/'+sample_path+'/'+sample+'_2.fq.gz'
out_extract_1 = tmp_dir+'/'+sample+'_1.extract.fq.gz'
out_extract_2 = tmp_dir+'/'+sample+'_2.extract.fq.gz'
print(fa_gz_1,fa_gz_2)

os.system(f"mkdir -p {generate_location}/{sample_path}")
os.chdir(tmp_dir)


cmd = f'fastp -i {fa_gz_1} \
      -I {fa_gz_2} \
      -o {out_extract_1} \
      -O {out_extract_2} \
      -w 8 \
      -l 30  > fastp.log 2>&1' 
p = subprocess.Popen(cmd,shell=True)
p.communicate()
if p.returncode != 0:
    exit('fastp is false !!!')
