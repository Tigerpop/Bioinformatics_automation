# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_dir = config['sample']['sample_dir']
sample_list = config['sample']['sample_list']
bed_list = config['bed']['bed_list']                            # ['BC17:/refhub/hg19/target/BC17/BC17.raw.hg19.bed', 'Q120:/refhub/hg19/target/Q120/Q120.raw.hg19.bed', 'Q120:/refhub/hg19/target/Q120/Q120.raw.hg19.bed']
extract_mode = config['extract_mode']['choose']

def work(sample_path,bed):
    try:
        # print(sample_path,len(os.listdir(sample_dir+"/"+sample_path)))  
        sample = sample_path.split("/")[-1]
        if (not os.path.exists(sample_dir+"/"+sample_path)) or len(os.listdir(sample_dir+"/"+sample_path))!=2:
            with open('/working_tmp/need_manual_processing.txt','a+')as f:
                f.write('输入文件为不合法情况，请手工处理: '+sample_dir+"/"+sample_path+"\n")
            return sample_path,'为不合法情况，请手工处理。'
        if extract_mode == 'umi_mode':
            cmds = [f"bash activate_env_fq_umi.sh {sample_path}",\
                    f"bash activate_env_call_mutation_fbs.sh {sample_path} {bed}"]
        if extract_mode == 'fastp_mode':
            cmds = [f"bash activate_env_no_umitools_py.sh {sample_path}",\
                    f"bash activate_env_call_mutation_fbs.sh {sample_path} {bed}"]
        for cmd in cmds:
            print(sample,cmd,'look here !')
            bam_file1 = generate_location+"/"+sample_path+"/"+sample+".dedup.bam"
            bam_file2 = generate_location+"/"+sample_path+"/"+sample+".markdup.bam"
            if (os.path.exists(bam_file1) or os.path.exists(bam_file2)) and cmd==cmds[0]:
                print(sample,' 有 dudep或者markdup文件,跳过第一个环节，直接进入第二环节。')
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
                print('look here!!! ',cmd+"  failed!")
                # subprocess.call("pause",shell=True)  # 暂停
                exit(100)
    except:
        with open('/working_tmp/need_manual_processing.txt','a+')as log:
            log.write('执行出错，需要手工调整: '+sample_path+"\n")        
        print("运行：",cmd,"出现问题。")

        
if __name__=="__main__":
    py_execute_dir = "/home/chenyushao/py_execute/"
    
    sample_list = re.findall( r"\'(.*?)\'",sample_list)
    bed_list = re.findall( r"\'(.*?)\'",bed_list)
    pre_sample_list = list(map(lambda x: x.replace('-T',"").replace('-N',""),sample_list))
    
    # 以一个sample为例子先跑通。
    jobs = []
    for _ in range(len(sample_list)):
        sample = sample_list[_]
        pre_sample = pre_sample_list[_]
        sample_path = pre_sample+"/"+sample   # 2022WSSW003294/2022WSSW003294-T
        jobs.append(sample_path)
    # print(jobs)
    pool = Pool(processes=6)                   # 进程池中进程是 x 个。不影响池子中进程再开子进程。
    for i in range(len(jobs)):
        result = pool.apply_async(work,(jobs[i],bed_list[i].split(":")[0],))
        # output = result.get()                 # 获取每个子进程返回值 ,但是一旦加了get异步就会失效！！！
        # print(output)
    pool.close()
    pool.join()
    
    
