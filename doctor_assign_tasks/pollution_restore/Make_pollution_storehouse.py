# coding=utf8
import pandas as pd
import numpy as np
import re
pd.set_option('display.max_columns', None)

class data():
    def __init__(self):
        self.raw_pollution_file = 'raw_pollution_storehouse.txt'
        df_1537,df_1567,df_1568,df_1596,df_1597\
        ,df_3292,df_3294,df_3295,df_3765,df_4409 = pd.read_csv('1537.txt', sep='\t')\
                                                  ,pd.read_csv('1567.txt', sep='\t')\
                                                  ,pd.read_csv('1568.txt', sep='\t')\
                                                  ,pd.read_csv('1596.txt', sep='\t')\
                                                  ,pd.read_csv('1597.txt', sep='\t')\
                                                  ,pd.read_csv('3292.txt', sep='\t')\
                                                  ,pd.read_csv('3294.txt', sep='\t')\
                                                  ,pd.read_csv('3295.txt', sep='\t')\
                                                  ,pd.read_csv('3765.txt', sep='\t')\
                                                  ,pd.read_csv('4409.txt', sep='\t')
        df_1537[['Chr','Start','CLNSIG_1537','VAF_1537']]=df_1537[['Chr','Start','CLNSIG','VAF']]
        df_1537=df_1537[['Chr','Start','CLNSIG_1537','VAF_1537']]
        df_1567[['Chr','Start','CLNSIG_1567','VAF_1567']]=df_1567[['Chr','Start','CLNSIG','VAF']]
        df_1567=df_1567[['Chr','Start','CLNSIG_1567','VAF_1567']]
        df_1568[['Chr','Start','CLNSIG_1568','VAF_1568']]=df_1568[['Chr','Start','CLNSIG','VAF']]
        df_1568=df_1568[['Chr','Start','CLNSIG_1568','VAF_1568']]
        df_1596[['Chr','Start','CLNSIG_1596','VAF_1596']]=df_1596[['Chr','Start','CLNSIG','VAF']]
        df_1596=df_1596[['Chr','Start','CLNSIG_1596','VAF_1596']]
        df_1597[['Chr','Start','CLNSIG_1597','VAF_1597']]=df_1597[['Chr','Start','CLNSIG','VAF']]
        df_1597=df_1597[['Chr','Start','CLNSIG_1597','VAF_1597']]
        df_3292[['Chr','Start','CLNSIG_3292','VAF_3292']]=df_3292[['Chr','Start','CLNSIG','VAF']]
        df_3292=df_3292[['Chr','Start','CLNSIG_3292','VAF_3292']]
        df_3294[['Chr','Start','CLNSIG_3294','VAF_3294']]=df_3294[['Chr','Start','CLNSIG','VAF']]
        df_3294=df_3294[['Chr','Start','CLNSIG_3294','VAF_3294']]
        df_3295[['Chr','Start','CLNSIG_3295','VAF_3295']]=df_3295[['Chr','Start','CLNSIG','VAF']]
        df_3295=df_3295[['Chr','Start','CLNSIG_3295','VAF_3295']]
        df_3765[['Chr','Start','CLNSIG_3765','VAF_3765']]=df_3765[['Chr','Start','CLNSIG','VAF']]
        df_3765=df_3765[['Chr','Start','CLNSIG_3765','VAF_3765']]
        df_4409[['Chr','Start','CLNSIG_4409','VAF_4409']]=df_4409[['Chr','Start','CLNSIG','VAF']]
        df_4409=df_4409[['Chr','Start','CLNSIG_4409','VAF_4409']]

        # self.df_list = [df_1537,df_1567,df_1568,df_1596,df_1597,df_3292,df_3294,df_3295,df_4409]  # df_3765 ??????????????????????????????vaf?????????????????????.
        # self.num_list = ['1537','1567','1568','1596','1597','3292','3294','3295','4409']
        self.df_list = [df_1537, df_1567, df_1568, df_1596, df_1597, df_3292, df_3294, df_3295, df_4409]
        self.num_list = ['1537', '1567', '1568', '1596', '1597', '3292', '3294', '3295', '4409']
        df_concat = pd.concat(self.df_list)
        df_concat.to_csv(self.raw_pollution_file, sep='\t', index=False)
        self.df_init = df_concat


    def filter(self):
        # ????????? ????????????CLNSIG ?????? '.' ?????????
        output_file = 'pollution_storehouse.txt'
        with open(self.raw_pollution_file,'r')as f0,open(output_file,'w')as f1:
            header_line = next(f0)
            f1.write(header_line)
            print(header_line)
            for line in f0:
                # print(line)
                elements = re.split(r"[\t]+",line)    # python ???re ??????????????? ???????????? ?????? [ ] ??????????????????
                clnsig,vaf = elements[2],elements[3]
                vaf = float(vaf.split('%')[0])
                if clnsig == '.':
                    f1.write(line)

    def group_compress_position(self,input_file='pollution_storehouse.txt'):
        df = pd.read_csv(input_file,sep='\t')
        print(df)
        # Series.apply() ?????????????????????????????? Series ?????? DataFrame, ??????????????????????????????????????????????????????????????????????????????
        # DataFrame.apply() DataFrame.apply() ?????????????????????????????????????????? function????????????????????? ??????????????????????????????????????????????????????
        # DataFrame.apply() ?????????????????????????????? ????????????df???????????????????????????????????????????????????????????????????????????
        # ????????????????????? python??????append????????????????????????????????????Series ?????????append???????????????????????????????????????????????????????????????
        # ??????????????? python append???????????????????????????
        # reset_index() ????????? groupby?????? ?????????????????? df ?????????
        # pandas ??????????????? df???series?????? append??????????????????????????? df??? series ??? concat???????????????
        def func(df):
            s = pd.Series([],dtype='object')                    # ?????????????????????Series,????????????series??????????????????????????? object?????????
            for num in self.num_list:
                s = pd.concat([ s, pd.Series({
                    f'CLNSIG_{num}': re.sub(r'nan','',''.join(map(str, df[f'CLNSIG_{num}'])))  # ????????????????????? ??? NaN str ??? nan ??????????????????,????????????????????? ??????np.nan???
                })])
                s = pd.concat([ s,pd.Series({
                    f'VAF_{num}': re.sub(r'nan','',''.join(map(str, df[f'VAF_{num}'])))
                })])
            return s

        df_result = df.groupby(['Chr','Start']).apply(func).reset_index()

        for num in self.num_list:                                                # ??????????????????vaf ????????????????????????
            df_result[f'VAF_{num}'] = df_result[f'VAF_{num}'].apply(lambda x: x.split(',')[0])
        df_result = df_result[['Chr','Start','VAF_1537','VAF_1567','VAF_1568','VAF_1596','VAF_1597','VAF_3292','VAF_3294','VAF_3295','VAF_4409']]
        print(df_result)
        df_result.to_csv('pollution_storehouse.txt', sep='\t', index=False)
        return df_result


