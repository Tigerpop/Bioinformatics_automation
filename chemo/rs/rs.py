#coding=utf8
import pandas as pd 
import subprocess

def make_rs_address():
    raw_df = pd.read_csv('just_rs.txt',header=None,sep=' ',names=['rs'])
    for i in range(len(raw_df['rs'])):
        rs = raw_df['rs'].iloc[i]
        cmd = "cat /opt/annovar/humandb/hg19_avsnp150.txt | grep {rs}$ >> /home/chenyushao/chemo/rs/rs_address.txt".format(rs=rs)
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()

def drop_duplicate():
    raw_df = pd.read_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',\
    names=['chr','start','end','variant1','variant2','rs'])
    raw_df.drop_duplicates(subset=['start'],keep='first',inplace=True)
    raw_df.to_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',index=None)

def output_base_num():         
    raw_df = pd.read_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',\
    names=['chr','start','end','variant1','variant2','rs'])
    #  记得切换进 call 突变的环境。start和end在1177位置，输出的位置就在1176.
    for i in range(len(raw_df['rs'])):
        chr,start,end,rs = raw_df['chr'].iloc[i], raw_df['start'].iloc[i],raw_df['end'].iloc[i],raw_df['rs'].iloc[i]
        bam = '~/py_generate/2022WSSW000970/2022WSSW000970-T/E100065602_L01_2022WSSW000970-T/E100065602_L01_2022WSSW000970-T.dedup.bam'
        out = '~/chemo/rs'
        if i==0:
            cmd = "sambamba depth base -F '' -L chr{chr}:{start}-{end} {bam} >> {out}/Check_for_specified_mutations.txt"\
            .format(chr=chr,start=start,end=end,bam=bam,out=out)
        else:
            cmd = "sambamba depth base -F '' -L chr{chr}:{start}-{end} {bam} | sed -n '2p' >> {out}/Check_for_specified_mutations.txt"\
            .format(chr=chr,start=start,end=end,bam=bam,out=out)
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()

def process_output_base_num():
    address_df = pd.read_csv('/home/chenyushao/chemo/rs/rs_address.txt',header=None,sep='\t',\
              names=['chr','start','end','variant1','variant2','rs'])
    call_mutation_df = pd.read_csv('Check_for_specified_mutations.txt',sep='\t')
    call_mutation_df['rs'] = address_df['rs']
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
    for i in range(len(call_mutation_df['rs'])):
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
            path = []
            for key,value in dict_.items():
                if 0.3<=value and value<=0.7:
                    path.append(key)
            print(''.join(path))
            new_call_mutation_df['Genetype'].iloc[i] = ''.join(path)
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
    df_result1.to_csv('/home/chenyushao/chemo/rs/process_output_base_num.txt',sep='\t',index=None)
    
if __name__=="__main__":
    # make_rs_address()                # 生成以后我手动删除了两行。
    # drop_duplicate()
    # output_base_num()
    process_output_base_num()
