#coding=utf8
import pandas as pd 
import subprocess,os,sys


sample = sys.argv[1]  # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]


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
                if new_call_mutation_df[ele].iloc[i] >= new_call_mutation_df[alt].iloc[i]:
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
    raw_df.to_csv(f'{generate_location}/{sample_path}/chemo_generate/process_output_base_num.txt',sep='\t',index=None)

if __name__=="__main__":
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
