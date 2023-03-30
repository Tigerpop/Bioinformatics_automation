#coding=utf8 
import pandas as pd 
import os,re,subprocess
import warnings 
warnings.filterwarnings('ignore')

df_snp_bed = pd.read_csv('SNP-BED-addmsi.csv',sep=',')
df_snp_bed['S'] = df_snp_bed['S'] - 100
df_snp_bed['E'] = df_snp_bed['E'] + 100
df_snp_bed = df_snp_bed[df_snp_bed['Target-name'].str.match('^rs')]
df_snp_bed.to_csv('SNP-BED.bed',sep='\t',header=None,index=None)

# cmd = 'bedtools getfasta -fi ucsc.hg19.fasta -bed SNP-BED.bed > SNP-BED.fasta'
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()

# # 根据目标fasta文件制作bait探针 这一步很慢，挂后台跑。
# cmd = 'mrbait -b 120 -A SNP-BED.fasta -T 16' 
# p = subprocess.Popen(cmd,shell=True)  
# p.communicate()

# # 读baits.fasta 文件 ，把baits.fasta文件中 Locus23 改为第23行的SNP-BED.bed 中的 rs 号。
# # 因为 Locus 从1开始计数，而python默认从0开始计数，所以 Locusxxx -1 才是 python中的index。
# df_snp_bed.reset_index(inplace=True)
# print(df_snp_bed)
# with open('./baits.fasta','r')as f,open('./rename_baits.fasta','w')as f0:
#     for ele in f:
#         if ele[0]=='>':
#             index = int(re.match(r'^>Locus([0-9]+?)_',ele).group(1)) - 1
#             rs = df_snp_bed.iloc[index]['Target-name']
#             ele = ele.replace(f"Locus{index+1}",rs)
#             # print(ele)
#         f0.write(ele)

# cmd = 'bwa mem  /refhub/hg19/human_genome_index/gatk_hg19 rename_baits.fasta  > SNP-BED.sam '
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()
# cmd = 'bedtools bamtobed -i SNP-BED.sam > SNP-BED_rs_build.bed '
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()

# 排序.
def sort_chr_start(df_result,output='sorted_SNP-BED_rs_build.bed'):
    print(df_result)
    # 'https://cloud.tencent.com/developer/ask/sof/96816'
    df_result1 = df_result[~(df_result.chr.isin(['chrX','chrY']))]              #  ~是求反集。
    df_result1['chr_num'] = df_result1['chr'].str.extract(r'(\d+)').astype(int) # 仅仅处理1-22基因，xy后面加上去。
    df_result1 = df_result1.sort_values(by=['chr_num','S'])

    if not df_result[df_result['chr']=='chrX'].empty:                           # 处理xy。
        df_resultX = df_result[df_result.chr.isin(['chrX'])]
        df_resultX = df_resultX.sort_values(by=['S'])
        df_result1 = pd.concat([df_result1,df_resultX])
    if not df_result[df_result['chr']=='chrY'].empty:
        df_resultY = df_result[df_result.chr.isin(['chrY'])]
        df_resultY = df_resultY.sort_values(by=['S'])
        df_result1 = pd.concat([df_result1,df_resultY])
    df_result1 = df_result1.drop(columns=['chr_num'])                           # 删除排序工具字段。
    useful_chr_list = ['chr'+str(i) for i in range(1,23)]
    useful_chr_list.extend(['chrX','chrY'])
    df_result1 = df_result1[df_result1.chr.isin(useful_chr_list)]               # 删除1-22 x y 之外的chr。
    df_result1.to_csv(output,sep='\t',index=False,header=None)
# df_SNP_BED_rs_build_bed = pd.read_csv('SNP-BED_rs_build.bed',sep='\t',header=None,names=['chr','S','E','rs_bait','60','direct'])
# df_SNP_BED_rs_build_bed[['rs','target','bait']] = df_SNP_BED_rs_build_bed['rs_bait'].str.split('_',expand=True)
# df_SNP_BED_rs_build_bed = df_SNP_BED_rs_build_bed[['chr','S','E','rs','bait']]
# # print(df_SNP_BED_rs_build_bed)
# sort_chr_start(df_SNP_BED_rs_build_bed) 

