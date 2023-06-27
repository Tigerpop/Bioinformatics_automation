# -*- coding: utf-8 -*-
import time,os,random,subprocess
import queue,chardet
import pandas as pd 
from multiprocessing import Pool
from datetime import date,datetime

def worker(sample,panel):
    # print(f"start {sample},process is {os.getpid()}")
    # time.sleep(random.randint(2,100))
    # print(f"end {sample},process is {os.getpid()}")
    try:
        print('运行的启动时间是： ',time.time())
        def choose_bed(panel: str) -> str:  
            options = {
                'BC17T': f'python BC17T.py {sample}', 'BC17B': f'python BC17B.py {sample}', 
                'Q110T': f'python Q120T.py {sample}','Q80T': f'python Q120T.py {sample}','Q120T': f'python Q120T.py {sample}','Q110B': f'python Q120B.py {sample}','Q80B': f'python Q120B.py {sample}','Q120B': f'python Q120B.py {sample}',
                'SD160T': f'python SD160T.py {sample}', 'SD160B': f'python SD160B.py {sample}', 
                'BCP650': f'python BCP650.py {sample}','NBC650': f'python NBC650.py {sample}',
                'G2T':f'python comprehensive_bed.py {sample} {panel}','G2B':f'python comprehensive_bed.py {sample} {panel}',
                'BRCAT':f'python comprehensive_bed.py {sample} {panel}','BRCAG':f'python comprehensive_bed.py {sample} {panel}',
                'SLC17T':f'python comprehensive_bed.py {sample} {panel}','SLC17B':f'python comprehensive_bed.py {sample} {panel}',
                'SLC80T':f'python comprehensive_bed.py {sample} {panel}','SLC80B':f'python comprehensive_bed.py {sample} {panel}'
            }
            return options.get(panel, f'echo no_this_panel {panel}')
        cmd = choose_bed(panel)
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
        # Time = date.today().strftime("%Y-%m-%d %H:%M")
        Time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open('/home/chenyushao/py_streaming_generate/need_manual_processing.txt','a+')as log:
            log.write('执行出错，需要手工调整: '+sample+'  '+panel+f' {Time}'+'\n'+stderr.decode('utf-8')+"------------------------------\n\n")        
        print("运行：",cmd,"出现问题。")
    
    
# 维护文件夹，一定不能把 “加载文件进文件夹”和“定时扫描” 分开独立写，
# 因为：可能出现这边流程已经开始了，那边光有个文件名，文件还没有加载完，
# 所以，要把 “加载文件进文件夹” 写进 “定时扫描”维护文件夹流程内部！！！
def Output_New_File_and_push_to_pool(path_to_watch,pool): # path_to_watch 是被监控文件夹，pool是文件最终进入的进程池。
    # path_to_watch = "/Users/chenyushao/Desktop/python_draft/biotools_draft/Scan_folder"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:
        start_time = time.time()
        time.sleep(60)
        
        # 加载（移动）文件进文件夹，写在这。读未读。
        # time.sleep(5)
        if os.path.exists(f'/received/received_new.csv') or os.path.exists(f'/received/received_vip.csv'):
            cmd = f'python download_data.py '
            p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            p.communicate()
            returncode = p.returncode
            print('读文件下载的完成时间是： ',time.time())
            if returncode !=0:
                if os.path.exists(f'/received/received_new.csv'):
                    os.rename(f'/received/received_new.csv',f'/received/received_new_err.csv')
                if os.path.exists(f'/received/received_vip.csv'):
                    os.rename(f'/received/received_vip.csv',f'/received/received_vip_err.csv')
                print('请检查输入的received_new received_VIP 表。')
                # exit(100)
                
        after = dict([(f, None) for f in os.listdir(path_to_watch)])  # 列表推导的方式 对 dict 赋值。f 是文件名,也可能是文件夹名.
        added = [f for f in after if not f in before]  # [2088-T,2883-T,2458-T] 。
        # 为应对 同名元素传入，我们会在 mv 文件进被监控文件夹时，把旧的加上 _before 。
        # 首先要从added中排除有‘_before’词缀的
        # 再从after中找 _before 词缀前的 原版元素。
        # 判断 _before 词缀前的 原版元素文件创建时间 是否离当前时刻在一个扫描周期内。
        # 如果在一个周期内，就把 _before 词缀前的 原版元素 添加进added，否则视为旧有元素。
        added = [x for x in added if '_before' not in x]
        have_before_pre = list(set([x.split('_before')[0] for x in after if '_before' in x]))
        new_time = time.time()
        have_before_pre_newAdd = \
                [x for x in  have_before_pre if (new_time-os.path.getctime(f'{path_to_watch}/{x}'))<new_time-start_time ]
        added.extend(have_before_pre_newAdd)
        # print('added: ',added)
        # print('have_before_pre_newAdd: ',have_before_pre_newAdd)
        if added:   
            # print(added)
            added_str = ",".join(added)
            # print(added_sub_str)
            # 这一步，要按照 老板意思来，老板并不能很好的理解流程规则，但是老板的意思从根本上来说就是更喜欢读写received表，而不是“项目表”，
            # 那就让老板读写 另外一个长得和 received 表格式一样的表即可。流程可以不变。如果真的后台在写表，手工又写表，可能会带来额外锁的问题，没必要弄复杂。
            # 下面在 python make_received_csv.py 之前，需要补充一个 填充项目表的 类似 received 格式的表格，完成对其它家数据的补充。
            # cmd = f'python make_received_csv.py {added_sub_str} > /home/chenyushao/py_streaming_generate/log/make_received.log 2>&1'
            # p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            # p.communicate()

            print("Added: ", added_str)
            for f in added:             #  都去 pool前面排队。因为没有 pool.close() 告诉进程池不再接收新任务，所以队列越排越长。但是进程池不会出现空闲。
                # 后续这一步中识别panel. 备加入。
                with open('/received/main/received.csv', 'rb') as f0: # 确认编码类型。
                    encoding_stype = chardet.detect(f0.read())
                df = pd.read_csv('/received/main/received.csv',sep=',',header=1,encoding=encoding_stype['encoding'])
                # print(df[df['样本编号*']==f])
                panel = df[df['样本编号*']==f]['探针*'].iloc[0]
                pool.apply_async(worker, args=(f,panel,)) 
        before = after


def main():
    pool = Pool(4)

    # 识别出文件夹内新来的文件，并扔进进程池排队的序列中。
    Output_New_File_and_push_to_pool(path_to_watch="/home/chenyushao/py_streaming_generate/monitor", pool=pool)


if __name__ == '__main__':
    main()
