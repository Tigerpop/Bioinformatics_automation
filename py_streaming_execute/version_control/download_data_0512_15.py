# -*- coding: utf-8 -*-
import time, os, random, subprocess, sys, re, shutil
import queue, chardet
from multiprocessing import Pool
from datetime import date, datetime
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


# 大体思路 ，每家的文件先下载在不同的文件夹下，校验完毕之后再改名 移动到 被监控的文件夹中。
# 0、读received文件一行一行的下载
# 1、先 ossutil ls 源文件 -c  不同家配置文件 > temp.txt
# 2、从temp.txt 中把 MD5文件，和 RawData... 递归下载，注意，是相对路径。
# 3、在MD5目录校验MD5值，看是否每行 OK 结尾。
# 4、放进被fastq或者监控的文件夹，或者VIP手动扔的文件夹。


def download_checkMD5(oss, sample):
    # 读received文件一行一行的下载
    oss_body = oss.split('/')[-1].strip()
    oss_enterprise = oss.split('/')[2].strip()
    print('oss_body is :', oss_body, '\noss_enterprise is :', oss_enterprise)
    temp_download = '/home/chenyushao/py_streaming_generate/temp_download'
    print('temp_download is : ', temp_download)

    # cmd_0 = 'echo 未输入正确公司'
    if oss_enterprise == 'qgq2021-1042':
        config = f'/refhub/osskey/qgq2021-1042.ossutilconfig'
    elif oss_enterprise == 'sh-kefu-ruimingbio':
        config = f'/refhub/osskey/sh-kefu-ruimingbio.ossutilconfig'
    elif oss_enterprise == 'rx2020-1027':
        config = f'/refhub/osskey/rx2020-1027.ossutilconfig'
    elif oss_enterprise == 'jm2020-1000':
        config = f'/refhub/osskey/jm2020-1000.ossutilconfig'
    elif oss_enterprise == 'rm2021-1051':
        config = f'/refhub/osskey/rm2021-1051.ossutilconfig'
    cmd_0 = f'ossutil64 ls {oss} -c {config} > {temp_download}/temp_{oss_body}.txt'
    p = subprocess.Popen(cmd_0, shell=True, executable='/bin/bash')
    out, err = p.communicate()
    if p.returncode != 0:
        exit(1)

    # cmd_1,cmd_2 = 'echo 未输入正确下载链接','echo 未输入正确下载链接'
    with open(f'{temp_download}/temp_{oss_body}.txt', 'r')as f0:
        for line in f0:
            MD5_line = re.findall(f'{oss_body}/MD5', line) # 可能有多个md5 和多个rawdata的情况。
            if MD5_line != []:
                MD5_oss_url = line.split(' ')[-1].strip()
                print('MD5_oss_url is :', MD5_oss_url)
                cmd_1 = f"ossutil64 cp -f {MD5_oss_url} {temp_download}/MD5_{oss_body}.txt -c {config}"
            RawData_line = re.findall(f'.*{oss_body}/(RawData|00.mergeRawFq)/$', line)
            if RawData_line != []:
                RawData = 'RawData' if re.findall('RawData', RawData_line[0]) != [] else '00.mergeRawFq'
                RawData_url = line.split(' ')[-1].strip()
                print('RawData_url is :', RawData_url)
                print('RawData is :', RawData)
                if os.path.exists(f'{temp_download}/{RawData}/{sample}'):  # 重复文件处理。移动进被监控文件夹之前还要这样再来一遍。
                    Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    os.rename(f'{temp_download}/{RawData}/{sample}', f'{temp_download}/{RawData}/{sample}_before{Time}')
                cmd_2 = f"ossutil64 cp -f -r {RawData_url} {temp_download}/{RawData}/ -c {config} --include '*{sample}*' "
            os.chdir(f'{temp_download}')  # 进入 MD5 所在文件夹。
            cmd_3 = f'grep "{sample}"  MD5_{oss_body}.txt | md5sum -c > md5sum_result'
    for i in range(1, 4):
        p = subprocess.Popen(locals()[f'cmd_{i}'], shell=True, executable='/bin/bash')
        out, err = p.communicate()
        returncode = p.returncode
        if p.returncode != 0:
            exit(1)
    # 此时 md5sum_result 内 每行都是 OK 结尾的，就说明被读的received_new 文件的这一行可以写入 received_main 中了。
    with open('md5sum_result', 'r') as f:
        shutil.move(f'{temp_download}/MD5_{oss_body}.txt', f'{temp_download}/{RawData}/{sample}/')
        shutil.move(f'{temp_download}/md5sum_result', f'{temp_download}/{RawData}/{sample}/')
        shutil.move(f'{temp_download}/temp_{oss_body}.txt', f'{temp_download}/{RawData}/{sample}/')
        for line in f:
            if not line.endswith('OK\n'):
                print('line is :', line)
                print('此行不可以写入received_main')
                return False, temp_download, RawData
        else:
            print('OK，此行可以写入received_main')
            return True, temp_download, RawData


