# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_dir = config['sample']['sample_dir']
sample_list = config['sample']['sample_list']
extract_mode = config['extract_mode']['choose']

def work(sample_path):
    if extract_mode == 'umi_mode':
        cmds = [f"bash activate_env_fq_umi.sh {sample_path}",\
                f"bash activate_env_call_mutation_fbs.sh {sample_path}"]
    if extract_mode == 'fastp_mode':
        cmds = [f"bash activate_env_no_umitools_py.sh {sample_path}",\
                f"bash activate_env_call_mutation_fbs.sh {sample_path}"]
    for cmd in cmds:
        bam_file1 = generate_location+"/"+sample_path+"/"+sample+".dedup.bam"
        bam_file2 = generate_location+"/"+sample_path+"/"+sample+".markdup.bam"
        if (os.path.exists(bam_file1) or os.path.exists(bam_file2)) and cmd==cmds[0]:
            continue
        print(cmd," start! ")
        p = subprocess.Popen(cmd,shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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

        
if __name__=="__main__":
    py_execute_dir = "/home/chenyushao/py_execute/"
    
    sample_list = re.findall( r"\'(.*?)\'",sample_list)
    pre_sample_list = list(map(lambda x: x.replace('-T',"").replace('-N',""),sample_list))
    
    # 以一个sample为例子先跑通。
    jobs = []
    for _ in range(len(sample_list)):
        sample = sample_list[_]
        pre_sample = pre_sample_list[_]
        sample_path = pre_sample+"/"+sample
        jobs.append(sample_path)
    print(jobs)
    pool = Pool(processes=3)
    for ele in jobs:
        pool.apply_async(work,(ele,))
    pool.close()
    pool.join()
    
    
    
# def work(sample_path):
#     if extract_mode == 'umi_mode':
#         cmds = [f"bash activate_env_fq_umi.sh {sample_path}",\
#                 f"bash activate_env_call_mutation_fbs.sh {sample_path}"]
#     if extract_mode == 'fastp_mode':
#         cmds = [f"bash activate_env_no_umitools_py.sh {sample_path}",\
#                 f"bash activate_env_call_mutation_fbs.sh {sample_path}"]
#     for cmd in cmds:
#         bam_file1 = generate_location+"/"+sample_path+"/"+sample+".dedup.bam"
#         bam_file2 = generate_location+"/"+sample_path+"/"+sample+".markdup.bam"
#         if (os.path.exists(bam_file1) or os.path.exists(bam_file2)) and cmd==cmds[0]:
#             continue
#         print(cmd," start! ")
#         p = subprocess.Popen(cmd,shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#         # 一下方式是实时查看紫禁城subprocess中输出，自己选择看不看。
#         while p.poll() is None:
#             line = p.stdout.readline()
#             line = line.strip()
#             if line: print('Subprogram output: [{}]'.format(line))
#         # p.wait()
#         # 如果使用 subprocess.Popen，就不使用 Popen.wait()【可能死锁】，而使用 Popen.communicate() 来等待外部程序执行结束
#         stdout,stderr = p.communicate()
#         returncode = p.returncode
#         print(returncode)
#         if returncode == 0:
#             print( cmd+"  successed!" )
#         else:
#             print(cmd+"  failed!")
#             subprocess.call("pause",shell=True)  # 暂停
#             exit(100)
