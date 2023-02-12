# -*- coding: utf-8 -*-
import subprocess
cmds = ["pre_treatment.py",\
        "fastp_extract.py",\
        "bwa_mem.py",\
        "picard_markdup.py"]
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
    stdout,stderr = p.communicate()
    returncode = p.returncode
    print(returncode)
    if returncode == 0:
        print( cmd+"  successed!" )
    else:
        print(cmd+"  failed!")
        subprocess.call("pause",shell=True)  # 暂停
        exit(1) # 注意表示非正常结束一定要加一个非零参数。
    
# ####################################
# cmds=(
# umitools_extract.sh
# bwa_文件对比.sh
# umi_tools_dedup.sh
# )
# for cmd in ${cmds[@]}
# do
#   echo ${cmd}" start!"
#   bash ${cmd}
#   if [ $? -ne 0 ]; then
#     echo  ${cmd}" failed!"
#     exit 6
#   else
#     echo ${cmd}" succeed!"
#   fi
# done
