#coding=utf8
import pandas as pd 
import subprocess,os,sys
import functools
from typing import Dict, List, Union

sample = sys.argv[1]  # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
bed = sys.argv[4]
log_path = sys.argv[5]

import configparser,subprocess,re,os,sys

class tool():
    def process_fastp_log(self,sample,sample_path,generate_location): 
        # 主动抛出异常，看看父进程的父进程显示效果。
        # aaa
        
        base_quality,inser_size_peak,duplication_rate = '没找到，手动找找','没找到，手动找找','没找到，手动找找'
        os.chdir(sample_path)
        quality_dir = sample_path+"/"+"quality_control"
        if not os.path.exists(quality_dir):
            os.mkdir(quality_dir)
        with open(sample_path+"/"+'fastp_extract_debug.log','r') as f0:
            i = 0 
            for lines in f0:
                if len(lines.split(' ')) >= 3:
                    v1,v2,v3 = lines.split(' ')[0],lines.split(' ')[1],lines.split(' ')[2]
                    if v1 == 'Q30' and v2 == 'bases:' and i==0:
                        base_quality = re.findall('\((.*?)\)',v3)[0]
                        print('base_quality: ',base_quality)
                        i += 1
                if lines[:-5] == 'Insert size peak (evaluated by paired-end reads):':
                    inser_size_peak = lines[-5:-1]
                    print('inser_size_peak: ',inser_size_peak)
                if lines[:17] == 'Duplication rate:':
                    duplication_rate = lines[18:]
                    print('duplication_rate: ',duplication_rate)
        return base_quality,inser_size_peak,duplication_rate
    
    def process_bam(self,sample,log_path,sample_path,generate_location,bed):
        mapped,Coverage,ontarget,depth,cleandepth = '没找到，手动找找','没找到，手动找找','没找到，手动找找','没找到，手动找找','没找到，手动找找'
        
        os.chdir(f"{log_path}/quality_control")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        # quality_dir = generate_location+"/"+log_path+"/"+"quality_control"
        # if not os.path.exists("quality_control"):
        #     os.mkdir("quality_control")
            
        bam_file = generate_location +"/"+ sample_path +"/"+ sample +".markdup.bam"
        cmd = f'samtools flagstat {bam_file} > {log_path}/quality_control/output.flagstat'
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        cmd = f'/opt/bamdst/bamdst -p {bed} -o {log_path}/quality_control/ {bam_file}'
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        
        with open(f'{log_path}/quality_control/output.flagstat','r') as f0:
            for lines in f0:
                mapped = re.findall('.*mapped \((.*?)\)',lines)
                if mapped != []:          # 第一个出现mapped 的地方。
                    print('mapped: ',mapped)
                    mapped = mapped[0].split(':')[0]
                    break
        with open(f'{log_path}/quality_control/coverage.report','r')as f:
            for lines in f:
                Coverage_line = re.findall(r'\[Target\] Coverage \(>=4x\)', lines)
                if Coverage_line!=[]:                # 定位到目标行。
                    [Coverage] = re.findall(r'\d*\.\d*%$',lines)
                    print(Coverage)
                ontarget_line = re.findall(r'Fraction of Target Reads in all reads', lines)
                if ontarget_line != []:  # 定位到目标行。
                    [ontarget] = re.findall(r'\d*\.\d*%$', lines)
                    # print(lines)
                    print(ontarget)
                depth_line = re.findall(r'\[Target\] Average depth',lines)
                if depth_line != [] and re.findall(r'\(.*?\)',lines)==[]: # 同时无括号。
                    [depth] = re.findall(r'\d*\.\d*$', lines)
                    # print(lines)
                    print(depth)
                cleandepth_line = re.findall(r'\[Target\] Average depth\(rmdup\)',lines)
                if cleandepth_line != []:
                    [cleandepth] = re.findall(r'\d*\.\d*$', lines)
                    # print(lines)
                    print(cleandepth)
        return mapped,Coverage,ontarget,depth,cleandepth