def read_received_new_table():
    with open('/received/received_new.csv', 'rb') as f:  # 识别编码类型。
        encoding_stype = chardet.detect(f.read())
    df = pd.read_csv('/received/received_new.csv', sep=',', header=1, encoding=encoding_stype['encoding'])
    df.dropna(how='all', inplace=True)
    for index, row in df.iterrows():
        print(row['样本编号*'], row['链接*'])
        sample, oss = row['样本编号*'], row['链接*']
        result, temp_download, RawData = download_checkMD5(oss, sample)
        if result:
            with open('/received/main/received.csv', 'a') as f:
                f.write(','.join(map(str, row)) + '\n')
            # 写入数据仓库。
            if os.path.exists(f'/fastq_data/{sample}'):  # 重复文件处理。移动进被监控文件夹之前还要这样再来一遍。
                Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.rename(f'/fastq_data/{sample}', f'/fastq_data/{sample}_before{Time}')
            cmd = f'cp -r {temp_download}/{RawData}/{sample}/ /fastq_data/{sample}/'
            p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            p.communicate()
            # 文件夹结构不包括文件，写入被监控文件夹。
            if os.path.exists(
                    f'/home/chenyushao/py_streaming_generate/monitor/{sample}'):  # 重复文件处理。移动进被监控文件夹之前还要这样再来一遍。
                Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.rename(f'/home/chenyushao/py_streaming_generate/monitor/{sample}',
                          f'/home/chenyushao/py_streaming_generate/monitor/{sample}_before{Time}')
            src, dst = f'{temp_download}/{RawData}/{sample}/', f'/home/chenyushao/py_streaming_generate/monitor/{sample}/'
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*.fq.gz', '*.fq'))
            # 删除 临时下载文件夹的文件。
            shutil.rmtree(f'{temp_download}/{RawData}/{sample}/')
    # received_new 全部遍历完毕，没有出错，就把received_new扔进历史记录中，提示操作人员可以上传新的received_new了。
    Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    shutil.move('/received/received_new.csv', f'/received/record/received_new{Time}.csv')


def read_received_vip_table():
    with open('/received/received_vip.csv', 'rb') as f:
        encoding_stype = chardet.detect(f.read())
    df = pd.read_csv('/received/received_vip.csv', sep=',', header=1, encoding=encoding_stype['encoding'])
    for index, row in df.iterrows():
        print(row['样本编号*'], row['链接*'])
        sample, oss = row['样本编号*'], row['链接*']
        result, temp_download, RawData = download_checkMD5(oss, sample)
        if result:
            with open('/received/main/received.csv', 'a') as f:
                f.write(','.join(map(str, row)) + ',VIP' + '\n')
            # 写入数据仓库。
            if os.path.exists(f'/fastq_data/{sample}'):  # 重复文件处理。移动进被监控文件夹之前还要这样再来一遍。
                Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.rename(f'/fastq_data/{sample}', f'/fastq_data/{sample}_before{Time}')
            cmd = f'cp -r {temp_download}/{RawData}/{sample}/ /fastq_data/{sample}/'
            p = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            p.communicate()
            # 删除 临时下载文件夹的文件。
            shutil.rmtree(f'{temp_download}/{RawData}/{sample}/')
    # received_vip 全部遍历完毕，没有出错，就把received_vip扔进历史记录中，提示操作人员可以上传新的received_vip了。
    Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    shutil.move('/received/received_vip.csv', f'/received/record/received_vip{Time}.csv')


if __name__ == '__main__':
    # oss = 'oss://sh-kefu-ruimingbio/rawdata/20230424_E150009636_SuZhouRuiMing_C'
    # sample = '20230419L007'
    # result = download_checkMD5(oss,sample)
    # print(result)
    if os.path.exists(f'/received/received_vip.csv'):
        read_received_vip_table()
    if os.path.exists(f'/received/received_new.csv'):
        read_received_new_table()

# # 针对性下载。(注意00.mergeRawFq 与下载位置的00.mergeRawFq 的对应关系;可以用 是否为00.mergeRawFq/或者 RawData/ 结尾来确认目标下载内容。)
# ossutil64 cp -r oss://sh-kefu-ruimingbio/rawdata/20230424_E150009636_SuZhouRuiMing_C/00.mergeRawFq/ ~/py_streaming_generate/temp_download/00.mergeRawFq/ -c /refhub/osskey/sh-kefu-ruimingbio.ossutilconfig --include "*20230419L007*"
#
# # 进入 MD5 所在文件夹 进行 md5sum校验，只需要 sample对应的行 出现了 “OK” 即可。
# grep "20230419L007"  ~/py_streaming_generate/temp_download/MD5.txt | md5sum -c
