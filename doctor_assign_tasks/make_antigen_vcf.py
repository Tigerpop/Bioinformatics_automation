# coding=utf8
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

def tools():
    df = pd.read_csv('0610-T.process.txt',sep='\t')
    df_hava_pathganic = df[df['CLNSIG'].apply(lambda x: re.search(r'Pathogenic',x) != None )]
    print( df_hava_pathganic  )

    df_have_uncertain = df[df['CLNSIG'].apply(lambda x: re.search(r'Uncertain_significance',x) != None )]
    # print(df_have_uncertain)

    df_hava_pathganic['VAF_float'] = df_hava_pathganic['VAF'].str.split(',', expand=True)[0].str.strip("%").astype(float) / 100
    df_hava_pathganic = df_hava_pathganic.sort_values(by=['VAF_float'],ascending=False).reset_index(drop=True, inplace=False)
    print(df_hava_pathganic)

    df_have_uncertain['VAF_float'] = df_have_uncertain['VAF'].str.split(',', expand=True)[0].str.strip("%").astype(float) / 100
    df_have_uncertain = df_have_uncertain.sort_values(by=['VAF_float'],ascending=False).reset_index(drop=True, inplace=False)
    print(df_have_uncertain)

    # pathogenic取50个，如果没有50个，就从uncertain 中补。
    volume = 50
    i = min(volume, len(df_hava_pathganic))
    df_result = df_hava_pathganic[:i]
    if i < volume:
        df_result = pd.concat([df_result,df_have_uncertain[:min(volume-i,len(df_have_uncertain))]])
    df_result['chr_start'] = df_result['Chr']+"_"+df_result['Start'].astype(str)
    print(df_result)
    return df_result

def useAddress_make_antigenVcf(df_address):
    df_address['Start']
    with open('0610-T.pollpass.vcf', 'r')as f0,open('0610-T.antigen.vcf','w')as f1:
        line = f0.readline()
        f1.write(line)
        i = 0
        while line[:2]=='##':
            line = f0.readline()
            f1.write(line)
            i += 1
    print(i)
    df_vcf = pd.read_csv('0610-T.pollpass.vcf',sep='\t',header=i)  # 跳过vcf 的注释部分。
    df_vcf['chr_start'] = df_vcf['#CHROM']+"_"+df_vcf['POS'].astype(str)


    df_result = df_vcf[df_vcf['chr_start'].apply(lambda x: x in df_address['chr_start'].tolist() ) ]
    df_result = df_result.drop(columns=['chr_start'])
    print(df_result)
    df_result.to_csv('temp.vcf',sep='\t',index=None,header=None)
    with open('temp.vcf','r')as f0,open('0610-T.antigen.vcf','a+')as f1:
        for line in f0:
            f1.write(line)

if __name__ == '__main__':
    df_address = tools()
    useAddress_make_antigenVcf(df_address)