# 翻译的对应关系表。
def choose(english_word: str) -> str:  
    options = {
        'cyclophosphamide': '环磷酰胺','temozolomide': '替莫唑胺','fluorouracil': '氟尿嘧啶','tegafur': '替加氟',
        'capecitabine': '卡培他滨','gemcitabine': '吉西他滨','pemetrexed': '培美曲塞','methotrexate': '甲氨蝶呤','doxorubicin': '多柔比星',
        'epirubicin': '表柔比星','mitoxantrone': '丝裂霉素','erythromycin': '红霉素','irinotecan': '伊立替康','vincristine': '长春新碱',
        'vinorelbine': '长春瑞滨','etoposide': '依托泊苷','paclitaxel': '紫杉醇','docetaxel': '多西他赛','tamoxifen': '他莫昔芬','letrozole': '来曲唑',
        'anastrozole': '阿那曲唑','cisplatin': '顺铂','Platinum compounds': '铂类化合物','carboplatin': '卡铂','oxaliplatin': '奥沙利铂',
        'leucovorin': '甲酰四氢叶酸','tropisetron': '曲硫咪索','ondansetron': '昂丹司琼','granisetron': '格拉司琼',
        'Breast Neoplasms;Drug Toxicity': '乳腺肿瘤；药物毒性',
        
        
        'Phenotype Category': '表型类别','Toxicity': '毒性','Efficacy': '疗效','Metabolism/PK': '代谢',
        'Other': '其他','Dosage': '剂量',
        
        'Breast Neoplasms':'乳腺肿瘤','Drug Toxicity': '药物毒性','Transplantation': '移植','Hepatic Veno-Occlusive Disease': '肝窦闭塞症',
        'Transplantation': '移植','Neoplasms': '肿瘤','Glioma': '胶质瘤','Rectal Neoplasms': '直肠肿瘤','Colonic Neoplasms': '结肠肿瘤',
        'Neoplasm Metastasis': '肿瘤转移', 'Stomach Neoplasms': '胃肿瘤','Pancreatic Neoplasms': '胰腺肿瘤','Colorectal Neoplasms': '结直肠肿瘤',
        'Uterine Cervical Neoplasms': '宫颈癌','Glioma': '胶质瘤','Drug Toxicity': '药物毒性','Nausea': '恶心', 'Vomiting': '呕吐',
        'Diarrhea': '腹泻', 'Neoplasms': '肿瘤','Colorectal Neoplasms': '结直肠肿瘤','Carcinoma, Non-Small-Cell Lung': '非小细胞肺癌',
        'Carcinoma, Non-Small-Cell Lung': '非小细胞肺癌', 'Mesothelioma': '间皮瘤', 'Pancreatic Neoplasms': '胰腺肿瘤',
        'Neoplasms': '肿瘤', 'Neutropenia': '中性粒细胞减少','Carcinoma, Non-Small-Cell Lung': '非小细胞肺癌', 'Mesothelioma': '间皮瘤',
        'Mesothelioma': '间皮瘤','Carcinoma, Non-Small-Cell Lung': '非小细胞肺癌', 'Mesothelioma': '间皮瘤','Carcinoma, Non-Small-Cell Lung': '非小细胞肺癌',
        'Osteosarcoma': '骨肉瘤','Arthritis, Rheumatoid': '类风湿性关节炎', 'Drug Toxicity': '药物毒性','Adverse Events': '不良事件', 'Arthritis, Rheumatoid': '类风湿性关节炎',
        'Psoriasis': '银屑病','Breast Neoplasms': '乳腺肿瘤', 'Neutropenia': '中性粒细胞减少',
        'Arrhythmias, Cardiac': '心律失常', 'Drug Toxicity': '药物毒性', 'Lymphoma, Non-Hodgkin': '非霍奇金淋巴瘤',
        'Carcinoma, Hepatocellular': '癌, 肝细胞','Postoperative':'术后','Ototoxicity':'耳毒性','Testicular Neoplasms':'睾丸肿瘤',
        'Postoperative Nausea and Vomiting':'术后恶心呕吐','Ovarian Neoplasms':'卵巢肿瘤','Thrombocytopenia':'血小板减少症',
        'Infection':'传染','Gastrointestinal Neoplasms':'胃肠道肿瘤','Menopause':'更年期','overall survival':'总生存率',
        'Anemia':'贫血'
    }
    return options.get(english_word, f'echo {english_word} No_relevant_translation_available')
  
