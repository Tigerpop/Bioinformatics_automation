# coding=utf8
import pandas as pd
import subprocess,os
from multiprocessing import Process,Pool

def drop_duplicate():
    raw_df = pd.read_csv('middle_generate.txt',sep='\t')
    raw_df.drop_duplicates(subset=['variant'],keep='first',inplace=True)
    print(raw_df['variant'].iloc[0],len(raw_df['variant']))
    raw_df.to_csv('middle_generate.txt',sep='\t',index=None)

def process(j):
    raw_df = pd.read_csv('middle_generate.txt',sep='\t')
    print(raw_df['variant'])
    length_rslist = len(raw_df['variant'])
    if j==6:
        for i in range(500*j-500,length_rslist):
            rs = raw_df['variant'].iloc[i]      #  rs1042713  
            cmd = "cat /opt/annovar/humandb/hg19_avsnp150.txt | grep {rs}$ >> /home/chenyushao/chemo/new_rs.txt".format(rs=rs)
            p = subprocess.Popen(cmd,shell=True)
            p.communicate()
    else:
        for i in range(500*j-500,500*j):
            rs = raw_df['variant'].iloc[i]      #  rs1042713  
            cmd = "cat /opt/annovar/humandb/hg19_avsnp150.txt | grep {rs}$ >> /home/chenyushao/chemo/new_rs.txt".format(rs=rs)
            p = subprocess.Popen(cmd,shell=True)
            p.communicate()
            
def drop_duplicate2():
    raw_df = pd.read_csv('new_rs.txt',sep='\t',header=None,names=['chr','start','end','v1','v2','rs'])
    raw_df.drop_duplicates(subset=['rs'],keep='first',inplace=True)
    print(raw_df,len(raw_df))
    raw_df2 = pd.read_csv('middle_generate.txt',sep='\t')
    raw_df2.drop_duplicates(subset=['variant'],keep='first',inplace=True)
    print(raw_df2[(~raw_df2.variant.isin(raw_df['rs'].values.tolist()))])
    print(len(raw_df2[(~raw_df2.variant.isin(raw_df['rs'].values.tolist()))]))
    print(len(raw_df),len(raw_df2))
    # 有17个 rs 从 hg19_avsnp150.txt 中找不到 对应的位置信息！！！
    raw_df.to_csv('drop_duplicate_new_rs.txt',sep='\t',index=None,header=None)
    
if __name__=="__main__":
    # drop_duplicate()
    # 
    # test_list = [j for j in range(1,7)]
    # pool = Pool(processes=6)
    # for j in test_list:
    #     print(j)
    #     pool.apply_async(process,(j,))
    # pool.close()
    # pool.join()
    
    drop_duplicate2()
