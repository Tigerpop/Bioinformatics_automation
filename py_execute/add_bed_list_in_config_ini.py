# coding = utf8 
import re,configparser
import pandas as pd 
import numpy as np 
config = configparser.ConfigParser()
config.read('config.ini')
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']

def build_bed_list(sample_list):
    dict_ = {} 
    dict_['BC17'] = f'/refhub/{hg_19_or_38}/target/BC17/BC17.raw.{hg_19_or_38}.bed'
    dict_['BCP650'] = f'/refhub/{hg_19_or_38}/target/BCP650/BCP650.raw.{hg_19_or_38}.bed'
    dict_['HY671'] = f'/refhub/{hg_19_or_38}/target/HY671/HY671.raw.{hg_19_or_38}.bed'
    dict_['NBC650'] = f'/refhub/{hg_19_or_38}/target/NBC650/NBC650.raw.{hg_19_or_38}.bed'
    dict_['Q120'] = f'/refhub/{hg_19_or_38}/target/Q120/Q80.raw.{hg_19_or_38}.bed'
    dict_['SD160'] = f'/refhub/{hg_19_or_38}/target/SD160/SD160.raw.bed'
    
    bed_list = []
    sample_list = re.findall( r"\'(.*?)\'",sample_list)
    df_received = pd.read_csv('/received/received.csv',sep=',',header=1) 
    # print(df_received[['样本编号*','探针*']])
    # print(sample_list)
    for sample in sample_list:
        # print(df_received[df_received['样本编号*']==sample]['探针*'].iloc[0])
        bed_name = str(df_received[df_received['样本编号*']==sample]['探针*'].iloc[0])
        bed_list.append(bed_name+":"+dict_[bed_name])
    # print(bed_list)
    return bed_list
  
# build_bed_list(str(['2022WSSW005588-T','2022WSSW005258-T','2022WSSW005704-T']))