# 切面功能，装饰一下；
def English_to_Chinese(columns_list: List[str],sep: str):
    def english_to_chinese(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            df = func(*args,**kwargs)
            for columns in columns_list:
                df_temp = df[[columns]] # series 转 df
                for index,row in df_temp.iterrows():
                    line = sep.join([choose(ele) for ele in row[columns].split(sep)])
                    df[columns].iloc[index] = line
            return df
        return wrapper
    return english_to_chinese
# 切面功能，装饰一下；
def Handling_special_rs(rs_dict: Dict[str, List[Union[str, List[str]]]]):
    def handing_special_rs(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            df = func(*args,**kwargs)
            for index,row in df.iterrows():
                # print(row['检测位点'])
                # print(rs_dict.keys())
                if row['检测位点'] in rs_dict:
                    snpindel = f'{generate_location}/{sample_path}/{sample}.process.hg19_multiprocess.txt'
                    df_snpindel = pd.read_csv(snpindel,sep='\t')
                    if row['检测位点'] not in df_snpindel['avsnp150'].values:
                        df['基因型'].iloc[index] = rs_dict[row['检测位点']][1][0]   # 没突变是正常的；
                        df['用药提示'].iloc[index] = rs_dict[row['检测位点']][1][1]
                    else:
                        rs_VAF = df_snpindel[df_snpindel['avsnp150']==row['检测位点']]['VAF'].iloc[0] 
                        if float(rs_VAF.strip('%')) >= 90 or (float(rs_VAF.strip('%')) >= 40 and float(rs_VAF.strip('%')) <= 60):
                            df['基因型'].iloc[index] = rs_dict[row['检测位点']][3][0]   # 纯合
                            df['用药提示'].iloc[index] = rs_dict[row['检测位点']][3][1]
                        else:
                            df['基因型'].iloc[index] = rs_dict[row['检测位点']][2][0]   # 杂合
                            df['用药提示'].iloc[index] = rs_dict[row['检测位点']][2][1]
                    df['检测位点'].iloc[index] = rs_dict[row['检测位点']][0] # 特殊 rs号改为 UGT1A1 写法；
            return df
        return wrapper
    return handing_special_rs
# 切面功能，装饰一下；
def Delete_rows_with_None(columns_list: List[str]):
    def delete_rows_with_None(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            # 创建一个空列表用于存储要删除的行的索引
            rows_to_delete = []
            df = func(*args,**kwargs)
            for index,row in df.iterrows():
                for columns in columns_list: 
                    if row[columns] == 'None':
                        print('有None的行是',index,row)
                        rows_to_delete.append(index)
            df = df.drop(rows_to_delete)
            return df
        return wrapper
    return delete_rows_with_None
  
  
# just_rs.txt 从报告中来的。
def make_rs_address(): # 这一步或时间长，生成一次以后用他的结果就好了。
    # raw_df = pd.read_csv('just_rs.txt',header=None,sep=' ',names=['rs'])
    # for i in range(len(raw_df['rs'])):
    #     rs = raw_df['rs'].iloc[i]
    #     cmd = "cat /opt/annovar/humandb/hg19_avsnp150.txt | grep {rs}$ >> /home/chenyushao/chemo/rs/rs_address.txt".format(rs=rs)
    #     p = subprocess.Popen(cmd,shell=True)
    #     p.communicate()
    raw_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/just_rs.txt',header=None,sep=' ',names=['rs'])
    for i in range(len(raw_df['rs'])):
        rs = raw_df['rs'].iloc[i]
        cmd = "cat /opt/annovar/humandb/dbsnp.vcf | grep {rs}$'\t' >> /refhub/hg19/toolbox_and_RefFile/chemo/rs_address.txt".format(rs=rs)
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()

def drop_duplicate0():
    raw_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/rs_address.txt',sep='\t')
    raw_df = raw_df.drop_duplicates()
    raw_df.to_csv('/refhub/hg19/toolbox_and_RefFile/chemo/rs_address.txt',sep='\t',index=None)

def output_base_num():         
    # raw_df = pd.read_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',\
    # names=['chr','start','end','variant1','variant2','rs'])
    raw_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/shenghuifeng_rs_address.txt',header=None,sep='\t',\
        names=['chr','start','rs','variant1','variant2','unkown0','unkown1','comprehensive'])
    print(len(raw_df['rs']))
    #  记得切换进 call 突变的环境。start和end在1177位置，输出的位置就在1176.
    for i in range(len(raw_df['rs'])):
        chr,start,end,rs = raw_df['chr'].iloc[i], raw_df['start'].iloc[i],raw_df['start'].iloc[i],raw_df['rs'].iloc[i]
        print(chr,start,end,rs)
        bam = f'{generate_location}/{sample_path}/{sample_path}.markdup.bam'
        out = f'{generate_location}/{sample_path}/1p19q_generate'
        if i==0:
            cmd = f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
                  conda activate call_mutation_fbs && \
                  sambamba depth base -F '' -L chr{chr}:{start}-{end} {bam} > {out}/Check_for_specified_mutations.txt && \
                  conda deactivate"
        else:
            cmd = f"source /opt/miniconda3/etc/profile.d/conda.sh  && \
                  conda activate call_mutation_fbs && \
                  sambamba depth base -F '' -L chr{chr}:{start}-{end} {bam} | sed -n '2p' >> {out}/Check_for_specified_mutations.txt && \
                  conda deactivate"
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()


def process_output_base_num():
    # address_df = pd.read_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',\
    #           names=['chr','start','end','variant1','variant2','rs'])
    address_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/shenghuifeng_rs_address.txt',header=None,sep='\t',\
        names=['chr','start','rs','variant1','variant2','unkown0','unkown1','comprehensive'])   
    call_mutation_df = pd.read_csv('Check_for_specified_mutations.txt',sep='\t')
    # call_mutation_df['rs'] = address_df['rs'] #  这一步一定有问题。
    address_df['chr'] = 'chr'+address_df['chr'].astype(str)
    df_start_rs = address_df[['start', 'rs']]
    df_start_rs['rs'] = df_start_rs['rs'].astype(str)

    print("df_start_rs 是： ",df_start_rs)
    call_mutation_df = call_mutation_df.merge(df_start_rs, left_on=call_mutation_df['POS']+1, right_on='start', how='left')
    print(address_df['rs'])
    # for index,row in call_mutation_df.iterrows():
    #     print(df_start_rs[ df_start_rs['start']==row['start']])
    #     call_mutation_df['rs'].iloc[index] = df_start_rs[ df_start_rs['start']==row['start']]['rs']
    new_call_mutation_df = call_mutation_df[['rs','REF','POS','COV','A','C','G','T']]
    print('检查address_df： ',address_df)
    print('call_mutation_df 在这里：',call_mutation_df)
    print('new_call_mutation_df 在这里：',new_call_mutation_df)
    new_call_mutation_df['A_percent']\
    ,new_call_mutation_df['C_percent']\
    ,new_call_mutation_df['G_percent'],\
    new_call_mutation_df['T_percent'] = new_call_mutation_df['A']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['C']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['G']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['T']/new_call_mutation_df['COV']
    new_call_mutation_df['Genetype'] = None
    new_call_mutation_df['VAF'] = None
    dict_ = {}
    for i in range(len(new_call_mutation_df['rs'])):
        rs = new_call_mutation_df['rs'].iloc[i]
        ref = address_df[ address_df['rs']==rs]['variant1'].iloc[0]
        dict_['A'] = new_call_mutation_df['A_percent'].iloc[i]
        dict_['T'] = new_call_mutation_df['T_percent'].iloc[i]
        dict_['C'] = new_call_mutation_df['C_percent'].iloc[i]
        dict_['G'] = new_call_mutation_df['G_percent'].iloc[i]
        if dict_['A']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'AA'
            if ref == 'A': new_call_mutation_df['VAF'].iloc[i]=0
            else: new_call_mutation_df['VAF'].iloc[i]=1
        elif dict_['C']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'CC'
            if ref == 'C': new_call_mutation_df['VAF'].iloc[i]=0
            else: new_call_mutation_df['VAF'].iloc[i]=1
        elif dict_['T']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'TT'
            if ref == 'T': new_call_mutation_df['VAF'].iloc[i]=0
            else: new_call_mutation_df['VAF'].iloc[i]=1
        elif dict_['G']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'GG'
            if ref == 'G': new_call_mutation_df['VAF'].iloc[i]=0
            else: new_call_mutation_df['VAF'].iloc[i]=1
        else:
            # path = []
            # for key,value in dict_.items():
            #     if 0.3<=value and value<=0.7:
            #         path.append(key)
            # print(''.join(path))
            # new_call_mutation_df['Genetype'].iloc[i] = ''.join(path)
            
            rs = new_call_mutation_df['rs'].iloc[i]
            # print('看这里 rs 在这：',rs)
            # 加了个小补丁，以实际出现的情况为主；
            # print('看这里： ', address_df[ address_df['rs']==rs] )
            alt_list = address_df[ address_df['rs']==rs]['variant2'].iloc[0].split(',')
            alt = alt_list[0]
            for ele in alt_list:
                if new_call_mutation_df[ele].iloc[i] >= new_call_mutation_df[alt].iloc[i]:
                    alt = ele
            new_call_mutation_df['Genetype'].iloc[i] = address_df[ address_df['rs']==rs]['variant1'].iloc[0]+alt
            # if alt == ''.join(list(set(list(new_call_mutation_df['Genetype'].iloc[i])))):  # 全alt。
            #     new_call_mutation_df['VAF'].iloc[i] = 1
            # elif alt != ''.join(list(set(list(new_call_mutation_df['Genetype'].iloc[i])))) and len(''.join(list(set(list(new_call_mutation_df['Genetype'].iloc[i])))))==1:
            #     new_call_mutation_df['VAF'].iloc[i] = 0
            new_call_mutation_df['VAF'].iloc[i] = new_call_mutation_df[alt].iloc[i]/new_call_mutation_df['COV'].iloc[i]
    new_call_mutation_df = new_call_mutation_df[['rs','REF','POS','COV','A','C','G','T','Genetype','VAF']]
    df_result1 = new_call_mutation_df[~(new_call_mutation_df.REF.isin(['chrX','chrY']))]                                    # 求反集
    df_result1['chr_num'] = df_result1['REF'].str.extract(r'(\d+)').astype(int)   # 先处理1-22
    df_result1 = df_result1.sort_values(by=['chr_num','POS'])
    
    if not new_call_mutation_df[new_call_mutation_df['REF']=='chrX'].empty:                           # 处理xy。
        df_resultX = new_call_mutation_df[new_call_mutation_df.REF.isin(['chrX'])]
        df_resultX = df_resultX.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1,df_resultX])
    if not new_call_mutation_df[new_call_mutation_df['REF']=='chrY'].empty:
        df_resultY = new_call_mutation_df[new_call_mutation_df.REF.isin(['chrY'])]
        df_resultY = df_resultY.sort_values(by=['start'])
        df_result1 = pd.concat([df_result1,df_resultY])
    df_result1 = df_result1.drop(columns=['chr_num'])
    print(df_result1)
   
    # 这个打了个补丁，把vaf 1和 0 的值 反过来了；临时处理的；就不改动前面的生成逻辑了。
    df_result1['vaf'] = df_result1['VAF'] 
    df_result1.loc[df_result1['VAF'] == 1, 'vaf'] = 0
    df_result1.loc[df_result1['VAF'] == 0, 'vaf'] = 1
    df_result1.drop('VAF', axis=1, inplace=True)
    df_result1 = df_result1.rename(columns={'vaf': 'VAF'})
    df_result1.to_csv(f'{generate_location}/{sample_path}/1p19q_generate/process_output_base_num.txt',sep='\t',index=None)
    df_result2 = df_result1[['REF','POS','rs','VAF']]
    df_result2.to_csv(f'{generate_location}/{sample_path}/1p19q_generate/1p19q_process_output_base_num.txt',sep='\t',index=None,header=['chr','pos','rs','VAF'])
    
def drop_duplicate():
    raw_df = pd.read_csv(f'{generate_location}/{sample_path}/1p19q_generate/process_output_base_num.txt',sep='\t')
    raw_df = raw_df.drop_duplicates()
    raw_df.to_csv(f'{generate_location}/{sample_path}/1p19q_generate/row_process_output_base_num.txt',sep='\t',index=None)
    raw_df.to_csv(f'{generate_location}/{sample_path}/1p19q_generate/process_output_base_num.txt',sep='\t',index=None)
    
def Make_chemo_csv_Prepare_for_summery():
    
    raw_df = pd.read_csv(f'{generate_location}/{sample_path}/chemo_generate/row_process_output_base_num.txt',sep='\t')
    # print(raw_df['rs'],raw_df['Genetype'])
    df_rs_genetype = pd.read_excel(f'/refhub/ref/chemo/chemodrug.var.annotation.xlsx', sheet_name=None)
    df_rs_drug = pd.read_excel(f'/refhub/ref/chemo/chemodrug.clinical.annotation.xlsx', sheet_name=None)
    df0,df1 = df_rs_genetype['Sheet1'],df_rs_drug['rs_drug_isUnique']
    with open(f'{generate_location}/{sample_path}/chemo_generate/temp_process_output_base_num.txt','w')as f:
        for index, row in raw_df.iterrows():
            drug,gene,rs,genetype,phenotype,level_of_evidence,medication_reminder = \
                None,None,None,None,None,None,None
            # 以下为先找 chemodrug.var.annotation.xlsx 表。
            # df_temp = df0[(df0['Variant']==row['rs']) & (df0['Allele']==row['Genetype'])]
            # # print(df_temp)
            # for index0,row0 in df_temp.iterrows():
            #     drug,gene,medication_reminder = row0['Drug'],row0['Gene'],row0['Review']
            #     # print(drug,gene,medication_reminder)
            #     df_temp1 = df1[(df1['Variant/Haplotypes']==row['rs']) & (df1['Drug(s)']==drug)]
            #     rs,genetype = row['rs'],row['Genetype']
            #     for index1,row1 in df_temp1.iterrows():
            #         phenotype,level_of_evidence = row1['Phenotype(s)'],row1['Level of Evidence']
            #         # print('drug is: ',drug,'gene is: ',gene,'rs is: ',rs,'genetype is: ',genetype,'phenotype is: ',phenotype,'level_of_evidence is: ',level_of_evidence,'medication_reminder is: ',medication_reminder)
            #         print(drug,gene,rs,genetype,phenotype,level_of_evidence,medication_reminder)
            #         line_str = '\t'.join(list(map(str,[drug,gene,rs,genetype,phenotype,level_of_evidence,medication_reminder])))
            #         f.write(line_str+'\n')
            # 以下为先找 chemodrug.clinical.annotation.xlsx 表。
            print(row['rs'])
            df_temp = df1[df1['Variant/Haplotypes']==row['rs']]
            print(df_temp)
            rs,genetype = row['rs'],row['Genetype']
            for index0,row0 in df_temp.iterrows():
                phenotype,level_of_evidence,gene,drug = row0['Phenotype Category'],row0['Level of Evidence'],row0['Gene'],row0['Drug(s)']
                # GA AG 不要影响匹配；
                # df_temp1 = df0[(df0['Variant']==row['rs']) & (set(list(df0['Allele']))==set(list(row['Genetype']))) & (df0['Drug']==row0['Drug(s)'])]
                reversal_genetype = row['Genetype'][1]+row['Genetype'][0]
                df_temp1 = df0[(df0['Variant']==row['rs']) & (df0['Allele'].isin([row['Genetype'],reversal_genetype])) & (df0['Drug']==row0['Drug(s)'])]
                if not df_temp1.empty:
                    for index1,row1 in df_temp1.iterrows():
                        medication_reminder = row1['Review']
                        line_str = '\t'.join(list(map(str,[drug,gene,rs,genetype,phenotype,level_of_evidence,medication_reminder])))
                        f.write(line_str+'\n')
                else:
                    # genetype = None 若果写实际 检测出的值，这里就需要注释掉。
                    line_str = '\t'.join(list(map(str,[drug,gene,rs,genetype,phenotype,level_of_evidence,medication_reminder])))
                    f.write(line_str+'\n')
                    
    raw_df = pd.read_csv(f'{generate_location}/{sample_path}/chemo_generate/temp_process_output_base_num.txt',sep='\t',header=None)
    raw_df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None,header=['药物名称','检测基因','检测位点','基因型','类别','证据等级','用药提示'])
    raw_df = pd.read_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t')
    
    # 按照指定顺序排序； 
    raw_df['sort'] = raw_df['检测位点']+raw_df['药物名称']
    df1['sort'] = df1['Variant/Haplotypes']+df1['Drug(s)']
    order_list = df1['sort'].tolist()
    # 将'sort'列转换为Categorical数据类型，并指定排序顺序
    raw_df['sort'] = pd.Categorical(raw_df['sort'], categories=order_list, ordered=True)
    # 根据'A'列的顺序对DataFrame进行排序
    raw_df = raw_df.sort_values(by='sort')
    raw_df = raw_df.drop(columns=['sort'])
    raw_df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None)
    
    @Delete_rows_with_None(columns_list=['用药提示'])
    @Handling_special_rs(rs_dict={
      'rs11280056':['rs11280056',['TTAAAGTTA/TTAAAGTTA','疗效减弱'],['TTAAAGTTA/del','疗效增强'],['del/del','疗效增强']],\
      'rs3064744':['UGT1A1*28',['*1/*1','剂量增加'],['*1/*28','剂量增加'],['*28/*28','剂量减少']],\
      'rs4148323':['UGT1A1*6',['*1/*1','毒性一般'],['*1/*6','毒性增强'],['*6/*6','毒性增强']]
      })
    @English_to_Chinese(columns_list=['药物名称','类别'],sep=';')
    def read_df(path):
        return  pd.read_csv(path,sep='\t')
    df = read_df(path=f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt')
    df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None)

