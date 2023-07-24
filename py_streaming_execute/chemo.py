#coding=utf8
import pandas as pd 
import subprocess,os,sys
import functools
from typing import Dict, List, Union

sample = sys.argv[1]  # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]

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
    raw_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/rs_address.txt',header=None,sep='\t',\
        names=['chr','start','rs','variant1','variant2','unkown0','unkown1','comprehensive'])
    print(len(raw_df['rs']))
    #  记得切换进 call 突变的环境。start和end在1177位置，输出的位置就在1176.
    for i in range(len(raw_df['rs'])):
        chr,start,end,rs = raw_df['chr'].iloc[i], raw_df['start'].iloc[i],raw_df['start'].iloc[i],raw_df['rs'].iloc[i]
        print(chr,start,end,rs)
        bam = f'{generate_location}/{sample_path}/{sample_path}.markdup.bam'
        out = f'{generate_location}/{sample_path}/chemo_generate'
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
    address_df = pd.read_csv('/refhub/hg19/toolbox_and_RefFile/chemo/rs_address.txt',header=None,sep='\t',\
        names=['chr','start','rs','variant1','variant2','unkown0','unkown1','comprehensive'])   
    call_mutation_df = pd.read_csv('Check_for_specified_mutations.txt',sep='\t')
    # call_mutation_df['rs'] = address_df['rs'] #  这一步一定有问题。
    call_mutation_df = call_mutation_df.merge(address_df[['start', 'rs']], left_on=call_mutation_df['POS']+1, right_on='start', how='left')
    new_call_mutation_df = call_mutation_df[['rs','REF','POS','COV','A','C','G','T']]
    new_call_mutation_df['A_percent']\
    ,new_call_mutation_df['C_percent']\
    ,new_call_mutation_df['G_percent'],\
    new_call_mutation_df['T_percent'] = new_call_mutation_df['A']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['C']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['G']/new_call_mutation_df['COV']\
                                        ,new_call_mutation_df['T']/new_call_mutation_df['COV']
    new_call_mutation_df['Genetype'] = None
    dict_ = {}
    for i in range(len(new_call_mutation_df['rs'])):
        dict_['A'] = new_call_mutation_df['A_percent'].iloc[i]
        dict_['T'] = new_call_mutation_df['T_percent'].iloc[i]
        dict_['C'] = new_call_mutation_df['C_percent'].iloc[i]
        dict_['G'] = new_call_mutation_df['G_percent'].iloc[i]
        if dict_['A']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'AA'
        elif dict_['C']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'CC'
        elif dict_['T']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'TT'
        elif dict_['G']>0.9:
            new_call_mutation_df['Genetype'].iloc[i] = 'GG'
        else:
            # path = []
            # for key,value in dict_.items():
            #     if 0.3<=value and value<=0.7:
            #         path.append(key)
            # print(''.join(path))
            # new_call_mutation_df['Genetype'].iloc[i] = ''.join(path)
            rs = new_call_mutation_df['rs'].iloc[i]
            print(rs)
            # 加了个小补丁，以实际出现的情况为主；
            alt_list = address_df[ address_df['rs']==rs]['variant2'].iloc[0].split(',')
            alt = alt_list[0]
            for ele in alt_list:
                print('检查点： ele ,alt 分别是',ele,alt)
                # print(new_call_mutation_df)
                # {ele, alt} <= {'A', 'T', 'C', 'G'} and
                if {ele, alt} <= {'A', 'T', 'C', 'G'} and new_call_mutation_df[ele].iloc[i] >= new_call_mutation_df[alt].iloc[i]:
                    alt = ele
            new_call_mutation_df['Genetype'].iloc[i] = address_df[ address_df['rs']==rs]['variant1'].iloc[0]+alt
    new_call_mutation_df = new_call_mutation_df[['rs','REF','POS','COV','A','C','G','T','Genetype']]
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
    df_result1.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None)

def drop_duplicate():
    raw_df = pd.read_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t')
    raw_df = raw_df.drop_duplicates()
    raw_df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/row_process_output_base_num.txt',sep='\t',index=None)
    raw_df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None)
    
def Make_chemo_csv_Prepare_for_summery():
# 化药部分已经得出了 rs位点 以及 genotype ；

# 在表 chemodrug.var.annotation.xlsx 中 （rs，genotype）不是unique的，但是依然通过他们来定位其它元素；
    # 例如： rs1801131，GG 就会定位出 四个不同的 drug，但是依然用 这个drug 的 series 进行接下来的定位，
    # 就是一组 rs，genotype 对应的药物有多个。
    # 事实上 (rs,drugs) 是unique的。
# 在表 chemodrug.clinical.annotation.xlsx 中 (rs,drugs) 是unique的，通过他们来定位其它元素；

# 表 chemodrug.clinical.annotation.xlsx 中的 drugs 可以从 chemodrug.var.annotation.xlsx 中 通过（rs，genotype）定位出来；

# 步骤：
# 1、在表 chemodrug.clinical.annotation.xlsx 中 (rs) 选出 phenotype类别、证据等级；
# 2、在表 chemodrug.var.annotation.xlsx 中 (rs，genotype) 选出 drugs、gene、用药提示,找不到就空着；
# 3、将新表 作为 chemo 被收集进 summery；
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
    # 当 ordered=True 时，未知的值会被视为最大值，因此会在排序结果的末尾。
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
                    
def main():
    tmp_dir = f"{generate_location}/{sample_path}/"+"chemo_generate"
    sample_dir = f"{generate_location}/{sample_path}"
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    # make_rs_address()                # 生成以后我手动删除了两行。生成一次以后 用生成结果就好了，不用反复运行。
    drop_duplicate0()
    output_base_num()
    process_output_base_num()
    drop_duplicate()
    Make_chemo_csv_Prepare_for_summery()

if __name__=="__main__":
    main()
    
    
