# -*- coding: utf-8 -*-
import re,os,sys,shutil,chardet
import pandas as pd
from pandas import DataFrame
from datetime import date
import warnings
warnings.filterwarnings('ignore')

sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
log_path = sys.argv[3]
generate_location = sys.argv[4]
bed_key = sys.argv[5]

def generate_summary():
    # 实现多个sheet 写入一个exel。
    with pd.ExcelWriter(f'{generate_location}/{sample_path}/{sample}.summary.xlsx') as writer:
        try:
            # mate
            with open('/received/main/received.csv', 'rb') as f0: # 确认编码类型。
                encoding_stype = chardet.detect(f0.read())
            df_receive = pd.read_csv(f'/received/main/received.csv',sep=',',header=1,encoding=encoding_stype['encoding'])
            df_mate = df_receive[df_receive['样本编号*']==sample]
            df_mate[['id','name','gender','age','cancer','clinname','送检医院','panel','projectname','报告模版','样本类型*','到样日期*']] \
            = df_mate[['样本编号*','姓名*','性别','年龄','肿瘤类型*','临床诊断*','送检医院','探针*','检测项目*','报告模板*','样本类型*','到样日期*']]
            df_mate = df_mate[['id','name','gender','age','cancer','clinname','送检医院','到样日期*','样本类型*','panel','projectname','报告模版']]
            # df_mate['id'] = df_mate['id'].apply(lambda x: x[:-2])
            df_mate = df_mate.tail(1)
            DataFrame(df_mate).to_excel(writer,sheet_name='meta',index=False,header=True)
            
            # snpindel 
            file = f'{generate_location}/{sample_path}/{sample}.process.hg19_multiprocess.txt'
            df_snpindel = pd.read_csv(file,sep='\t')
            df_snpindel['review'] = None
            DataFrame(df_snpindel).to_excel(writer,sheet_name='snpindel',index=False,header=True)

            # snpindel_germline 
            file = f'{generate_location}/{sample_path}/{sample}.germline.hg19_multigermline.txt'
            df_germline = pd.read_csv(file,sep='\t')
            df_germline['review'] = None
            DataFrame(df_germline).to_excel(writer,sheet_name='germline',index=False,header=True)
            
            
            # fusion
            file = f"{generate_location}/{sample_path}/factera_generate/{sample}.bwa_mem.factera.fusions.txt"
            head = ['Est_Type','Region1','Region2','Break1','Break2','Break_support1','Break_support2','Break_offset','Orientation','Order1','Order2','Break_depth','Proper_pair_support','Unmapped_support','Improper_pair_support','Paired_end_depth','Total_depth','Fusion_seq','<>','Non-templated_seq','-']
            df_fusion = pd.read_csv(file,sep='\t',header=None,names=head,skiprows=1)
            df_fusion['review'] = None
            DataFrame(df_fusion).to_excel(writer,sheet_name='fusion',index=False)
            
            # cnv
            file = f'{generate_location}/{sample_path}/decon_generate/DECoNtestCalls_all.txt'
            df_cnv = pd.read_csv(file,sep='\t')
            df_cnv['cnv.number'] = df_cnv['Reads.ratio']*2 
            df_cnv['review'] = None
            DataFrame(df_cnv).to_excel(writer,sheet_name='cnv',index=False,header=True)
            
            # msi 和 chemo
            if bed_key in ['Q120','SD160','NBC650','BCP650']: 
                file1 = f"{generate_location}/{sample_path}/msisensor_generate/{sample}msi"
                file2 = f"{generate_location}/{sample_path}/msisensor_generate/{sample}msi_somatic"
                file = f"{generate_location}/{sample_path}/temp_smi"
                with open(file1,'r')as f0,open(file2,'r')as f1,open(file,'w')as f2:
                    for line in f0:
                        f2.write(line)
                    for line in f1:
                        f2.write(line)
                df_msi = pd.read_csv(file,sep='\t',header=None,names=[1,2,3,4,5,6,7])
                DataFrame(df_msi).to_excel(writer,sheet_name='msi',index=False,header=False)
                
                file = f"{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt"
                df_chemo = pd.read_csv(file,sep='\t')
                df_chemo['review'] = None
                DataFrame(df_chemo).to_excel(writer,sheet_name='chemo',index=False,header=True)
            
            # hla 和 neoantigen
            if bed_key in ['NBC650','BCP650']: 
                file = f'{generate_location}/{sample_path}/optitype_generate/fished_result.tsv'
                df_hla = pd.read_csv(file,sep='\t')
                df_hla = df_hla.rename(columns={'Unnamed: 0':'Patient'})      # 重命名一下第一列。
                df_hla['Patient'] = sample
                DataFrame(df_hla).to_excel(writer,sheet_name='hla',index=False,header=True) 
                file = f'{generate_location}/{sample_path}/neoantigen_generate/{sample}.format_neoantigens.txt'
                df_neoantigen = pd.read_csv(file,sep='\t')
                df_neoantigen['review'] = None
                DataFrame(df_neoantigen).to_excel(writer,sheet_name='neoantigen',index=False,header=True) 
            
            # qc   
            file = f"{log_path}/quality_control/Quality_Control.txt"
            file1 = f"{log_path}/temp_qc"
            with open(file, 'r') as f:
                lines = f.readlines()
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            dict = {}
            for line in non_empty_lines:
                if len(line.split(":"))>1:
                    dict[line.split(":")[0]] = line.split(":")[1]
                # else:
                #      dict[line.split(":")[0]] = ' '
            with open(file1,'w')as f:
                print(dict.values())
                f.write('\t'.join(dict.keys())+'\n')
                f.write('\t'.join(dict.values())+'\n')
            df_qc = pd.read_csv(file1,sep='\t')
            DataFrame(df_qc).to_excel(writer,sheet_name='qc',index=False,header=True)
            
        except Exception as e:
            # print(e, type(e))
            if (isinstance(e, pd.errors.EmptyDataError)):
                print(f"这里对空行文件\n{file}\n进行处理")
                if re.search('fusion',file)!=None:
                    head = ['Est_Type','Region1','Region2','Break1','Break2','Break_support1','Break_support2','Break_offset','Orientation','Order1','Order2','Break_depth','Proper_pair_support','Unmapped_support','Improper_pair_support','Paired_end_depth','Total_depth','Fusion_seq','<>','Non-templated_seq','-','review']
                    df_fusion = pd.DataFrame(columns=header)
                    DataFrame(df_fusion).to_excel(writer,sheet_name='fusion',index=False,header=True)
            sys.stderr.write(f'出现错误：\n {e} \n')
            exit(1) # 让上一层看见 这一步出现的错误。
            
def send_summary_to_archive(): # 和之前批处理不一样，这里只需要把这一个sample 添加进archive文件夹的当天子文件夹内。
    try:
        today=date.today().strftime("%Y%m%d")
        summary_file = f'{generate_location}/{sample_path}/{sample}.summary.xlsx'
        print(summary_file)
        today=date.today().strftime("%Y%m%d")
        if not os.path.exists(f'/archive/{today}'):
            os.mkdir(f'/archive/{today}')
        shutil.copyfile(summary_file, f'/archive/{today}/{sample}.summary.xlsx')
    except Exception as e:
        sys.stderr.write(f'出现错误：\n {e} \n')
        exit(1) # 让上一层看见 这一步出现的错误。
        
if __name__=='__main__':
    generate_summary()
    send_summary_to_archive()
