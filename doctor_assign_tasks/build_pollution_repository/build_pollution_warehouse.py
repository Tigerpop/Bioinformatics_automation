# coding=utf8
import pandas as pd
import functools, chardet, sys
import warnings

warnings.filterwarnings('ignore')


def Sort_Chr_Start(chr: str = 'chr', start: str = 'start'):  # 以后都用这样给chr start 文件排序。
    def sort_chr_start(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            df_result1 = df[~(df[chr].isin(['chrX', 'chrY']))]  # 求反集
            df_result1['chr_num'] = df_result1[chr].str.extract(r'(\d+)').astype(int)  # 先处理1-22
            df_result1 = df_result1.sort_values(by=['chr_num', start])

            if not df[df[chr] == 'chrX'].empty:  # 处理xy。
                df_resultX = df[df[chr].isin(['chrX'])]
                df_resultX = df_resultX.sort_values(by=[start])
                df_result1 = pd.concat([df_result1, df_resultX])
            if not df[df[chr] == 'chrY'].empty:
                df_resultY = df[df[chr].isin(['chrY'])]
                df_resultY = df_resultY.sort_values(by=[start])
                df_result1 = pd.concat([df_result1, df_resultY])
            df_result1 = df_result1.drop(columns=['chr_num'])
            print(df_result1)
            return df_result1

        return wrapper

    return sort_chr_start


@Sort_Chr_Start(chr='chr', start='pos')
def read_df(input_file):
    with open(input_file, 'rb') as f:  # 识别编码类型。
        encoding_stype = chardet.detect(f.read())
    df = pd.read_csv(input_file, sep='\t', encoding=encoding_stype['encoding'])
    return df


def build_pollution_warehouse(input_file: str):
    df = pd.read_excel(input_file, sheet_name=None)
    meta = df['meta']
    bed_key, sample = meta['panel'].iloc[0], meta['id'].iloc[0]

    pollution_warehouse = f'/refhub/hg19/toolbox_and_RefFile/{bed_key}_pollution_storehouse.txt'
    somatic, germline = df['somatic'], df['germline']
    df_snpindel = pd.concat([somatic, germline])
    # print(df_snpindel)

    df_potential_pollution = df_snpindel[df_snpindel['review'].isin(['po', 'PO', 'Po', 'oP'])]
    df_potential_pollution = df_potential_pollution.reset_index(drop=True)  # 在df建立一个新的df后，一旦没有重制索引，会带来很多潜在问题！！！ 
    # print(df_potential_pollution)

    # 注意 REF 和 ALT 中的 - 表示的是缺失，不是任意值的意思。
    # 以下是用merge.vcf 文件中的 pos ref 和alt 代替 标签打好的文件的 pos、ref、alt。
    df_potential_pollution['chr_pos'] = df_potential_pollution['Chr']+"_"\
                                                +df_potential_pollution['Start'].astype(str)
    # df_potential_pollution['Start-1'] =  df_potential_pollution['Start'] - 1
    # df_potential_pollution['chr_pos_loss1'] = df_potential_pollution['Chr']+"_"\
    #                                         +df_potential_pollution['Start-1'].astype(str)
    generate_location = '/home/chenyushao/py_streaming_generate/'
    sample_path = sample
    vcf_path = f'/home/chenyushao/py_streaming_generate/{sample_path}/split_vcf/{sample}.merge.vcf'
    with open(vcf_path,'r')as f:
        i=0
        for line in f:
            if line[0] == '#' and line[1] == '#':
                i += 1
            else:
                break
    print(i)
    df_vcf = pd.read_csv(vcf_path,sep='\t',header=i)
    df_vcf['chr_pos'] = df_vcf['#CHROM'] + "_" + df_vcf['POS'].astype(str)
    # print(df_vcf['chr_pos'])
    df_potential_pollution['chr_pos_ref_alt'] = None
    for index,row in df_potential_pollution.iterrows():
        print('index 是:',index)
        start,chr = row['Start'],row['Chr']
        chr_pos = row['chr_pos']
        print('start,chr is :',start,chr)
        print('chr_pos is :',chr_pos)
        while df_vcf[df_vcf['chr_pos'] == chr_pos].empty:
            start -= 1
            chr_pos = chr+"_"+str(start)
            print('中间的chr_pos 是:',chr_pos)
        print('找到可以匹配上的 chr_pos is：',chr_pos)
        row['Start'] = start = chr_pos.split('_')[1]
        row['Chr'] = ref = df_vcf.loc[df_vcf['chr_pos'] == chr_pos, '#CHROM'].values[0]
        row['Ref'] = ref = df_vcf.loc[df_vcf['chr_pos'] == chr_pos, 'REF'].values[0]
        row['Alt'] = alt =  df_vcf.loc[df_vcf['chr_pos'] == chr_pos, 'ALT'].values[0]
        row['chr_pos_ref_alt'] = f'{chr}_{start}_{ref}_{alt}'
        df_potential_pollution.iloc[index] = row
        print('chr_pos_ref_alt 是',row['chr_pos_ref_alt'])
        print('chr,start,ref,alt 分别为： ',chr,start,ref,alt)
        print('chr,start,ref,alt例举完。\n')
    # 以上是用merge.vcf 文件中的 pos ref 和alt 代替 标签打好的文件的 pos ref、alt。
    
    # df_potential_pollution['chr_pos_ref_alt'] = df_potential_pollution['Chr'] + "_" \
    #                                             + df_potential_pollution['Start'].astype(str) + "_" \
    #                                             + df_potential_pollution['Ref'] + "_" \
    #                                             + df_potential_pollution['Alt']
    
    print('df_potential_pollution 是：',df_potential_pollution)
    df_pollution_warehouse = pd.read_csv(pollution_warehouse, sep='\t')
    unique_list = df_pollution_warehouse['chr_pos_ref_alt'].tolist()
    # print(unique_list)
    for index, row in df_potential_pollution.iterrows():
        # 有则修改。
        if row['chr_pos_ref_alt'] in unique_list:
            num = df_pollution_warehouse[df_pollution_warehouse['chr_pos_ref_alt'] == row['chr_pos_ref_alt']]['num'].iloc[0]
            args_VAF = float(
                df_pollution_warehouse[df_pollution_warehouse['chr_pos_ref_alt'] == row['chr_pos_ref_alt']][
                    'arg_VAF'].iloc[0].strip('%'))
            args_VAF = "{:.2f}%".format((args_VAF * num + float(row['VAF'].strip('%'))) / (num + 1))
            # 改污染库
            df_pollution_warehouse.loc[
                df_pollution_warehouse['chr_pos_ref_alt'] == row['chr_pos_ref_alt'], 'arg_VAF'] = args_VAF
            df_pollution_warehouse.loc[
                df_pollution_warehouse['chr_pos_ref_alt'] == row['chr_pos_ref_alt'], 'num'] = num + 1
        # 无则添加
        else:
            new_row = {'chr_pos_ref_alt': row['chr_pos_ref_alt'], 'chr': row['Chr'], 'pos': row['Start'],
                       'ref': row['Ref'], \
                       'alt': row['Alt'], 'arg_VAF': row['VAF'], 'num': 1}
            df_pollution_warehouse = df_pollution_warehouse.append(new_row, ignore_index=True)
            #print('df_pollution_warehouse 新增了一条。:',df_pollution_warehouse)

    df_pollution_warehouse.to_csv(pollution_warehouse, sep='\t', index=None)


# '''
#     # 着补回 误打标签进 污染库的数据，就像chr3 30691872 - A 没打污染标签 ，而chr3 30691872  A - 被打了污染标签；
#     # 她们复原到call 完突变的vcf文件中 其实都是一个位置  chr3 30691871 GA G,GAAA 
#     # 因此我们需要 根据没打标签的信息，把这样的 chr3 30691871 GA G,GAAA 从污染库中剔除；
#     df_out_pollution = df_snpindel[~(df_snpindel['review'].isin(['po', 'PO', 'Po', 'oP']))]
#     df_out_pollution = df_out_pollution.reset_index(drop=True)
#     df_out_pollution['chr_pos'] = df_out_pollution['Chr']+"_"\
#                                             +df_out_pollution['Start'].astype(str)
#     df_out_pollution['chr_pos_ref_alt'] = None
#     for index,row in df_out_pollution.iterrows():
#         print('index 是:',index)
#         start,chr = row['Start'],row['Chr']
#         chr_pos = row['chr_pos']
#         print('start,chr is :',start,chr)
#         print('chr_pos is :',chr_pos)
#         while df_vcf[df_vcf['chr_pos'] == chr_pos].empty:
#             start -= 1
#             chr_pos = chr+"_"+str(start)
#             print('中间的chr_pos 是:',chr_pos)
#         print('找到可以匹配上的 chr_pos is：',chr_pos)
#         row['Start'] = start = chr_pos.split('_')[1]
#         row['Chr'] = ref = df_vcf.loc[df_vcf['chr_pos'] == chr_pos, '#CHROM'].values[0]
#         row['Ref'] = ref = df_vcf.loc[df_vcf['chr_pos'] == chr_pos, 'REF'].values[0]
#         row['Alt'] = alt =  df_vcf.loc[df_vcf['chr_pos'] == chr_pos, 'ALT'].values[0]
#         row['chr_pos_ref_alt'] = f'{chr}_{start}_{ref}_{alt}'
#         df_out_pollution.iloc[index] = row
#         print('chr_pos_ref_alt 是',row['chr_pos_ref_alt'])
#         print('chr,start,ref,alt 分别为： ',chr,start,ref,alt)
#         print('chr,start,ref,alt例举完。\n')
#     print('df_out_pollution 是：',df_out_pollution)
#     # 剔除。
#     df_pollution_warehouse = pd.read_csv(pollution_warehouse, sep='\t')
#     df_pollution_warehouse = df_pollution_warehouse[~df_pollution_warehouse['chr_pos_ref_alt'].isin(df_out_pollution['chr_pos_ref_alt'])]
#     
#     
#     
#     df_pollution_warehouse.to_csv(pollution_warehouse, sep='\t', index=None)
# '''

    df_result = read_df(pollution_warehouse)
    df_result = df_result.drop_duplicates()
    df_result.to_csv(pollution_warehouse, sep='\t', index=None)
    

if __name__ == '__main__':
    input_file = sys.argv[1]
    # build_pollution_warehouse(input_file='/archive/20230523/2023WSSW000978-T.summary.xlsx')
    build_pollution_warehouse(input_file=input_file)


