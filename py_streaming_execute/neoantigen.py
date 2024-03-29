# -*- coding: utf-8 -*-
import subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')

sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
bed_key = sys.argv[4]

os.chdir(generate_location+"/"+sample_path)
if not os.path.exists("neoantigen_generate"):
    os.mkdir("neoantigen_generate")
# os.chdir(generate_location+"/"+sample_path+"/"+"neoantigen_generate")

def format_optitype_result_0(sample):
    df = pd.read_csv('./optitype_generate/fished_result.tsv',sep='\t',header=None,names=['Patient','HLA-A_1','HLA-A_2','HLA-B_1','HLA-B_2','HLA-C_1','HLA-C_2','some1','some2'])
    df = df.drop(index=[0])[['Patient','HLA-A_1','HLA-A_2','HLA-B_1','HLA-B_2','HLA-C_1','HLA-C_2']]
    df['Patient'].iloc[0] = sample + '.antigen'
    def func(x):
        if x[:2]=='A*': return 'HLA-A'+x[2:]
        elif x[:2]=='B*': return 'HLA-B'+x[2:]
        elif x[:2] == 'C*': return 'HLA-C' + x[2:]
        else: return x
    df = df.applymap(func)
    print(df)
    df.to_csv(generate_location+"/"+sample_path+"/"+"neoantigen_generate"+'/'+'hla_new_format.txt',sep='\t',index=None)


def Neoprepipe(sample):
    antigen_vcf = generate_location+"/"+sample_path +"/"+ 'antigen_generate'+'/'#+ sample+'.antigen.vcf' # 在这个文件夹下可以找到以样本名命名的vcf文件。
    cmd = f'python2 /opt/NeoPredPipe/NeoPredPipe.py \
            -I {antigen_vcf} \
            -H ./neoantigen_generate/hla_new_format.txt \
            -o ./neoantigen_generate/ -n {sample} \
            -c 1 2 \
            -E 8 9 10'
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    if p.returncode != 0:
        exit('neoantigen is false!')
 
    
def format_optitype_result_1(sample):
    df = pd.read_csv(f'./neoantigen_generate/{sample}.neoantigens.txt',sep='\t',header=None,\
    names=['Sample','R1','R2','Line','chr','allelepos','ref','alt','GeneName:RefSeqID',\
    'pos','hla','peptide','core','Of','Gp','Gl','Ip','Il','Icore','Identity','Score_EL',\
    '%Rank_EL','Score_BA','%Rank_BA','Aff(nM)','Candidate','BindLevel'])
    df['GeneName'] = df['GeneName:RefSeqID'].apply(lambda x: x.split(',')[0].split(":")[0])
    # print(df)
    df.to_csv(generate_location+"/"+sample_path+"/"+"neoantigen_generate"+'/'+f'{sample}'+'.format_neoantigens.txt',sep='\t',index=None)

if __name__=="__main__":
    if bed_key in ['BCP650','NBC650']:
        format_optitype_result_0(sample)
        Neoprepipe(sample)
        format_optitype_result_1(sample)
