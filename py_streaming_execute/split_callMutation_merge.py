# -*- coding: utf-8 -*-
import multiprocessing, subprocess, re, os, sys, shutil
from multiprocessing import Process, Pool

sample = sys.argv[1]  # 第一个参数
# log_path = sys.argv[2]
sample_path = sys.argv[2]
log_path = sys.argv[3]
generate_location = sys.argv[4]
ref_fasta = sys.argv[5]

file_path = generate_location + "/" + sample_path
chr_split = file_path + "/" + "chr_split"
split_vcf = file_path + "/" + "split_vcf"


# apply_async 开多进程 调用的方法最好还是写在模块里class外。
def shell_func_0(i, queue, ref_fasta=ref_fasta, chr_split=chr_split, sample=sample, split_vcf=split_vcf):
    print('进入shell_func_0方法运行。')
    if i == "7_replenish":  # 对于补充处理的关键区域单独call,并且缩小颗粒度。
        cmd = f"freebayes -f {ref_fasta} --min-alternate-count=5 \
        --min-alternate-fraction=0.001  \
        --min-coverage 20 \
        --region chr7:55241614-55259567 \
        {chr_split}/{sample}.markdup.REF_chr{i}.bam > {split_vcf}/{sample}.markdup.REF_chr{i}.vcf "
        # cmd = cmd.format(fasta=fasta,bam_path=bam_path,sample=sample,output_path=output_path,i=i)
        # subprocess.call(cmd,shell=True)
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        out, err = p.communicate()
        with open(f'{log_path}/callMutation_normal.log', 'a+') as f0, open(f'{log_path}/callMutation_debug.log',
                                                                           'a+') as f1:
            if out is None:
                f0.write(f"")
            else:
                f0.write(f"{out.decode('utf-8')}")
            if err is None:
                f1.write(f"")
            else:
                f1.write(f"{err.decode('utf-8')}")
        # queue.put(err.decode('utf-8'))
        # queue.put('进入第一个call')
        if p.returncode != 0:
            exit(2)
    else:
        cmd = f"freebayes -f {ref_fasta} --min-alternate-count=5 \
        --min-alternate-fraction=0.01  \
        --min-coverage 20 \
        {chr_split}/{sample}.markdup.REF_chr{i}.bam > {split_vcf}/{sample}.markdup.REF_chr{i}.vcf "
        # cmd = cmd.format(fasta=fasta,bam_path=bam_path,sample=sample,output_path=output_path,i=i)
        # subprocess.call(cmd,shell=True)
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        out, err = p.communicate()
        with open(f'{log_path}/callMutation_normal.log', 'a+') as f0, open(f'{log_path}/callMutation_debug.log',
                                                                           'a+') as f1:
            if out is None:
                f0.write(f"")
            else:
                f0.write(f"{out.decode('utf-8')}")
            if err is None:
                f1.write(f"")
            else:
                f1.write(f"{err.decode('utf-8')}")
        # queue.put(err.decode('utf-8'))
        # queue.put('进入第二个call')
        if p.returncode != 0:
            exit(2)


def shell_func_1(i, queue, sample=sample):
    cmd1 = f"bgzip -c {sample}.markdup.REF_chr{i}.vcf > {sample}.markdup.REF_chr{i}.vcf.gz"
    cmd2 = f"bcftools index -t {sample}.markdup.REF_chr{i}.vcf.gz"
    # cmd1,cmd2 = cmd1.format(sample=sample,i=i),cmd2.format(sample=sample,i=i)
    p = subprocess.Popen(cmd1, shell=True, stderr=subprocess.PIPE)
    out, err = p.communicate()
    queue.put(err.decode('utf-8'))
    if p.returncode != 0:
        exit(3)
    p = subprocess.Popen(cmd2, shell=True, stderr=subprocess.PIPE)
    out, err = p.communicate()
    queue.put(err.decode('utf-8'))
    if p.returncode != 0:
        exit(3)


