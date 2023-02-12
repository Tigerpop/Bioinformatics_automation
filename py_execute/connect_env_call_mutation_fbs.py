# -*- coding: utf-8 -*-
import subprocess
cmds = ["split_add_index_chr.py",\
        "call_mutation_fbs.py",\
        "merge_and_filter_vcf.py",\
        "annovar_vcf.py",\
        "anno_filter.py",\
        "process_anno_filter.py"]

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
        
        
        
