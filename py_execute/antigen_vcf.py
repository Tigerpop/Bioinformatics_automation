# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]



def tools(input_process):
    df = pd.read_csv(input_process,sep='\t')
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

def useAddress_make_antigenVcf(df_address,input_pollpass,output_antigen):
    df_address['Start']
    with open(input_pollpass, 'r')as f0,open(output_antigen,'w')as f1:
        line = f0.readline()
        f1.write(line)
        i = 0
        while line[:2]=='##':
            line = f0.readline()
            f1.write(line)
            i += 1
    print(i)
    df_vcf = pd.read_csv(input_pollpass,sep='\t',header=i)  # 跳过vcf 的注释部分。
    df_vcf['chr_start'] = df_vcf['#CHROM']+"_"+df_vcf['POS'].astype(str)


    df_result = df_vcf[df_vcf['chr_start'].apply(lambda x: x in df_address['chr_start'].tolist() ) ]
    df_result = df_result.drop(columns=['chr_start'])
    print(df_result)
    df_result.to_csv('./temp.vcf',sep='\t',index=None,header=None)
    with open('./temp.vcf','r')as f0,open(output_antigen,'a+')as f1:
        for line in f0:
            f1.write(line)

if __name__ == '__main__':
    try:
        os.chdir(generate_location+"/"+sample_path)
        input_process = generate_location+"/"+sample_path +"/"+ sample+'.process.filter.hg19_multianno.txt'
        input_pollpass = generate_location+"/"+sample_path +"/"+ sample+'.pollpass.vcf'
        output_antigen = generate_location+"/"+sample_path +"/"+ sample+'.antigen.vcf'
        
        df_address = tools(input_process)
        useAddress_make_antigenVcf(df_address,input_pollpass,output_antigen)
    except:
        print('make antigen.vcf is falsed !')