class split_callMutation_merge():
    def __init__(self, sample, sample_path, generate_location, ref_fasta):
        self.sample, self.sample_path, self.generate_location, self.ref_fasta = sample, sample_path, generate_location, ref_fasta
        self.file_path = generate_location + "/" + sample_path
        self.chr_split = self.file_path + "/" + "chr_split"
        self.split_vcf = self.file_path + "/" + "split_vcf"
        self.test_list = [i for i in range(1, 23)]
        self.test_list.extend(["X", "Y"]) # 在这里决定是否打开 细粒度的call突变开关。["X", "Y", "7_replenish"]

    def split(self):
        os.chdir(self.file_path)
        if not os.path.exists(self.chr_split):
            os.makedirs(self.chr_split)
        # os.system(f"cp {self.file_path}/{self.sample}.markdup.bam ./chr_split/") # 这种写法有隐患。
        cmd = f"cp {self.file_path}/{self.sample}.markdup.bam ./chr_split/"
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()
        os.chdir(self.chr_split)
        cmd = f"bamtools split -in {self.chr_split}/{self.sample}.markdup.bam  -reference"
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            sys.stderr.write(out.decode('utf-8'))  # 子进程的报错 写入标准错误输出流，让父进程识别。但是需要注意子进程的报错可能是输出在标准输出流中而不是错误流中。
            sys.stderr.write(err.decode('utf-8'))
            exit(1)
        chr_list = [i for i in range(1, 23)]
        chr_list.extend(['X', 'Y'])
        for i in chr_list:
            cmd = f"samtools index -@ 10 {self.chr_split}/{self.sample}.markdup.REF_chr{i}.bam {self.chr_split}/{self.sample}.markdup.REF_chr{i}.bam.bai"
            p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                sys.stderr.write(out.decode('utf-8'))
                sys.stderr.write(err.decode('utf-8'))
                exit(1)
        cmd = f'rm -rf {self.chr_split}/{self.sample}.markdup.bam'
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()
        if p.returncode != 0:
            sys.stderr.write(out.decode('utf-8'))
            sys.stderr.write(err.decode('utf-8'))
            exit(1)

    # 注意：有 pool.apply_async 开多进程的情况下实现父子进程通信。
    # 有点不一样。用的是multiprocessing.Manager().Queue()
    # 而且 需要apply_async的返回值，在循环后阻塞！！
    def callMutation(self):
        os.chdir(file_path)
        if not os.path.exists("split_vcf"):
            os.makedirs("split_vcf")
        os.chdir("chr_split")
        shutil.copyfile(f'{chr_split}/{sample}.markdup.REF_chr7.bam',
                        f'{chr_split}/{sample}.markdup.REF_chr7_replenish.bam')
        shutil.copyfile(f'{chr_split}/{sample}.markdup.REF_chr7.bam.bai',
                        f'{chr_split}/{sample}.markdup.REF_chr7_replenish.bam.bai')
        test_list = self.test_list
        pool = Pool(processes=10)
        queue = multiprocessing.Manager().Queue()
        for index, i in enumerate(test_list):
            result = pool.apply_async(shell_func_0, (i, queue))  # 这一步似乎已经 截获了子进程的输出。无需再用进程通信队列来实现通信。
        result.get()  # 阻塞
        try:
            if result.get() is None:
                pass
        except AttributeError:
            pass
        # result = pool.apply_async(shell_func,(1,queue))
        # print(result.get()) # 阻塞
        pool.close()
        pool.join()
        while not queue.empty():  # 子进程返回的值，直接输出就在stdout中了，再上一层就是正常输出日志里。这里可以改道stderr中。
            # print(queue.get())
            sys.stderr.write(f"{queue.get()}\n")

    def merge(self):
        os.chdir(self.split_vcf)
        test_list = self.test_list
        pool = Pool(processes=10)
        queue = multiprocessing.Manager().Queue()
        for i in test_list:
            result = pool.apply_async(shell_func_1, (i, queue))
        print(result.get())  # 阻塞
        pool.close()
        pool.join()
        while not queue.empty():  # 子进程返回的值，直接输出就在stdout中了，再上一层就是正常输出日志里。这里可以改道stderr中。
            print(queue.get())
        if "7_replenish" in self.test_list:
            cmd = f"bcftools merge -m snps -f PASS,. --force-samples \
            {sample}.markdup.REF_chr1.vcf.gz \
            {sample}.markdup.REF_chr2.vcf.gz \
            {sample}.markdup.REF_chr3.vcf.gz \
            {sample}.markdup.REF_chr4.vcf.gz \
            {sample}.markdup.REF_chr5.vcf.gz \
            {sample}.markdup.REF_chr6.vcf.gz \
            {sample}.markdup.REF_chr7.vcf.gz \
            {sample}.markdup.REF_chr8.vcf.gz \
            {sample}.markdup.REF_chr9.vcf.gz \
            {sample}.markdup.REF_chr10.vcf.gz \
            {sample}.markdup.REF_chr11.vcf.gz \
            {sample}.markdup.REF_chr12.vcf.gz \
            {sample}.markdup.REF_chr13.vcf.gz \
            {sample}.markdup.REF_chr14.vcf.gz \
            {sample}.markdup.REF_chr15.vcf.gz \
            {sample}.markdup.REF_chr16.vcf.gz \
            {sample}.markdup.REF_chr17.vcf.gz \
            {sample}.markdup.REF_chr18.vcf.gz \
            {sample}.markdup.REF_chr19.vcf.gz \
            {sample}.markdup.REF_chr20.vcf.gz \
            {sample}.markdup.REF_chr21.vcf.gz \
            {sample}.markdup.REF_chr22.vcf.gz \
            {sample}.markdup.REF_chrX.vcf.gz \
            {sample}.markdup.REF_chrY.vcf.gz \
            {sample}.markdup.REF_chr7_replenish.vcf.gz \
            > {sample}.merge.vcf"
        else:
            cmd = f"bcftools merge -m snps -f PASS,. --force-samples \
            {sample}.markdup.REF_chr1.vcf.gz \
            {sample}.markdup.REF_chr2.vcf.gz \
            {sample}.markdup.REF_chr3.vcf.gz \
            {sample}.markdup.REF_chr4.vcf.gz \
            {sample}.markdup.REF_chr5.vcf.gz \
            {sample}.markdup.REF_chr6.vcf.gz \
            {sample}.markdup.REF_chr7.vcf.gz \
            {sample}.markdup.REF_chr8.vcf.gz \
            {sample}.markdup.REF_chr9.vcf.gz \
            {sample}.markdup.REF_chr10.vcf.gz \
            {sample}.markdup.REF_chr11.vcf.gz \
            {sample}.markdup.REF_chr12.vcf.gz \
            {sample}.markdup.REF_chr13.vcf.gz \
            {sample}.markdup.REF_chr14.vcf.gz \
            {sample}.markdup.REF_chr15.vcf.gz \
            {sample}.markdup.REF_chr16.vcf.gz \
            {sample}.markdup.REF_chr17.vcf.gz \
            {sample}.markdup.REF_chr18.vcf.gz \
            {sample}.markdup.REF_chr19.vcf.gz \
            {sample}.markdup.REF_chr20.vcf.gz \
            {sample}.markdup.REF_chr21.vcf.gz \
            {sample}.markdup.REF_chr22.vcf.gz \
            {sample}.markdup.REF_chrX.vcf.gz \
            {sample}.markdup.REF_chrY.vcf.gz \
            > {sample}.merge.vcf"
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        if p.returncode != 0:
            exit(3)
        cmd = f"cp {self.split_vcf}/{self.sample}.merge.vcf {self.file_path}/"
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        if p.returncode != 0:
            exit(3)


if __name__ == '__main__':
    scm = split_callMutation_merge(sample, sample_path, generate_location, ref_fasta)
    scm.split()
    scm.callMutation()
    scm.merge()





