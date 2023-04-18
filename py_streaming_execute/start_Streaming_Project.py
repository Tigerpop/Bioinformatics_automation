# -*- coding: utf-8 -*-
import time,os,random,subprocess
import queue
from multiprocessing import Pool
from datetime import date

def worker(sample):
    # print(f"start {sample},process is {os.getpid()}")
    # time.sleep(random.randint(2,100))
    # print(f"end {sample},process is {os.getpid()}")
    try:
        cmd = f'python BC17.py {sample}'
        p = subprocess.Popen(cmd,shell=True, close_fds=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        # # 一下方式是实时查看紫禁城subprocess中输出，自己选择看不看。
        # while p.poll() is None:
        #     line = p.stdout.readline()
        #     line = line.strip()
        #     if line: print('Subprogram output: [{}]'.format(line))
        
        # p.wait()
        # 如果使用 subprocess.Popen，就不使用 Popen.wait()【可能死锁】，而使用 Popen.communicate() 来等待外部程序执行结束
        stdout,stderr = p.communicate()
        returncode = p.returncode
        if returncode == 0:
            print( cmd+"  successed!" )
        else:
            print('look here!!! ',cmd+"  failed!")
            # subprocess.call("pause",shell=True)  # 暂停
            exit(100)  # 在 try 中使用 exit 会退出程序，在退出程序之前会引发一个SystemExit异常，交给except捕获，等except下的代码运行完 再 退出此进程。
    except:
        Time = date.today().strftime("%Y-%m-%d %H:%M")
        with open('/home/chenyushao/py_streaming_generate/need_manual_processing.txt','a+')as log:
            log.write('执行出错，需要手工调整: '+sample+f' {Time}'+'\n'+stderr.decode('utf-8')+"------------------------------\n\n")        
        print("运行：",cmd,"出现问题。")
    
    
# 维护文件夹，一定不能把 “加载文件进文件夹”和“定时扫描” 分开独立写，
# 因为：可能出现这边流程已经开始了，那边光有个文件名，文件还没有加载完，
# 所以，要把 “加载文件进文件夹” 写进 “定时扫描”维护文件夹流程内部！！！
def Output_New_File_and_push_to_pool(path_to_watch,pool): # path_to_watch 是被监控文件夹，pool是文件最终进入的进程池。
    # path_to_watch = "/Users/chenyushao/Desktop/python_draft/biotools_draft/Scan_folder"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:
        time.sleep(5)
        
        # 加载（移动）文件进文件夹，写在这。读未读。
        time.sleep(5)
        
        after = dict([(f, None) for f in os.listdir(path_to_watch)])  # 列表推导的方式 对 dict 赋值。f 是文件名,也可能是文件夹名.
        added = [f for f in after if not f in before]  # [2088,2883,2458] 带 T N 的是它的子元素。
        if added:   
            # print(added)
            added_sub = []
            [ added_sub.extend(os.listdir(f"{path_to_watch}/{f}")) for f in added]
            added_sub_str = ",".join(added_sub)
            # print(added_sub_str)
            cmd = f'python make_received_csv.py {added_sub_str} > /home/chenyushao/py_streaming_generate/log/make_received.log 2>&1'
            p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            p.communicate()
            

            print("Added: ", added_sub_str)
            for f in added_sub:             #  都去 pool前面排队。因为没有 pool.close() 告诉进程池不再接收新任务，所以队列越排越长。但是进程池不会出现空闲。
                pool.apply_async(worker, args=(f,)) 
        before = after


def main():
    pool = Pool(4)

    # 识别出文件夹内新来的文件，并扔进进程池排队的序列中。
    Output_New_File_and_push_to_pool(path_to_watch="/home/chenyushao/py_streaming_generate/monitor", pool=pool)


if __name__ == '__main__':
    main()
