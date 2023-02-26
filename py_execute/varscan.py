# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys,time,datetime
from multiprocessing import Process,Pool
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg19_fasta = config['reference_document']['fasta']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

# 确定bed名。
sample_list = config['sample']['sample_list']
bed_list = config['bed']['bed_list']
sample_list = re.findall( r"\'(.*?)\'",sample_list)
bed_list = re.findall( r"\'(.*?)\'",bed_list)
bed_key = bed_list[sample_list.index(sample)].split(":")[0]

extract_mode = config['extract_mode']['choose']
if extract_mode == 'umi_mode':
    dedup_or_markdup = 'dedup'
elif extract_mode == 'fastp_mode':
    dedup_or_markdup = 'markdup'

# 针对 682 有Normal 的样本，我们在bed命名的时候就用 BCP_650-T、BCP_650-N 、NBC_650-T、NBC_650-N 加以区分。
bam = generate_location +"/" + sample_path + "/" + sample + f".{dedup_or_markdup}.bam"
tmp_dir = generate_location +"/" + sample_path
os.chdir(tmp_dir)
if bed_key[-1] == 'N': 
    if not os.path.exists(generate_location +"/" + sample_path + "/" + sample + ".normal.pileup"):
        cmd = f"samtools mpileup \
              -q 1 \
              -f {hg19_fasta} \
              {bam} \
              --output {tmp_dir}/{sample}.normal.pileup"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
    if not os.path.exists(f'{tmp_dir}/normal.pileup_have_build'):
        os.mkdir(f'{tmp_dir}/normal.pileup_have_build')
elif bed_key[-1] == 'T':
    if not os.path.exists(generate_location +"/" + sample_path + "/" + sample + ".tumor.pileup"):
        cmd = f"samtools mpileup \
              -q 1 \
              -f {hg19_fasta} \
              {bam} \
              --output {tmp_dir}/{sample}.tumor.pileup"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
    
    # 等待-N 产生了pileup 之后的文件，代表-N 的pileup文件已经彻底生成。
    # 轮询等待。
    sample_path_N,sample_N =  sample_path.replace('-T','-N'),sample.replace('-T','-N')
    normal_pileup = generate_location +"/" + sample_path_N + "/" + sample_N + ".normal.pileup"
    tumor_pileup = generate_location +"/" + sample_path + "/" + sample + ".tumor.pileup"
    normal_pileup_have_build = generate_location +"/" + sample_path_N + "/"+ 'normal.pileup_have_build'
    start_time = datetime.datetime.now()
    while not os.path.exists(normal_pileup_have_build):
        print("等待文件生成...")
        time.sleep(1)
    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    print(f"对应文件 normal_pileup 已生成，等待 {time_diff} 秒后退出程序...")

    if not os.path.exists(f"{tmp_dir}/{sample}.varscan.somatic.indel.vcf") \
        or not os.path.exists(f"{tmp_dir}/{sample}.varscan.somatic.snp.vcf"):
        cmd = f"varscan somatic \
                {normal_pileup} \
                {tumor_pileup} \
                {tmp_dir}/{sample}.varscan.somatic  \
                --output-vcf 1"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        if p.returncode != 0:
            exit(4)
    
    # cp varscan 结果 改名 注意，其实这里是没有进行污染库过滤的。
    indel = f'cp {tmp_dir}/{sample}.varscan.somatic.indel.vcf  {tmp_dir}/{sample}.pollpass.vcf'
    snp = f'cp {tmp_dir}/{sample}.varscan.somatic.snp.vcf  {tmp_dir}/{sample}.pollpass.vcf'
    for ccc in [indel,snp]:
        p = subprocess.Popen(ccc,shell=True)
        p.communicate()    

        cmds = [f"python ~/py_execute/annovar_vcf.py {sample_path}",\
                f"python ~/py_execute/anno_filter.py {sample_path}"]

        for cmd in cmds:
            print(cmd," start! ")
            p = subprocess.Popen(cmd,shell=True)
            p.communicate()
            returncode = p.returncode
            print(returncode)
            if returncode == 0:
                print( cmd+"  successed!" )
            else:
                print(cmd+"  failed!")
                subprocess.call("pause",shell=True)  # 暂停
                exit(2)

        indel_snp = re.findall(r'somatic.(.*?).vcf',ccc)[0]
        cmd = f'mv  {tmp_dir}/{sample}.filter.{hg_19_or_38}_multianno.txt  {tmp_dir}/{sample}.filter.{hg_19_or_38}_{indel_snp}.txt'
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()







