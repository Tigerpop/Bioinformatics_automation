#coding=utf8

import pandas as pd
import re

df_result = pd.read_csv('~/doctor_assign_tasks/make_panelcn_bed/sorted_filter_add_gene_exon_depth.log', sep='\t', header=None, \
    names=['chr', 'start', 'end','gene','exon', 'reads', 'covered_bp_nums', 'area_length', 'coverage_value'])
        
df_result['set'] = df_result[['gene','exon','chr', 'start', 'end']]\
    .astype(str).apply(lambda x: '.'.join(x.dropna()),axis=1)
    
df_result = df_result[['chr', 'start', 'end','set']]

df_result.to_csv('format.log', sep='\t', index=False, header=None)