# 求到原始rs 位置的 距离，选距离rs位置 更近的bait 打上标签。
def add_lable():
    df_raw_bed = pd.read_csv('SNP-BED-addmsi.csv',sep=',')
    df_sorted_bed = pd.read_csv('sorted_SNP-BED_rs_build.bed',sep='\t',header=None,names=['chr','S','E','rs','bait'])
    print(df_raw_bed)
    print(df_sorted_bed)
    grouped = df_sorted_bed.groupby('rs')
    temp_list = []
    for x in grouped.groups: # get_group(x) 结果是df
        df_temp = grouped.get_group(x) 
        center = df_raw_bed[df_raw_bed['Target-name']==df_temp['rs'].iloc[0]]['S'].iloc[0]
        df_temp['distance'] = abs((df_temp['S']+df_temp['E'])/2 - center)
        df_temp['distance'] = df_temp['distance'].apply(lambda x: 'Nearest' if x==df_temp['distance'].min() else '-')
        temp_list.append(df_temp)
    df_result = pd.concat(temp_list)
    df_result.to_csv('add_lable_sorted_SNP-BED_rs_build.bed',sep='\t',index=False,header=None)
# add_lable()
# df_add_lable_bed = pd.read_csv('add_lable_sorted_SNP-BED_rs_build.bed',sep='\t',header=None,names=['chr','S','E','rs','bait','distance'])
# sort_chr_start(df_add_lable_bed,output='add_lable_sorted_SNP-BED_rs_build.bed') 


# 用 blastn 做探针 匹配唯一性的判定。 
# # 生成 blastn 会用到的 ucsc.hg19.fasta.ndb 等一大堆文件，生成一次之后就能反复用了。
# # /opt/blast/bin/makeblastdb -parse_seqids -dbtype nucl -in /refhub/hg19/fa/fa/ucsc.hg19.fasta
# 用blastn 验证baits探针 的 唯一性。-db 指定ucsc.hg19.fasta.ndb 等一大堆文件 的前缀，
# cmd = '/opt/blast/bin/blastn \
#        -db ~/doctor_assign_tasks/mrbait_generate_bed/easy/hg19/ucsc.hg19.fasta \
#        -query ~/doctor_assign_tasks/mrbait_generate_bed/rename_baits.fasta \
#        -out blastn_test.out \
#        -outfmt 7 \
#        -num_threads 5'
# p = subprocess.Popen(cmd,shell=True)
# p.communicate()
# df_add_lable_bed = pd.read_csv('add_lable_sorted_SNP-BED_rs_build.bed',sep='\t',header=None,names=['chr','S','E','rs','bait','distance'])
# df_add_lable_bed['unique'] = 'N'
# with open('./blastn_test.out','r')as f:   # 两行两行读，前一行是'# 1 hits found\n' 后一行是rs开头，就判定唯一。
#     pre = f.readline()
#     print(pre)
#     for line in f: #从第二行 开始读。
#         if pre=='# 1 hits found\n' and re.match('^rs',line)!=None:
#             rs_target_bait = line.split('\t')[0].split('_')
#             rs,bait = rs_target_bait[0],rs_target_bait[2]
#             # print(rs,bait)
#             df_add_lable_bed.loc[(df_add_lable_bed['rs']==rs) & (df_add_lable_bed['bait']==bait), 'unique'] = 'Y'
#             # print(df_add_lable_bed[(df_add_lable_bed['rs']==rs) & (df_add_lable_bed['bait']==bait)])
#         pre = line
# df_add_two_lable_bed = df_add_lable_bed
# print(df_add_two_lable_bed)
# sort_chr_start(df_add_two_lable_bed,output='add_two_lable_sorted_SNP-BED_rs_build.bed') 
df_add_two_lable_bed = pd.read_csv('add_two_lable_sorted_SNP-BED_rs_build.bed',sep='\t',header=None,names=['chr','S','E','rs','bait','distance','unique'])
df_add_two_lable_bed.to_csv('add_two_lable_sorted_SNP-BED_rs_build.bed',sep='\t',index=False)
