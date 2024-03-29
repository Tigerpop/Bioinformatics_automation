# -*- coding: utf-8 -*-
import quality_control as qc
import subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')

sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
log_path = sys.argv[3]
bed_key = sys.argv[4]
sample_monitor = sys.argv[5] # 文件下载位置。
# vip_monitor = '/home/chenyushao/py_streaming_generate/vip_monitor'

def determine_sample_type(sample):
    pattern1 = r'.*(-T|-N|-T-1|-N-1)$'  # 样本类型1的正则表达式模式
    pattern2 = r'^\d{8}C?L\d{3}$'  # 样本类型2和3的正则表达式模式
    pattern3 = r'^\w+-\w+-\w+-\w+$'
    if re.match(pattern1, sample):
        print('这是 解码的样本')
        return "解码"
    elif re.match(pattern2, sample):
        print('这是 睿明的样本')
        return "睿明"
    elif re.match(pattern3, sample):
        print('这是 融享的样本')
        return "融享"
    else:
        return "未知样本类型"

def find_sampe_TN():
    if determine_sample_type(sample)=="解码":
        sample_path_TN = sample_path.replace('-T','-N') if '-T' in sample_path else sample_path.replace('-N','-T')
        # sample_path_TN = sample_path[:-1]+'N' if sample_path[-1] == 'T' else sample_path[:-1]+'T'
    elif determine_sample_type(sample)=="睿明":
        sample_path_TN = sample_path.replace('CL','L') if 'CL' in sample_path else sample_path.replace('L','CL')
    elif determine_sample_type(sample)=="融享":
        sample_path_TN = sample.replace('DZ','') if 'DZ' in sample else sample.rsplit('-', 1)[0] + 'DZ-' + sample.rsplit('-', 1)[1]
        temp_G = ['-'+str(i)+'G' for i in range(1,41)]
        combined_files = os.listdir(sample_monitor)# + os.listdir(vip_monitor)
        for capacity in temp_G:
            if capacity in sample_path_TN:
                other_ele_list = [x for x in temp_G if x!=capacity]
                for ele in other_ele_list:
                    temp_sample_path_TN = sample_path_TN.replace(capacity,ele)
                    if temp_sample_path_TN in combined_files:
                        sample_path_TN = temp_sample_path_TN
                        return sample_path_TN
                temp_sample_path_TN = sample_path_TN.replace(capacity,'-')
                if temp_sample_path_TN in combined_files:
                    sample_path_TN = temp_sample_path_TN
                    return sample_path_TN
    else:
        sample_path_TN = sample_path
    return sample_path_TN
sample_path_TN = find_sampe_TN()

# 注意，
# 走vip手动流程的话，因为没有加入 monitor 文件夹中，所以总是下载目录下有没有它，也就不会走TN对比。
# 因此 需要改进这里；已经改进。
combined_files = os.listdir(sample_monitor)# + os.listdir(vip_monitor)
print('sample_path_TN is :',sample_path_TN,'vip_monitor 是 ','vip_monitor')
print('配对的样本存在吗？',sample_path_TN in combined_files)
print('sample_path_TN : ',sample_path_TN,'下载目录下有没有它？',sample_path_TN in combined_files)
#print('我们看看vip_monitor下有哪些？ ',os.listdir(vip_monitor))
print('bed_key is:',bed_key)
if ((bed_key == 'BCP650' or bed_key == 'NBC650' or 'HRD')  and sample_path_TN in combined_files):  # 做一下 NGScheckmate 的质控，看看是不是一套。
    print('进入TN看匹配度的环节')
    QC = qc.tool()
    TN_similarity = QC.NGScheckmate(sample,sample_path,sample_monitor,log_path)
    if TN_similarity < 0.75:
        with open(f'{log_path}/quality_control/Quality_Control.txt','w')as f0:                      # 不符合条件，就停止后续流程。
            f0.write('NGScheckmate 结果质控不合格！！'+"\n")
            f0.write('TN_similarity: '+str(TN_similarity)+'\n')
        exit(4)
    with open(f'{log_path}/quality_control/Quality_Control.txt','a+')as f0:
        f0.write('NGScheckmate 结果质控合格！！'+"\n")
        f0.write('TN_similarity: '+str(TN_similarity)+'\n')
