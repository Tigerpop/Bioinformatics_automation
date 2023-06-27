#coding=utf8

# 把上面代码新建 multiprocessing.Queue() 加入参数，完成子进程内容向父进程的自定义代码回馈。
# 在报错表中方便检查问题。
import multiprocessing, subprocess,sys,os,re,time

class MyException(Exception):
    pass

# queue_0通信传递正确输出，queue_1传递错误输出内容，queue_2传递自定义的错误内容,command 是个dict。后期我进程了修改，queue中只有queue_2真正被用到了。
# 注意，我这里的定义中，有queue_1传递错误输出内容 不代表流程错误，queue_2传递自定义的错误内容 才是真的错误。
def run_command(command,command_key,log_path,queue_0,queue_1,queue_2): 
    try:
        # raise MyException("Something went wrong") # 主动抛出异常测试一下。s
        # 执行命令
        process = subprocess.Popen(command[command_key], shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 读取标准输出和标准错误输出，并将它们放入队列中
        have_err_or_not = False
        # 如果子进程的输出太多，output = process.stdout.readline() 这一步可能出现缓存区溢出。所以换下面另一种写法(不能实时读取，子进程运行完了写入。)；
        # 像下面这种 通信方式 能用但是不推荐，虽然灵活性高，但是有溢出风险，而且不容易排错。
        # 只有自定义的 通信 用 非阻塞的 ，因为它一般会比较小，不会 缓存溢出。
        # with open(f'{command_key}_normal.log', 'w') as f0,open(f'{command_key}_debug.log', 'w') as f1:
            # while True:
            #     output = process.stdout.readline() 
            #     error = process.stderr.readline()
            #     if output == b'' and process.poll() is not None:
            #         if error == b'' and process.poll() is not None:
            #             break
            #     if output:
            #         # queue_0.put(output.decode('utf-8'))
            #         sys.stdout.flush() # 记得清空一下缓存，不然可能被子进程输出撑爆。
            #         # 同样 如果子进程输出太多，multiprocessing.Queue() 可能会被撑爆。这可能会导致程序卡住。我们试着把它直接写进文件。
            #         f0.write(f"{output.decode('utf-8')}")
            #     if error:
            #          # have_err_or_not = True
            #          # queue_1.put(error.decode('utf-8'))# +'子进程的子进程异常或者调试信息,')
            #          sys.stderr.flush() # 记得清空一下缓存，不然可能被子进程输出撑爆。
            #          # 同理，如果子进程输出太多，multiprocessing.Queue() 可能会被撑爆。这可能会导致程序卡住。
            #          f1.write(f"{error.decode('utf-8')}")
        output, error = process.communicate()   # 阻塞
        with open(f'{log_path}/{command_key}_normal.log', 'w') as f0,open(f'{log_path}/{command_key}_debug.log', 'w') as f1:
            f0.write(f"{output.decode('utf-8')}")
            f1.write(f"{error.decode('utf-8')}")
        # queue_2.put(error)
        returncode = process.returncode # 用 process.returncode 来判断是不是真的正确输出，子进程exit(非0)它就接到一个非0值，调试信息存起来就行。
        if returncode == 0:
            print( command_key +"  successed!" )
        else:
            have_err_or_not = True
            queue_2.put(command_key+' 步骤发生了错误,')
            print(command_key +"  failed!")
            exit(1) # 注意表示非正常结束一定要加一个非零参数。
    except Exception as e:
        have_err_or_not = True
        queue_2.put(command_key+' 步骤发生了错误,')
        queue_1.put(str(e))# +'子进程异常')
        exit(1)
        

if __name__ == '__main__':
    # sample = '2022WSSW005607-T'
    sample_monitor = '/fastq_data'
    sample = sys.argv[1]  # '2022WSSW005608-T'
    sample_path = sample # sample.replace('-T','').replace('-N','')+'/'+sample  # 2022WSSW005608/2022WSSW005608-T
    generate_location = '/home/chenyushao/py_streaming_generate'
    log_path = f"{generate_location}/{sample_path}/log" # 'py_streaming_execute/log'
    ref_fasta = '/refhub/hg19/fa/ucsc.hg19.fasta'
    bed = '/refhub/hg19/target/Q120T/Q80.raw.hg19.bed'
    bed_key = 'Q120B'
    bed_1p19q = '/refhub/hg19/target/Q120B/1p19qtest2.bed'
    human_genome_index = '/refhub/hg19/human_genome_index/gatk_hg19'
    fa_gz_1 = str(f'/fastq_data/{sample_path}/{sample}_1.fq.gz')
    fa_gz_2 = str(f'/fastq_data/{sample_path}/{sample}_2.fq.gz')
    out_extract_1 = f"{generate_location}/{sample_path}/{sample}_1.extract.fq.gz"
    out_extract_2 = f"{generate_location}/{sample_path}/{sample}_2.extract.fq.gz"
    unsort_bam = f'{generate_location}/{sample_path}/{sample}.unsort.bam'
    sorted_bam = f'{generate_location}/{sample_path}/{sample}.bwa_mem.bam'
    sorted_bam_bai = f'{generate_location}/{sample_path}/{sample}.bwa_mem.bam.bai'
    markdup_bam = f'{generate_location}/{sample_path}/{sample}.markdup.bam'
    markdup_bam_bai = f'{generate_location}/{sample_path}/{sample}.markdup.bam.bai'
    merge_vcf = f'{generate_location}/{sample_path}/{sample}.merge.vcf'
    poll_pass_vcf = f'{generate_location}/{sample_path}/{sample}.pollpass.vcf'
    annovar_out_prefix = f'{generate_location}/{sample_path}/{sample}.anno'
    annover_txt = f'{generate_location}/{sample_path}/{sample}.anno.hg19_multianno.txt'
    process_anno_filter_txt = f'{generate_location}/{sample_path}/{sample}.process.hg19_multiprocess.txt'
    
    # 主动抛出错误测试。
    # aaa
    
    # 这里有问题。os 是典型的非阻塞模块，可能导致 主进程后面都开始运行了，这里的os方法还运行打一半。
    # 给原始文件改名E150000469_L01_2022WSSW003294-T_2.fq.gz -> 2022WSSW003294-T_2.fq.gz,睿明的样本把 _raw 去掉。
    # 要保证 下面运行完毕以后，再运行主进程的后续内容。
    name_list = os.listdir(f'{sample_monitor}/{sample_path}/')
    for name in name_list:
        if name[0] == 'E':
            newname = "_".join(name.split("_")[-2:])
            os.rename(f'{sample_monitor}/{sample_path}/{name}',f'{sample_monitor}/{sample_path}/{newname}')
        if re.findall('_raw_',name)!=[]:
            newname = name.replace('_raw_1','_1').replace('_raw_2','_2')
            os.rename(f'{sample_monitor}/{sample_path}/{name}',f'{sample_monitor}/{sample_path}/{newname}')

    if not os.path.exists(log_path):
        os.makedirs(log_path)
    # cmd = 'name_list=$(ls ${sample_monitor}/${sample_path}/)\
    #         for name in $name_list\
    #         do\
    #             if [ ${name:0:1} == "E" ]\
    #             then\
    #                 newname=$(echo $name | awk -F "_" '{print "_"$(NF-1)"_"$NF}')\
    #                 mv ${sample_monitor}/${sample_path}/${name} ${sample_monitor}/${sample_path}/${newname}\
    #             fi\
    #         done\
    #         for name in $name_list\
    #         do\
    #             newname=$(echo $name | sed 's/_raw_1/_1/g' | sed 's/_raw_2/_2/g')\
    #             mv ${sample_monitor}/${sample_path}/${name} ${sample_monitor}/${sample_path}/${newname}\
    #         done\
    #         if [ ! -d "$log_path" ]\
    #         then\
    #             mkdir -p "$log_path"\
    #         fi'
    # process = subprocess.Popen(command[command_key], shell=True, executable='/bin/bash')
    # process.communicate() 
    
    # 注意： 
    # 其实fastp.log 内是 错误才会输入进去，但是我们需要这个fastp.log 文件，就没有把它当错误处理。
    # 也就是说在shell命令中如果重定向 > 进了一个文件夹，进程通信就不能再得到正确或者错误的返回值了。
    # 也就是说 shell中 重定向 > 之后 其实监控不到 fastp 的报错，需要自己去 fastp.log 文件中自己去读。
    # 这是因为 ，有时候在程序执行时会将一些警告信息或者额外的调试信息输出到标准错误流（stderr）中，
    # 这些信息通常不是致命的错误，而是有助于理解程序的运行过程或者定位问题。bwa 也一样有这样的情况。
    # 可以尝试将其重定向到文件或者将其禁止输出。
    # 解决方法:
    # （生信工具编写者总是喜欢把 “调试内容”写进“标准错误输出err”中）
    # 用 process.returncode 来判断是不是真的正确输出，调试信息存起来就行。
    # time.sleep(60)
    command = {}  
    command['fastp_extract'] = \
              f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
              conda activate no_umitools_py  && \
              fastp -i {fa_gz_1} \
                  -o {out_extract_1} \
                  -I {fa_gz_2} \
                  -O {out_extract_2} \
                  -w 8 \
                  -l 30 && \
              conda deactivate "
    command['extract_qc'] = \
              f"python extract_qc.py {sample} {log_path} {generate_location} "
    command['bwa_mapping'] = \
              f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
              conda activate no_umitools_py  && \
              bwa mem -t 16 \
              -Y \
              {human_genome_index} \
              {out_extract_1} \
              {out_extract_2} \
              -o {unsort_bam} && \
              samtools sort -@ 10 -o {sorted_bam} {unsort_bam} && \
              rm -rf {unsort_bam} && \
              samtools index -@ 10 {sorted_bam} {sorted_bam_bai} && \
              conda deactivate"
    command['picard_markdup'] = \
              f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
              conda activate no_umitools_py  && \
              picard MarkDuplicates \
              I={sorted_bam} \
              O={markdup_bam} \
              M=sample_name.markdup_metrics.txt && \
              samtools index -@ 10 {markdup_bam} {markdup_bam_bai} && \
              conda deactivate"
    command['dedup_markdup_pc'] = \
              f"python dedup_markdup_pc.py  {sample} {log_path} {sample_path} {generate_location} {bed}"
    command['split_callMutation_merge'] = \
              f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
              conda activate call_mutation_fbs && \
              python split_callMutation_merge.py {sample} {sample_path} {log_path} {generate_location} {ref_fasta} && \
              conda deactivate"
    command['pollution_filter'] = \
              f"python pollution_filter.py {sample} {sample_path} {generate_location} {bed_key}"
    command['annovar'] = \
              f"/opt/annovar/table_annovar.pl \
              {poll_pass_vcf} \
              -out {annovar_out_prefix} \
              /refhub/hg19/toolbox_and_RefFile \
                  	 -buildver hg19 \
                  	-remove \
                  	-protocol smallrefGene,cytoBand,clinvar_20220320,avsnp150,dbnsfp42c \
                  	-operation g,r,f,f,f \
                  	-nastring . \
                  	-vcfinput \
                  	-polish"
    command['process_anno_filter'] = \
              f"python process_anno_filter.py {sample} {sample_path} {generate_location} {annover_txt}"
    command['panelcn_map_bam'] = \
              f"/usr/bin/Rscript panelcn.R {sample} {sample_path} {generate_location} {bed_key} "
    command['decon_map_bam'] = \
              f"python decon_map_bam.py {sample} {sample_path} {generate_location} {bed_key} {ref_fasta} "
    command['factera'] = \
              f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
              conda activate cnv_factera_delly  && \
              python factera.py {sample} {sample_path} {generate_location} {ref_fasta} && \
              conda deactivate"
    command['chemo'] = \
              f"python chemo.py {sample} {sample_path} {generate_location}"
    command['msi'] = \
              f'folder="{generate_location}/{sample_path}/msi_generate" \n \
              if [ ! -d "$folder" ]; then \n \
              mkdir "$folder" \n \
              fi && \
              python msi_detect.py --tool msisensor-pro --gene {bed_key} \
              {generate_location}/{sample_path}/{sample}.markdup.bam \
              {generate_location}/{sample_path}/msi_generate/msi_result'
    command['test_1p19q'] = \
              f"python test_1p19q.py {sample} {sample_path} {generate_location} {bed_1p19q} {log_path} "
    command['collect'] = \
              f"python collect.py {sample} {sample_path} {log_path} {generate_location} {bed_key} {sample_monitor} {bed}"
    # 流程list
    execution_order_list = ['collect']#['fastp_extract','extract_qc','bwa_mapping','picard_markdup','dedup_markdup_pc','split_callMutation_merge','pollution_filter','annovar','process_anno_filter','panelcn_map_bam','factera','chemo','msi','collect']
    for command_key in execution_order_list:
        queue_0,queue_1,queue_2 = multiprocessing.Queue(),multiprocessing.Queue(),multiprocessing.Queue()
        p = multiprocessing.Process(target=run_command, args=(command,command_key,log_path,queue_0,queue_1,queue_2)) # command以dict形式传递，用到的是value，key用于自定义输出。
        p.start()
        p.join()
        # 写标准输出流、写标准错误流或者调试内容，打印自定义输出内容。
        # with open(f'{command_key}_normal.log', 'w') as f:
        #     while not queue_0.empty():
        #         f.write(f'{queue_0.get()}')
        # with open(f'{command_key}_debug.log', 'w') as f:
        #     while not queue_1.empty():
        #         f.write(f'{queue_1.get()}')
        if not queue_2.empty():                            # 出现自定义错误就，真的停下 流程,记得让 exit值变非零,在父进程识别报错。
            while not queue_2.empty():
                custom_output = queue_2.get()
                # print(custom_output,'这是自定义输出\n',end='')
                sys.stderr.write(f'{custom_output}\n')
            # break
            exit(1)
 
