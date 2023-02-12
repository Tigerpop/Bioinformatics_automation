# -*- coding: utf-8 -*-
import configparser,subprocess,re,os
import subprocess
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_parent = config['sample']['sample_parent']
parent_name = sample_parent.split('fastq_data/')[1]
extract_mode = config['extract_mode']['choose']

# sample 是一个这样的文件  E100063570_L01_2021WSSW001567-T 
# 借助第三方文件，把sample 传导到每一个脚本。

        
if __name__=="__main__":
    py_execute_dir = "/home/chenyushao/py_execute/"
    cmd = "python pre_treatment.py"
    p = subprocess.Popen(cmd,shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line: print('Subprogram output: [{}]'.format(line))
    p.communicate()
    
    if extract_mode == 'umi_mode':
        cmds = ["activate_env_fq_umi.sh",\
                "activate_env_call_mutation_fbs.sh"]
    if extract_mode == 'fastp_mode':
        cmds = ["activate_env_no_umitools_py.sh",\
                "activate_env_call_mutation_fbs.sh"]
    son_list = os.listdir(sample_parent)   # 这个sample一定是在预处理之后才能有！ jj 
    print(son_list)
    for sample in son_list:     # sample 是一个这样的文件  E100063570_L01_2021WSSW001567-T
        print(son_list,"have",sample)
        # 借助第三方文件，把sample 传导到每一个脚本。
        p = subprocess.Popen("echo sample = \\'{}\\' > samples.py".format(sample),shell=True)
        p.communicate()
        for cmd in cmds:
            bam_file1 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".dedup.bam"
            bam_file2 = generate_location+"/"+parent_name+"/"+sample+"/"+sample+".markdup.bam"
            if (os.path.exists(bam_file1) or os.path.exists(bam_file2)) and cmd==cmds[0]:
                continue
            print(cmd," start! ")
            p = subprocess.Popen("source %s%s"%(py_execute_dir,cmd),shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            # 一下方式是实时查看紫禁城subprocess中输出，自己选择看不看。
            while p.poll() is None:
                line = p.stdout.readline()
                line = line.strip()
                if line: print('Subprogram output: [{}]'.format(line))
            # p.wait()
            # 如果使用 subprocess.Popen，就不使用 Popen.wait()【可能死锁】，而使用 Popen.communicate() 来等待外部程序执行结束
            stdout,stderr = p.communicate()
            returncode = p.returncode
            print(returncode)
            if returncode == 0:
                print( cmd+"  successed!" )
            else:
                print(cmd+"  failed!")
                subprocess.call("pause",shell=True)  # 暂停
                exit(100)
