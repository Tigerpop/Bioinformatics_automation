# -*- coding: utf-8 -*-
import configparser
config = configparser.ConfigParser()

# sample_dir = '/home/chenyushao/cumulative_download/datelog'
sample_dir = '/fastq_data'
sample_list = str(['2022WSSW003295-T','2022WSSW003294-T','2022WSSW003292-T'])
# sample_list = str(['2022WSSW002177-T','2022WSSW000970-T','2022WSSW002883-T','2022WSSW000328-T'])  # 为多线程准备。,'2022WSSW000970-T'
# sample_list = str(['2022WSSW003295-T'])

hg_19_or_38 = "hg19"   # 这里选择 hg19版本 还是 hg38版本 作为基准参照,直接在config文件中修改不起作用。
if hg_19_or_38 == "hg19":
    toolbox_and_RefFile = '/refhub/hg19/toolbox_and_RefFile'
elif hg_19_or_38 == "hg38":
    toolbox_and_RefFile = '/refhub/hg38/toolbox_and_RefFile'
# 注意这里 改了以后，文件最好要删除了重新运行一边，不然可能是hg19生成的dedup.bam 配hg38的后续处理，不匹配。

# hg选择
config['hg_19_or_38'] = {
    'hg_19_or_38': hg_19_or_38
}

# 突变检测模块，根据突变类型选择工具。
config['Mutation_detection'] = {
    'snv_indel': "freebayes",
    'sv': "factera",
    'cnv': "cnvnator",
    'hla': "optitype",
    'msi': "msisensor",
    'choose': "cnv"   # 这里选择
}

# extract 模式选择
config['extract_mode'] = {
    'umi_mode': "umi_tool",
    'fastp_mode': "fastp",
    'choose': "fastp_mode"
}

# 样本位置
config['sample'] = {
    'sample_dir': sample_dir,
    'sample_list': sample_list
}

# 生成文件位置.    /home/chenyushao/py_generate
generate_dir = "/working_tmp"
config['generate'] = {
    'location': generate_dir
}

# 归档文件位置.    
archive_dir = '/archive'
config['archive'] = {
    'location': archive_dir
}


# 调用文件位置
if hg_19_or_38 == "hg19":
    fasta = "/refhub/hg19/fa/ucsc.hg19.fasta"
    bed = '/home/chenyushao/doctor_assign_tasks/hg19_bed/four_field.bed'  #filter_just_save_17_GTF.bed'   # "/refhub/kitbed/BC17.expand1.hg19.bed"
    config['reference_document'] = {
        'human_genome_index': "/refhub/hg19/human_genome_index/gatk_hg19",
        'fasta': "/refhub/hg19/fa/ucsc.hg19.fasta",
        'fasta_dir': "/refhub/hg19/fa/fa",
        'bed': "/home/chenyushao/doctor_assign_tasks/hg19_bed/four_field.bed"}                    # 'bed': "/refhub/kitbed/BC17.expand1.hg19.bed"
elif hg_19_or_38 == "hg38":
    fasta = "/refhub/hg38/fa/Homo_sapiens_assembly38.fasta"
    bed = "/refhub/hg38/target/BC17.expand1.hg38.bed"
    config['reference_document'] = {
        'human_genome_index': "/refhub/hg38/human_genome_index/gatk_hg38",
        'fasta': "/refhub/hg38/fa/Homo_sapiens_assembly38.fasta",
        'fasta_dir': "/refhub/hg38/fa",
        'bed': "/refhub/hg38/target/BC17.expand1.hg38.bed"}



# 工具位置，以及工具参数。除了输入输出其他均可修改！
config['annovar'] = {
    'annovar_path': "/opt/annovar",
    'tool': "table_annovar.pl",
    'parameters_pool': "{toolbox_and_RefFile} \ \n\
 -buildver {hg_19_or_38} \ \n\
-remove \ \n\
-protocol smallrefGene,cytoBand,clinvar_20220320,avsnp150,dbnsfp42c \ \n\
-operation g,r,f,f,f \ \n\
-nastring . \ \n\
-vcfinput \ \n\
-polish".format(hg_19_or_38=hg_19_or_38,toolbox_and_RefFile=toolbox_and_RefFile)
}
config['faToTwoBit'] = {
    'faToTwoBit': "/opt/factera/faToTwoBit",
    'parameters_pool': "{fasta} \ \n\
    {generate_dir}/{hg_19_or_38}.2bit".format(hg_19_or_38=hg_19_or_38,fasta=fasta,generate_dir=generate_dir)
}
# /refhub/factera/hg38.ensembl.exon.bed
config['factera'] = {
    'factera_path': "/opt/factera",
    'tool': "factera.pl",
    'parameters_pool': f"/refhub/{hg_19_or_38}/target/factera_special_bed/{hg_19_or_38}.exons.bed \ \n\
{generate_dir}/{hg_19_or_38}.2bit "   # /home/chenyushao/doctor_assign_tasks/three_field.bed
}
config['cnvnator'] = {
    'parameters_pool1': "cnvnator -root file.root -genome {hg_19_or_38} -tree ".format(hg_19_or_38=hg_19_or_38),
    'parameters_pool2': "cnvnator -root file.root -genome {hg_19_or_38} -his 1000 -d ".format(hg_19_or_38=hg_19_or_38),
    'parameters_pool3': "cnvnator -root file.root -genome {hg_19_or_38} -stat 1000 ".format(hg_19_or_38=hg_19_or_38),
    'parameters_pool4': "cnvnator -root file.root -genome {hg_19_or_38} -partition 1000 ".format(hg_19_or_38=hg_19_or_38),
    'parameters_pool5': "cnvnator -root file.root -genome {hg_19_or_38} -call 1000  > cnv.call.txt".format(hg_19_or_38=hg_19_or_38),
    'parameters_pool6': "/opt/CNVnator_v0.4.1/src/cnvnator2VCF.pl cnv.call.txt >cnv.vcf"
}
config['razers3'] = {
    'razers3_pool': "razers3 -i 95 -m 1 -dr 0 ",
    'reffa': f"/refhub/{hg_19_or_38}/toolbox_and_RefFile/hla_reference_dna.fasta"
}
config['optitype'] = {
    'tools': "/opt/OptiType-master/OptiTypePipeline.py",
    'optitype_pool': "--dna \ \n \
             -v \ \n \
             -p fished "
}
config['msisensor'] = {
    'tools': "/opt/msisensor-ct-master/msisensor-ct",
    'msisensor_pool': "msi \ \n \
             -D \ \n \
             -M /opt/msisensor-ct-master/models_hg19_GRCh37 "
}



with open('config.ini','w')as configfile:
    config.write(configfile)
