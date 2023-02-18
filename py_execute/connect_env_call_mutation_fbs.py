# -*- coding: utf-8 -*-
import subprocess,sys
sample_path = sys.argv[1]  # f"poll_pass.py {sample_path}",\ 加在annovar 前。
cmds = [f"split_add_index_chr.py {sample_path}",\
        f"call_mutation_fbs.py {sample_path}",\
        f"merge_and_filter_vcf.py {sample_path}",\
        f"annovar_vcf.py {sample_path}",\
        f"anno_filter.py {sample_path}",\
        f"process_anno_filter.py {sample_path}"]

for cmd in cmds:
    print(cmd," start! ")
    p = subprocess.Popen("python %s"%cmd,shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # 一下方式是实时查看紫禁城subprocess中输出，自己选择看不看。
    # while p.poll() is None:
    #     line = p.stdout.readline()
    #     line = line.strip()
    #     if line: print('Subprogram output: [{}]'.format(line))
    # p.wait()
    # 如果使用 subprocess.Popen，就不使用 Popen.wait()【可能死锁】，而使用 Popen.communicate() 来等待外部程序执行结束
    p.communicate()
    returncode = p.returncode
    print(returncode)
    if returncode == 0:
        print( cmd+"  successed!" )
    else:
        print(cmd+"  failed!")
        subprocess.call("pause",shell=True)  # 暂停
        exit(2)
        
        
        