def sort_chr_start(df_result):
    df_concat = df_result
    # ??????????????? ????????????start ???????????????
    df_result1 = df_concat[~(df_concat.Chr.isin(['chrX', 'chrY']))]                # ~???????????????
    df_result1['chr_num'] = df_result1['Chr'].str.extract(r'(\d+)').astype(float)  # ????????????1-22?????????xy??????????????????
    df_result1 = df_result1.sort_values(by=['chr_num', 'Start'])
    if not df_concat[df_concat['Chr'] == 'chrX'].empty:                            # ??????xy???
        df_resultX = df_concat[df_concat.Chr.isin(['chrX'])]
        df_resultX = df_resultX.sort_values(by=['Start'])
        df_result1 = pd.concat([df_result1, df_resultX])
    if not df_concat[df_concat['Chr'] == 'chrY'].empty:
        df_resultY = df_concat[df_concat.Chr.isin(['chrY'])]
        df_resultY = df_resultY.sort_values(by=['Start'])
        df_result1 = pd.concat([df_result1, df_resultY])
    df_result1 = df_result1.drop(columns=['chr_num'])

    print(df_result1)
    df_result1.to_csv('pollution_storehouse.txt', sep='\t', index=False)
    return df_result1

# ?????????????????????
def add_frequency(df,num_list):
    df = df.replace('',np.nan)
    vaf_list = [f'VAF_{num}' for num in num_list]
    df['frequency'] = df[vaf_list].count(axis=1)/len(vaf_list)
    for vaf_ele in vaf_list:                                             # ?????????????????? 2.3% ??????float????????????????????? ???????????????????????????????????????
        df[vaf_ele] = df[vaf_ele].str.strip("%").astype(float) / 100
    df['sum'] = df[vaf_list].sum(axis=1)
    df['avg'] = df[vaf_list].mean(axis=1)
    df['max'] = df[vaf_list].max(axis=1)
    df['min'] = df[vaf_list].min(axis=1)
    df['Label'] = True
    df = df.round(3)
    # ??????????????????????????????????????????
    vaf_list.extend(['frequency', 'sum', 'avg', 'max', 'min'])
    for ele in vaf_list:
        df[ele] = df[ele].apply(lambda x: format(x,'.2%') if not np.isnan(x) else x)
    print(df)
    df.to_csv('pollution_storehouse.txt', sep='\t', index=False)
    return df

if __name__=='__main__':
    data = data()
    data.filter()
    df_result = data.group_compress_position()
    df_result = sort_chr_start(df_result)
    df_result = add_frequency(df_result,data.num_list)
