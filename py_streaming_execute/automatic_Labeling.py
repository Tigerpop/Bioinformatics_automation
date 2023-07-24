#coding=utf8

import pandas as pd
from openpyxl import load_workbook
# from docx import Document



class tools():
    def __init__(self,input_df,bed_key,output_file='./'):
        self.input_df = input_df
        self.output_file = output_file
        self.bed_key = bed_key
        self.Somatic = self.Fusion = self.Cnv = self.input_df

    def choose_Interest_Gene(self,bed_key:str)-> str:
        option_dict = \
            {'BC17T':'ALK,AKT1,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'BC17B':'ALK,AKT1,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'Q120T':'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'Q120B': 'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'SLC17T': 'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'SLC17B': 'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'SLC80T': 'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KIT,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'SLC80B': 'ALK,AKT1,APC,BRAF,BCL2L11,BIM,EGFR,ERBB2,HER2,KIT,KRAS,MAP2K1,MEK1,MET,PIK3CA,PTEN,NTRK1,NTRK2,NTRK3,NRAS,RET,ROS1,TP53'
             ,'SD160T':'AKT1,ALK,APC,ATM,BRAF,BRCA1,BRCA2,BRIP1,CDK12,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,EZH2,FANCL,FGFR1,FGFR2\
             ,FGFR3,HRAS,IDH1,IDH2,JAK1,JAK2,KDM6A,KIT,KRAS,MET,MTOR,NF1,NRAS,NTRK1,NTRK2,NTRK3,PDGFRA,PIK3CA,RAD51B,RAD51C,RAD51D\
             ,RAD54L,RET,ROS1,SRSF2,TP53,TSC1,TSC2,其他'
             ,'SD160B': 'AKT1,ALK,APC,ATM,BRAF,BRCA1,BRCA2,BRIP1,CDK12,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,EZH2,FANCL,FGFR1,FGFR2\
             ,FGFR3,HRAS,IDH1,IDH2,JAK1,JAK2,KDM6A,KIT,KRAS,MET,MTOR,NF1,NRAS,NTRK1,NTRK2,NTRK3,PDGFRA,PIK3CA,RAD51B,RAD51C,RAD51D\
             ,RAD54L,RET,ROS1,SRSF2,TP53,TSC1,TSC2,其他'
             ,'BCP650':'ABL1,AKT1,ALK,APC,ARAF,ARID1A,ATM,ATR,BCL2L11,BRAF,BRCA1,BRCA2,BRD4,BRIP1,CCND1,CCND2,CCND3,CDH1\
             ,CDK12,CDK4,CDK6,CDKN2A,CHEK1,CHEK2,CTNNB1,DNMT1,EGFR,ERBB2,HER2,ERBB3,ERBB4,ERCC1,ESR1,EZH2,FANCA,FANCC,FANCL,FGFR1\
             ,FGFR2,FGFR3,FLT3,FXBW7,GNA11,HRAS,IDH1,IDH2,JAK1,JAK2,KDM6A,KIT,KRAS,MAP2K1,MAP2K2,MET,MTOR,NF1,NRAS,NTRK1,NTRK2\
             ,NTRK3,PALB2,PDGFB,PDGFRA,PDGFRB,PIK3CA,PTCH1,PTEN,RAD51B,RAD51C,RAD51D,RAD54L,RAF1,RET,ROS1,SF3B1,SMARCB1,SRSF2\
             ,TP53,TSC1,TSC2,U2AF1,ZRSR2,其他'
             ,'NBC650': 'ABL1,AKT1,ALK,APC,ARAF,ARID1A,ATM,ATR,BCL2L11,BRAF,BRCA1,BRCA2,BRD4,BRIP1,CCND1,CCND2,CCND3,CDH1\
             ,CDK12,CDK4,CDK6,CDKN2A,CHEK1,CHEK2,CTNNB1,DNMT1,EGFR,ERBB2,HER2,ERBB3,ERBB4,ERCC1,ESR1,EZH2,FANCA,FANCC,FANCL,FGFR1\
             ,FGFR2,FGFR3,FLT3,FXBW7,GNA11,HRAS,IDH1,IDH2,JAK1,JAK2,KDM6A,KIT,KRAS,MAP2K1,MAP2K2,MET,MTOR,NF1,NRAS,NTRK1,NTRK2\
             ,NTRK3,PALB2,PDGFB,PDGFRA,PDGFRB,PIK3CA,PTCH1,PTEN,RAD51B,RAD51C,RAD51D,RAD54L,RAF1,RET,ROS1,SF3B1,SMARCB1,SRSF2\
             ,TP53,TSC1,TSC2,U2AF1,ZRSR2,其他'
             } # 在大panel中 删除了 不受待见的 BARD1 基因，以后看有无需要补充回去；
        return option_dict.get(bed_key,'没有对应的 探针名')
    def choose_Interest_fusion_Gene(self,bed_key:str)-> str:
        option_dict = \
            {'BC17T':'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'BC17B':'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'Q120T':'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'Q120B': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SLC17T': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SLC17B': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SLC80T': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SLC80B': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SD160T':'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'SD160B': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'BCP650':'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             ,'NBC650': 'ALK,EGFR,NTRK1,NTRK2,NTRK3,RET,ROS1'
             }
        return option_dict.get(bed_key,'没有对应的 探针名')
    def choose_Interest_cnv_Gene(self,bed_key:str)-> str:
        option_dict = \
            {'BC17T':'EGFR,ERBB2,HER2,MET'
             ,'BC17B':'EGFR,ERBB2,HER2,MET'
             ,'Q120T':'EGFR,ERBB2,HER2,MET'
             ,'Q120B': 'EGFR,ERBB2,HER2,MET'
             ,'SLC17T': 'EGFR,ERBB2,HER2,MET'
             ,'SLC17B': 'EGFR,ERBB2,HER2,MET'
             ,'SLC80T': 'EGFR,ERBB2,HER2,MET'
             ,'SLC80B': 'EGFR,ERBB2,HER2,MET'
             ,'SD160T':'CDK12,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,FGFR1,FGFR2,FGFR3,MET,'
             ,'SD160B': 'CDK12,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,FGFR1,FGFR2,FGFR3,MET,'
             ,'BCP650':'CDK12,CDK4,CDK6,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,ERBB3,ERBB4,FGFR1,FGFR2,FGFR3,MET'
             ,'NBC650': 'CDK12,CDK4,CDK6,CDKN2A,CHEK1,CHEK2,EGFR,ERBB2,HER2,ERBB3,ERBB4,FGFR1,FGFR2,FGFR3,MET'
             }
        return option_dict.get(bed_key,'没有对应的 探针名')

    def method_somatic_0(self): # somatic 和 germline 还没有分离。
        print('进入第一个打标签流程。')
        Interest_Gene = self.choose_Interest_Gene(self.bed_key)
        if Interest_Gene=='没有对应的 探针名': return self.input_df #'没有对应的 探针名'
        Interest_Gene_list = Interest_Gene.split(',')
        Somatic = self.Somatic
        Somatic['VAF_'] = Somatic['VAF'].str.rstrip('%').astype(float)
        Somatic.loc[((Somatic['VAF_'] >= 3) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    & (Somatic['Func.smallrefGene'] == 'exonic') \
                    & (Somatic['DP'] > 600) \
                    & (Somatic['CLNSIG'].str.contains('Uncertain|uncertain|not_provided')) \
                    & (Somatic['Gene.smallrefGene'].apply(lambda x: x in Interest_Gene_list)), 'review'] = 'S3'
        Somatic.loc[((Somatic['VAF_'] >= 3) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    &(Somatic['Func.smallrefGene']=='exonic')\
                    &(Somatic['DP']>600)\
                    &(Somatic['CLNSIG'].str.contains('Conflict.*pathogenicity|conflict.*pathogenicity|drug_response|Drug_response'))\
                    &(Somatic['Gene.smallrefGene'].apply(lambda x:x in Interest_Gene_list)),'review'] = 'S2'
        Somatic.loc[((Somatic['VAF_'] >= 3) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    &(Somatic['Func.smallrefGene']=='exonic')\
                    &(Somatic['DP']>600)\
                    &(Somatic['CLNSIG'].str.contains('pathogenic|Pathogenic'))\
                    &(Somatic['Gene.smallrefGene'].apply(lambda x:x in Interest_Gene_list)),'review'] = 'S1'
        Somatic.loc[((Somatic['VAF_'] >= 3) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    &(Somatic['CLNSIG'].str.contains('pathogenic|Pathogenic'))\
                    &(Somatic['Gene.smallrefGene'].apply(lambda x:x in ['TERT'])),'review'] = 'S1'
        Somatic.loc[((Somatic['VAF_'] >= 3) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    &(Somatic['Func.smallrefGene']=='exonic')\
                    &(Somatic['DP']>600) \
                    &(Somatic['Gene.smallrefGene'].isin(['EGFR','TP53'])) \
                    & ~(Somatic['CLNSIG'].astype(str).str.contains('Benign|benign|Uncertain|uncertain')) \
                    &(Somatic['Gene.smallrefGene'].apply(lambda x:x in Interest_Gene_list)),'review'] = 'S1'
        # Somatic.to_csv(output_file,sep='\t')
        return Somatic

    def method_somatic_1(self): # somatic 和 germline 还没有分离。
        print('进入第二个打标签流程。')
        Interest_Gene = self.choose_Interest_Gene(self.bed_key)
        if Interest_Gene == '没有对应的 探针名': return self.input_df #'没有对应的 探针名'
        Interest_Gene_list = Interest_Gene.split(',')
        Somatic = self.Somatic
        # print('ok')
        Somatic.loc[((Somatic['VAF_'] >= 0) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    & (Somatic['DP'] > 500) \
                    & (Somatic['AO'] > 200) \
                    & (Somatic['AAchange'].astype(str).str.contains(r'fs\*|ins|del')) \
                    & ~(Somatic['CLNSIG'].astype(str).str.contains('Benign|benign')) \
                    & (Somatic['Gene.smallrefGene'].apply(lambda x: x in Interest_Gene_list)), 'review'] = 'S1'
        Somatic.loc[((Somatic['VAF_'] >= 0) & (Somatic['VAF_'] <= 40) | (Somatic['VAF_'] >= 60) & (Somatic['VAF_'] <= 90)) \
                    & (Somatic['DP'] > 500) \
                    & (Somatic['AO'] > 200) \
                    & (Somatic['AAchange'].astype(str).str.contains(r'fs\*|ins|del')) \
                    & (Somatic['CLNSIG'].astype(str).str.contains('Uncertain|uncertain|not_provided')) \
                    & (Somatic['Gene.smallrefGene'].apply(lambda x: x in Interest_Gene_list)), 'review'] = 'S3'
        # print('ko')
        Somatic.drop('VAF_', axis=1, inplace=True)
        # Somatic.to_csv(output_file, sep='\t')
        return Somatic

    def method_somatic(self):
        result_df = self.method_somatic_0()
        result_df = self.method_somatic_1()
        return result_df

    def method_fusion(self):
        print('进入第三个打标签流程。')
        Interest_Gene = self.choose_Interest_fusion_Gene(self.bed_key)
        if Interest_Gene == '没有对应的 探针名': return self.input_df #'没有对应的 探针名'
        Interest_Gene_list = Interest_Gene.split(',')
        Fusion = self.Fusion
        Fusion.loc[((Fusion['Break_support1']>200) \
                    & (Fusion['Break_support2']>200)\
                    & ((Fusion['Region1'].apply(lambda x: x in Interest_Gene_list)) | (Fusion['Region2'].apply(lambda x: x in Interest_Gene_list)))),'review'] = 'S1'
        # Fusion.to_csv(output_file, sep='\t')
        return Fusion

    def method_cnv(self):
        print('进入第四个打标签流程。')
        Interest_Gene = self.choose_Interest_cnv_Gene(self.bed_key)
        if Interest_Gene == '没有对应的 探针名': return self.input_df #'没有对应的 探针名'
        Interest_Gene_list = Interest_Gene.split(',')
        Cnv = self.Cnv
        # 按照 'gene' 列进行分组，找到每组中 'CNN' 列最大值所在的索引
        max_idx = Cnv.groupby('Gene')['CNN'].idxmax()
        # # 根据索引提取对应的行
        # result = Cnv.loc[max_idx]
        Cnv.loc[(Cnv['Gene'].apply(lambda x: x in Interest_Gene_list))
                    & (Cnv['CNN']>=4)
                    & (Cnv.index.isin(max_idx)), 'review'] = 'S1'
        # Cnv.to_csv(output_file, sep='\t')
        return Cnv

#
# input_file = '/Users/chenyushao/Desktop/冯素改/rstudio-export-69/2023WSSW001021-T.summary.xlsx'
# output_file = '/Users/chenyushao/Desktop/冯素改/rstudio-export-69/test.xlsx'
# df = pd.read_excel(input_file, sheet_name=None)
# Meta,Somatic,Germline, Fusion, Cnv, Qc \
#     = df['meta'].fillna(''),df['somatic'], df['germline'], df['fusion'], df['cnv'], df['qc']
# input_df = Somatic
# bed_key = 'BCP650'#'BC17T'
#
# # 模拟使用 。
# T = tools(input_df,bed_key,output_file )
# result_df = T.method_somatic()
# result_df.to_csv(output_file,sep='\t')
# # T.method_fusion()
# # T.method_cnv()
