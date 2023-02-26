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

        # self.df_list = [df_1537,df_1567,df_1568,df_1596,df_1597,df_3292,df_3294,df_3295,df_4409]  # df_3765 去掉，因为样本得出的vaf过多，影响太大.
        # self.num_list = ['1537','1567','1568','1596','1597','3292','3294','3295','4409']
        self.df_list = [df_1537, df_1567, df_1568, df_1596, df_1597, df_3292, df_3294, df_3295, df_4409]
        self.num_list = ['1537', '1567', '1568', '1596', '1597', '3292', '3294', '3295', '4409']
        df_concat = pd.concat(self.df_list)
        df_concat.to_csv(self.raw_pollution_file, sep='\t', index=False)
        self.df_init = df_concat


    def filter(self):
        # 过滤掉 临床意义CLNSIG 不为 '.' 的行。
        output_file = 'pollution_storehouse.txt'
        with open(self.raw_pollution_file,'r')as f0,open(output_file,'w')as f1:
            header_line = next(f0)
            f1.write(header_line)
            print(header_line)
            for line in f0:
                # print(line)
                elements = re.split(r"[\t]+",line)    # python 用re 正则来实现 按照任意 数量 [ ] 分割字符串。
                clnsig,vaf = elements[2],elements[3]
                vaf = float(vaf.split('%')[0])
                if clnsig == '.':
                    f1.write(line)

    def group_compress_position(self,input_file='pollution_storehouse.txt'):
        df = pd.read_csv(input_file,sep='\t')
        print(df)
        # Series.apply() 功能也是自动遍历整个 Series 或者 DataFrame, 对每一个元素运行指定的函数，每一个值是基本处理单元。
        # DataFrame.apply() DataFrame.apply() 函数对某列或者几列运行指定的 function。以列或者行为 参数函数的参数，也就是基本处理单元。
        # DataFrame.apply() 传入的参数函数的参数 也可以是df，可以灵活的处理，只要实质上对每个元素处理过就行。
        # 需要注意的是： python中的append方法是没有返回值的，但是Series 对象的append方法是有返回值的，而且必须要赋值才能变化。
        # 以上的点和 python append方法区别很大！！！
        # reset_index() 可以把 groupby后的 分组对象变回 df 结构。
        # pandas 中即将淘汰 df和series对象 append方法的支持，统一用 df和 series 的 concat方法替代。
        def func(df):
            s = pd.Series([],dtype='object')                    # 先建立一个空的Series,新版本的series建立默认要求元素是 object类型。
            for num in self.num_list:
                s = pd.concat([ s, pd.Series({
                    f'CLNSIG_{num}': re.sub(r'nan','',''.join(map(str, df[f'CLNSIG_{num}'])))  # 这里一定要小心 把 NaN str 成 nan ，后续会影响,后面记得把‘’ 换成np.nan。
                })])
                s = pd.concat([ s,pd.Series({
                    f'VAF_{num}': re.sub(r'nan','',''.join(map(str, df[f'VAF_{num}'])))
                })])
            return s

        df_result = df.groupby(['Chr','Start']).apply(func).reset_index()

        for num in self.num_list:                                                # 只取第一个，vaf 有多个值的情况。
            df_result[f'VAF_{num}'] = df_result[f'VAF_{num}'].apply(lambda x: x.split(',')[0])
        df_result = df_result[['Chr','Start','VAF_1537','VAF_1567','VAF_1568','VAF_1596','VAF_1597','VAF_3292','VAF_3294','VAF_3295','VAF_4409']]
        print(df_result)
        df_result.to_csv('pollution_storehouse.txt', sep='\t', index=False)
        return df_result


def sort_chr_start(df_result):
    df_concat = df_result
    # 以下为按照 染色体和start 依次升序。
    df_result1 = df_concat[~(df_concat.Chr.isin(['chrX', 'chrY']))]                # ~是求反集。
    df_result1['chr_num'] = df_result1['Chr'].str.extract(r'(\d+)').astype(float)  # 仅仅处理1-22基因，xy后面加上去。
    df_result1 = df_result1.sort_values(by=['chr_num', 'Start'])
    if not df_concat[df_concat['Chr'] == 'chrX'].empty:                            # 处理xy。
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

# 加入其他指标。
def add_frequency(df,num_list):
    df = df.replace('',np.nan)
    vaf_list = [f'VAF_{num}' for num in num_list]
    df['frequency'] = df[vaf_list].count(axis=1)/len(vaf_list)
    for vaf_ele in vaf_list:                                             # 每一个字符串 2.3% 改为float类型方便计算。 最后为了美观还能再改回去。
        df[vaf_ele] = df[vaf_ele].str.strip("%").astype(float) / 100
    df['sum'] = df[vaf_list].sum(axis=1)
    df['avg'] = df[vaf_list].mean(axis=1)
    df['max'] = df[vaf_list].max(axis=1)
    df['min'] = df[vaf_list].min(axis=1)
    df['Label'] = True
    df = df.round(3)
    # 改回百分数的显示，好看一些。
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
