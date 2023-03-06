# coding=utf8 

import os,subprocess
import pandas as pd 

all_ref_exon_bed = '~/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed'
waiting_for_process_bed = '/refhub/hg19/target/Q120/Q80.raw.hg19.bed'
Generate_results = '/refhub/hg19/target/Q120/Q120.exon.hg19.bed'
Target_Regions_bed = '/refhub/hg19/target/Q120/Target_Regions.bed' 
customNumbering_txt = '/refhub/hg19/target/Q120/customNumbering.txt' 

cmd = f'bedtools intersect -a {all_ref_exon_bed} -b \
  {waiting_for_process_bed} -wa -wb > {Generate_results} '
p = subprocess.Popen(cmd,shell=True)
p.communicate()

df = pd.read_csv( f'{Generate_results}',sep='\t',names= \
     ['all_chr','all_start','all_end','genename','rna','direct'\
     ,'exon','bed_chr','bed_start','bed_end'])

df['exon_num'] =df['exon'].str.split("_",expand=True)[1]      # pandas 的这里和python有点不一样，不支持-1。  
print(df)

df_1 = df[['bed_chr','bed_start','bed_end','genename']]
df_1.to_csv(f'{Target_Regions_bed}',header=0,sep='\t', index=False)
df_2 = df[['all_chr','all_start','all_end','genename','exon_num']]
df_2.to_csv(f'{customNumbering_txt}',header=['Chr','Start','End','Gene','Custom.Exon'],sep='\t', index=False)

