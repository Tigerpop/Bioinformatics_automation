# -*- coding: utf-8 -*-
import subprocess,re,os,sys

sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
ref_fasta = sys.argv[4]

def make_2bit_file():
    if not os.path.exists(f'/refhub/hg19/toolbox_and_RefFile/hg19.2bit'):
        print('hg19.2bit文件不存在，现在生成。')
        fatotwobit = '/opt/factera/faToTwoBit'
        parameters_pool = f' {ref_fasta} /refhub/hg19/toolbox_and_RefFile/hg19.2bit'
        cmd = f"{fatotwobit} \
        {parameters_pool}"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        if p.returncode != 0:
            exit(1)
    else:
        print(f'hg19.2bit文件已经存在')

def run_fectera():
    tmp_dir = f"{generate_location}/{sample_path}/"+"factera_generate"
    sample_dir = f"{generate_location}/{sample_path}"
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    
    tumor_bam = sample_dir+"/"+sample+".bwa_mem.bam"
    cmd1 = f"cp {tumor_bam} {tumor_bam}.bai {tmp_dir}/ "
    p = subprocess.Popen(cmd1,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(2)
    
    tumor_bam = f'{tmp_dir}'+"/"+sample+".bwa_mem.bam"
    factera_path = '/opt/factera'
    tool = 'factera.pl'
    parameters_pool = '/refhub/hg19/target/factera_special_bed/hg19.exons.bed \
                      /refhub/hg19/toolbox_and_RefFile/hg19.2bit'
    cmd = f"{factera_path}/{tool} \
          {tumor_bam} \
          {parameters_pool}"
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(2)
    
    cmd = f'rm -rf {tumor_bam} {tumor_bam}.bai '
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit(2)

if __name__=='__main__':
    make_2bit_file()
    run_fectera()
    # fectera 人工解读的逻辑是：看看 Break_support1 Break_support2 都要>50;
    # 报告中，用 max(Break_support1,Break_support2 )/Total_depth ,百分数保留两位小数作为 丰度值写入word报告，
    # 所以 BC17_word.py 中还需要改一点内容。
    
    
    # snpdelins call 突变 需要打一个补丁 ，用于方便人工标注时减少工作量.
    # 1、CLNSIG 临床重要性 有标注的 跳过；
    # 2、主要针对 CLNSIG 临床重要性 为 . 的部分，VAF list中的max值 > 3% ，且  CLNSIG 为 pathogenic/likey pathogenic。
    # 3、主要针对 CLNSIG 临床重要性 为 . 的部分，AAchange 字段中出现了 del 或者 ins ，AO 的list 只有唯一一个元素，且AO>50，DP>500 ，就都标记S1.
    