def qc():
    QC = tool()
    base_quality,inser_size_peak,duplication_rate = QC.process_fastp_log(sample,log_path,generate_location)     # 质量控制。
    if int(inser_size_peak) < 60:
        with open(f'{log_path}/quality_control/1p19q_Quality_Control.txt','a+')as f0:                      # 不符合条件，就停止后续流程。
            f0.write('fastp 结果质控不合格！！'+"\n")
            f0.write('base_quality: '+str(base_quality)+'\n')
            f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
            f0.write('duplication_rate: '+str(duplication_rate)+'\n')
    else:
        with open(f'{log_path}/quality_control/1p19q_Quality_Control.txt','a+')as f0:
            f0.write('fastp 结果质控合格！！'+"\n")
            f0.write('base_quality: '+str(base_quality)+'\n')
            f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
            f0.write('duplication_rate: '+str(duplication_rate)+'\n')
    mapped,coverage,ontarget,depth,cleandepth = QC.process_bam(sample,log_path,sample_path,generate_location,bed) 
    if float(ontarget.split("%")[0]) < 40:                                                          
        with open(f'{log_path}/quality_control/1p19q_Quality_Control.txt','a+')as f0:                      # 不符合条件，就停止后续流程。
            f0.write('dedup_markdup 的bam 结果质控不合格！！'+"\n")
            f0.write('mapped: '+str(mapped)+'\n')
            f0.write('coverage: '+str(coverage)+'\n')
            f0.write('ontarget: '+str(ontarget)+'\n')
            f0.write('depth: '+str(depth)+'\n')
            f0.write('cleandepth: '+str(cleandepth)+'\n')
    else:
        with open(f'{log_path}/quality_control/1p19q_Quality_Control.txt','a+')as f0:
            f0.write('dedup_markdup 的bam 结果质控合格！！'+"\n")
            f0.write('mapped: '+str(mapped)+'\n')
            f0.write('coverage: '+str(coverage)+'\n')
            f0.write('ontarget: '+str(ontarget)+'\n')
            f0.write('depth: '+str(depth)+'\n')
            f0.write('cleandepth: '+str(cleandepth)+'\n')

