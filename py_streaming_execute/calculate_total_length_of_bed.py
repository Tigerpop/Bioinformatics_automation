# coding=utf8

import subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')


# sample = sys.argv[1] # 第一个参数
# sample_path = sys.argv[2]
# generate_location = sys.argv[3]
# bed = sys.argv[4]



# 算法思想：
# 按照染色体分组，每组内按照下列逻辑：
'''
    每新加一个区域，就实现一次 【"加新区域长度"，"减重叠区域长度"，"老区域融合"】
    （符合条件的段）
    假定新区域为 start_,end_
    其中 "减重叠区域长度" 要从 已经遍历的 段中，找出 start < end_ && end > start_ 的 所有段；
    每个符合要求的段都要执行一次 和 新加区域 剔除 重叠区域的计算（单一重）：
    （单一重）
    min(end,end_) - max(start,start_)
    （重叠区域长度）
    符合条件的段 每个都计算一遍（单一重），求和就是 总重叠区域长度，用前面的 "加新区域长度"，"减重叠区域长度" 即可；
    （老区域融合）
    已经遍历的段中 符合条件的段全部删除，加入一个 融合好的段；
'''

# 换一种算法，先全部融合，再求总长度，逻辑更加清晰；
# 但是我们为了图省事，直接用bedtools 的merge命令 来合并 段；
# 然后再 求 总 end - start 差值 即可。

class tool():
    def __init__(self,sample,sample_path,generate_location,bed):
        self.sample,self.sample_path,self.generate_location,self.bed = sample,sample_path,generate_location,bed
    def sort_chr(self,bed: str,output: str):
        bed_df = pd.read_csv(bed,sep='\t')
        bed_df = bed_df.iloc[:, :3]
        bed_df.columns = ['chr','start','end']
        # print(bed_df)
        df_result1 = bed_df[~(bed_df.chr.isin(['chrX','chrY']))]                                    # 求反集
        df_result1['chr_num'] = df_result1['chr'].str.extract(r'(\d+)').astype(int)   # 先处理1-22
        df_result1 = df_result1.sort_values(by=['chr_num','start'])
        if not bed_df[bed_df['chr']=='chrX'].empty:                           # 处理xy。
            df_resultX = bed_df[bed_df.chr.isin(['chrX'])]
            df_resultX = df_resultX.sort_values(by=['start'])
            df_result1 = pd.concat([df_result1,df_resultX])
        if not bed_df[bed_df['chr']=='chrY'].empty:
            df_resultY = bed_df[bed_df.chr.isin(['chrY'])]
            df_resultY = df_resultY.sort_values(by=['start'])
            df_result1 = pd.concat([df_result1,df_resultY])
        df_result1 = df_result1.drop(columns=['chr_num'])
        df_result1.to_csv(output,sep='\t',index=None,header=None)
    
    def merge_bed(self,input_bed:str,output_bed:str):
        cmd = f"bedtools merge -i {input_bed} > {output_bed}"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
    
    def calculate_total_length_of_bed(self,input):
        bed_df = pd.read_csv(input,sep='\t')
        bed_df = bed_df.iloc[:, :3]
        bed_df.columns = ['chr','start','end']
        bed_df['diff_sum'] = bed_df['end'].astype(int) - bed_df['start'].astype(int)
        result =bed_df.diff_sum.sum()
        print(bed_df,'result is :',result)
        return result 
        
    def main(self):
        bed = self.bed
        sorted_bed = f'{self.generate_location}/{self.sample_path}/sorted.bed'
        merged_bed = f'{self.generate_location}/{self.sample_path}/merged.bed'
        self.sort_chr(bed,sorted_bed)
        self.merge_bed(input_bed=sorted_bed,output_bed=merged_bed)
        result = self.calculate_total_length_of_bed(merged_bed)
        return result 
    
    
# if __name__=='__main__':
#     T = tool()
#     result = T.main()
#     print('result is :',result)
    
    
    
    



