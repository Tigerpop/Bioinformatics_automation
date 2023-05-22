#coding=utf8

import pandas as pd 

df = pd.read_csv('./add_exom.log',sep='\t',header=None,names=['chr_1','start_1','end_1','gene','rna','direction','exon'])
df = df[['chr_1','start_1','end_1','gene','exon']]
df['exon'] = df['exon'].str.replace('exon_','E')
df = df.drop_duplicates()

df.to_csv('add_gene_exon.log',sep='\t',header=None,index=None)
