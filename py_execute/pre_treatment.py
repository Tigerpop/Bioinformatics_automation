# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
config = configparser.ConfigParser()
config.read('config.ini')
sample_parent = config['sample']['sample_parent']
generate_dir = config['generate']['location']
son_list = os.listdir(sample_parent)
os.chdir(sample_parent) # cd 一个意思

file_count = 0 
for son in son_list:
    if os.path.isfile(sample_parent+ "/" + son):
        file_count += 1 
print("若没有文件，说明文件已经被预处理；文件个数为:%d"%file_count)
if file_count != 0:
    print("begin,开始预处理。")
    p = subprocess.Popen("ls %s | gawk -F ' ' '{print $1}' | grep '_1.fq.gz' | awk -F '_1.' '{print$1}' > %s/temp_name "%(sample_parent,generate_dir),shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(1)
    
    with open('{generate_dir}/temp_name'.format(generate_dir=generate_dir),'r')as f:
        row = f.readline().strip('\n')
        os.makedirs(sample_parent+"/"+row)
        for file in son_list:
            print(row,file)
            if re.search(row,file):
                os.system("mv {} {}".format(file,row))
    os.remove('{generate_dir}/temp_name'.format(generate_dir=generate_dir))
else:
    print("已经预处理，so跳过预处理步骤。")
    