def plot_pic0():
    import matplotlib
    # 设置Matplotlib的后端为Qt5
    matplotlib.use('agg')
    # 导入其他相关模块和库
    import matplotlib.pyplot as plt
    plt.figure() 
    # plt.subplot(1, 2, 1)  # 子图1，1行2列，第1个位置
    # 填写数据
    df = pd.read_csv(f'{generate_location}/{sample_path}/1p19q_generate/1p19q_process_output_base_num.txt',sep='\t')
    # print(df[df['chr']=='chr19']['pos','VAF'])
    df['VAF'] =df['VAF']*100
    x,y = df[df['chr']=='chr19']['pos'].tolist(),df[df['chr']=='chr19']['VAF'].tolist()
    # x = [47112648, 48833800,56030428]  # 横坐标
    # y = [25.00, 36.59,29.63]  # 纵坐标
    plt.scatter(x, y)
    
    # 添加辅助线
    plt.axhline(y=90, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=60, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=40, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=10, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axvline(x=25000000, color=(194/255, 194/255, 194/255), linestyle='-', label='cen')
    
    # 设置图表标题和坐标轴标签
    plt.title('Chromosome 19')
    plt.xlabel('Chromosome position (bp)')
    plt.ylabel('Allelic Frequency (%)')
    
    # 设置刻度范围
    plt.xlim(0, 65000000)
    plt.ylim(0, 110)
    plt.xticks(range(-5000000, 65000000, 10000000))
    plt.yticks(range(-10, 110, 10))
    plt.ticklabel_format(style='plain', axis='x')
    plt.grid(True,which='major',axis='y')
    
    # 文字
    plt.legend()
    # plt.text(10000000, 105, '19p', color='red', ha='right')
    plt.text(45000000, 105, '19q', color='red', ha='left')
    # 保存图像到指定位置
    save_path = f"{generate_location}/{sample_path}/"+"1p19q_generate/chr19_image.png" # 替换为您想要保存的路径和文件名
    plt.savefig(save_path)
    
def plot_pic1():
    import matplotlib
    # 设置Matplotlib的后端为Qt5
    matplotlib.use('agg')
    # 导入其他相关模块和库
    import matplotlib.pyplot as plt
    plt.figure() 
    # plt.subplot(1, 2, 2)  # 子图1，1行2列，第1个位置
    # 填写数据
    df = pd.read_csv(f'{generate_location}/{sample_path}/1p19q_generate/1p19q_process_output_base_num.txt',sep='\t')
    df['VAF'] =df['VAF']*100
    x,y = df[df['chr']=='chr1']['pos'].tolist(),df[df['chr']=='chr1']['VAF'].tolist()
    # x = [47112648, 48833800,56030428]  # 横坐标
    # y = [25.00, 36.59,29.63]  # 纵坐标
    plt.scatter(x, y)
    
    # 添加辅助线
    plt.axhline(y=90, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=60, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=40, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axhline(y=10, color=(13/255, 83/255, 138/255), linestyle='-')
    plt.axvline(x=150000000, color=(194/255, 194/255, 194/255), linestyle='-', label='cen')
    
    # 设置图表标题和坐标轴标签
    plt.title('Chromosome 1')
    plt.xlabel('Chromosome position (bp)')
    plt.ylabel('Allelic Frequency (%)')
    
    # 设置刻度范围
    plt.xlim(0, 250000000)
    plt.ylim(0, 110)
    plt.xticks(range(0, 250000000, 50000000))
    plt.yticks(range(-10, 110, 10))
    plt.ticklabel_format(style='plain', axis='x')
    plt.grid(True,which='major',axis='y')
    
    # 文字
    plt.legend()
    plt.text(50000000, 105, '1p', color='red', ha='right')
    # plt.text(20000000, 105, '1q', color='red', ha='left')
    # 保存图像到指定位置
    save_path = f"{generate_location}/{sample_path}/"+"1p19q_generate/chr1_image.png" # 替换为您想要保存的路径和文件名
    plt.savefig(save_path)

def concat_plot():
    # 以下注释部分为 上下拼接。 
    # from PIL import Image
    # # 打开两张图片
    # image1 = Image.open(f"{generate_location}/{sample_path}/"+"1p19q_generate/chr1_image.png")
    # image2 = Image.open(f"{generate_location}/{sample_path}/"+"1p19q_generate/chr19_image.png")
    # # 获取两张图片的宽度和高度
    # width1, height1 = image1.size
    # width2, height2 = image2.size
    # # 确定新图片的宽度和高度
    # new_width = max(width1, width2)
    # new_height = height1 + height2
    # # 创建一个新的空白图片
    # new_image = Image.new('RGB', (new_width, new_height))
    # # 将image1粘贴到新图片的上半部分
    # new_image.paste(image1, (0, 0))
    # # 将image2粘贴到新图片的下半部分
    # new_image.paste(image2, (0, height1))
    # # 保存拼接后的图片
    # new_image.save('1p19q_image.jpg')
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(13, 6.5)) # 设置画布宽度。
    def line_deccor(plt):
        # plt.xlabel('Chromosome position (bp)')
        # plt.ylabel('Allelic Frequency (%)')
        # Add gray background for y-values between 40 and 60 using RGB color
        gray_color = (0.5, 0.5, 0.5)  # RGB values for gray color
        plt.axhspan(10, 40, facecolor=gray_color, alpha=0.5)
        plt.ylim(0, 110)
        plt.yticks(range(-10, 110, 10))
        plt.grid(True, which='major', axis='y')

    def plot_chr1(plt):
        # x = [47112648, 48833800, 56030428]
        # y = [25.00, 36.59, 29.63]
        # plt.subplot(1, 2, 1)
        # plt.scatter(x, y)
        # plt.xlim(0, 65000000)
        # plt.xticks(range(-5000000, 65000000, 10000000))
        # plt.legend()
        # plt.text(10000000, 105, '19p', color='red', ha='right')
        # plt.text(45000000, 105, '19q', color='red', ha='left')
        # line_deccor(plt)
        plt.subplot(1, 2, 1)
        df = pd.read_csv(f'{generate_location}/{sample_path}/1p19q_generate/1p19q_process_output_base_num.txt',sep='\t')
        df['VAF'] =df['VAF']*100
        x,y = df[df['chr']=='chr1']['pos'].tolist(),df[df['chr']=='chr1']['VAF'].tolist()
        plt.scatter(x, y,color=(41/255, 84/255, 117/255), zorder=10)
        # 添加辅助线
        plt.axhline(y=100, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=90, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=60, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=40, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=10, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=0, color=(41/255, 84/255, 117/255), linestyle='-')
        # Add gray background for y-values between 10 and 40 using RGB color
        plt.axhspan(10, 40, facecolor=(241 / 255, 241 / 255, 241 / 255), alpha=0.5)
        plt.axhspan(60, 90, facecolor=(241 / 255, 241 / 255, 241 / 255), alpha=0.5)
        # plt.axvline(x=150000000, color=(194/255, 194/255, 194/255), linestyle='-', label='cen')
        # 设置图表标题和坐标轴标签
        plt.title('Chromosome 1p')
        plt.xlabel('Chromosome position (bp)')
        plt.ylabel('Allelic Frequency (%)')
        # 设置刻度范围
        # plt.xlim(0, 150000000)
        plt.ylim(0, 110)
        # plt.xticks(range(0, 150000000, 50000000))
        yticks=range(-10, 110, 10)
        # 隐藏 -10 刻度线
        yticks_labels = ['' if tick == -10 else str(tick) for tick in yticks]
        # 应用自定义刻度线标签
        plt.yticks(yticks, yticks_labels)
        # 隐藏x轴坐标。
        plt.xticks([])
        # Disable scientific notation on x-axis tick labels
        plt.ticklabel_format(style='plain', axis='x', useOffset=False)
        
        # Change default gridlines to dashed lines 
        plt.grid(True, which='major', axis='y', linestyle='--')
        # 文字
        plt.legend()
        # plt.text(50000000, 105, '1p', color='red', ha='right')
    
    def plot_chr19(plt):
        # x = [47112648, 48833800, 56030428]
        # y = [25.00, 36.59, 29.63]
        # plt.subplot(1, 2, 2)
        # plt.scatter(x, y)
        # plt.xlim(0, 65000000)
        # plt.xticks(range(-5000000, 65000000, 10000000))
        # plt.legend()
        # plt.text(10000000, 105, '19p', color='red', ha='right')
        # plt.text(45000000, 105, '19q', color='red', ha='left')
        # line_deccor(plt)
        plt.subplot(1, 2, 2)
        df = pd.read_csv(f'{generate_location}/{sample_path}/1p19q_generate/1p19q_process_output_base_num.txt',sep='\t')
        df['VAF'] =df['VAF']*100
        x,y = df[df['chr']=='chr19']['pos'].tolist(),df[df['chr']=='chr19']['VAF'].tolist()
        plt.scatter(x, y,color=(41/255, 84/255, 117/255), zorder=10)
        # 设置图表标题和坐标轴标签
        plt.title('Chromosome 19q')
        plt.xlabel('Chromosome position (bp)')
        # plt.ylabel('Allelic Frequency (%)')
        # plt.axvline(x=25000000, color=(194 / 255, 194 / 255, 194 / 255), linestyle='-', label='cen')
        # 设置刻度范围
        # plt.xlim(0, 65000000)
        plt.ylim(0, 110)
        # plt.xticks(range(-5000000, 65000000, 10000000))
        yticks=range(-10, 110, 10)
        # 隐藏 -10 刻度线
        yticks_labels = ['' if tick == -10 else str(tick) for tick in yticks]
        # 应用自定义刻度线标签
        plt.yticks(yticks, yticks_labels)
        # plt.ticklabel_format(style='plain', axis='x')
        # 添加辅助线
        plt.axhline(y=100, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=90, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=60, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=40, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=10, color=(41/255, 84/255, 117/255), linestyle='-')
        plt.axhline(y=0, color=(41/255, 84/255, 117/255), linestyle='-')
        # Add gray background for y-values between 10 and 40 using RGB color
        plt.axhspan(10, 40, facecolor=(241 / 255, 241 / 255, 241 / 255), alpha=0.5)
        plt.axhspan(60, 90, facecolor=(241 / 255, 241 / 255, 241 / 255), alpha=0.5)
        # 隐藏x轴坐标。
        plt.xticks([])
        # Disable scientific notation on x-axis tick labels
        plt.ticklabel_format(style='plain', axis='x', useOffset=False)
        # Change default gridlines to dashed lines 
        plt.grid(True, which='major', axis='y', linestyle='--')
        # 文字
        plt.legend()
        # plt.text(10000000, 105, '19p', color='red', ha='right')
        # plt.text(45000000, 105, '19q', color='red', ha='left')

    plot_chr1(plt)
    plot_chr19(plt)
    plt.show()
    save_path = f"{generate_location}/{sample_path}/"+"1p19q_generate/1p19q_image.png" # 替换为您想要保存的路径和文件名
    plt.savefig(save_path)


def main():
    qc()
    
    tmp_dir = f"{generate_location}/{sample_path}/"+"1p19q_generate"
    sample_dir = f"{generate_location}/{sample_path}"
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    # make_rs_address()                # 生成以后我手动删除了两行。生成一次以后 用生成结果就好了，不用反复运行。
    drop_duplicate0()
    output_base_num()
    process_output_base_num()
    drop_duplicate()
    plot_pic1()
    plot_pic0()
    concat_plot()
    # Make_chemo_csv_Prepare_for_summery()

if __name__=="__main__":
    main()
    
    
