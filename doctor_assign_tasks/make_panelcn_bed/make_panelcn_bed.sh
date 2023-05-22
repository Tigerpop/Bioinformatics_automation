#!/bin/bash

# # 第一步加入exon信息;
# bedtools intersect \
# -a /home/chenyushao/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed \
# -b /refhub/hg19/target/BC17/BC17.raw.hg19.bed \
# -wa > add_exom.log
# 
# python ~/doctor_assign_tasks/make_panelcn_bed/save_exom.py
# 
# # 第二步加入深度信息；
# source /opt/miniconda3/etc/profile.d/conda.sh
# conda activate no_umitools_py
# 
# bedtools coverage -a /home/chenyushao/doctor_assign_tasks/make_panelcn_bed/add_gene_exon.log \
# -b /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17/2022WSSW004338-T.bwa_mem.bam \
# > ~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log 2>&1
# 
# conda deactivate
# 
# # 第三步过滤 reads 20以下的；
# python ~/doctor_assign_tasks/make_panelcn_bed/filter_and_sort.py
# 
# # 第四步调整为panelcn.bed 需要的格式；
# python ~/doctor_assign_tasks/make_panelcn_bed/format_panelcn_bed.py

#############################################
# # 第一步加入exon信息;
# bedtools intersect \
# -a /home/chenyushao/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed \
# -b /refhub/hg19/target/BCP650/BCP650.raw.hg19.bed \
# -wa > add_exom.log
# 
# python ~/doctor_assign_tasks/make_panelcn_bed/save_exom.py
# 
# # 第二步加入深度信息；
# source /opt/miniconda3/etc/profile.d/conda.sh
# conda activate no_umitools_py
# 
# bedtools coverage -a /home/chenyushao/doctor_assign_tasks/make_panelcn_bed/add_gene_exon.log \
# -b /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2022WSSW000306-T.bwa_mem.bam \
# > ~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log 2>&1
# 
# conda deactivate
# 
# # 第三步过滤 reads 20以下的；
# python ~/doctor_assign_tasks/make_panelcn_bed/filter_and_sort.py
# 
# # 第四步调整为panelcn.bed 需要的格式；
# python ~/doctor_assign_tasks/make_panelcn_bed/format_panelcn_bed.py


# ##################################
# #第一步加入exon信息;
# bedtools intersect \
# -a /home/chenyushao/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed \
# -b /refhub/hg19/target/NBC650/NBC650.raw.hg19.bed \
# -wa > add_exom.log
# 
# python ~/doctor_assign_tasks/make_panelcn_bed/save_exom.py
# 
# # 第二步加入深度信息；
# source /opt/miniconda3/etc/profile.d/conda.sh
# conda activate no_umitools_py
# 
# bedtools coverage -a /home/chenyushao/doctor_assign_tasks/make_panelcn_bed/add_gene_exon.log \
# -b /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004654-T.bwa_mem.bam \
# > ~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log 2>&1
# 
# conda deactivate
# 
# # 第三步过滤 reads 20以下的；
# python ~/doctor_assign_tasks/make_panelcn_bed/filter_and_sort.py
# 
# # 第四步调整为panelcn.bed 需要的格式；
# python ~/doctor_assign_tasks/make_panelcn_bed/format_panelcn_bed.py


# ##################################
# # 第一步加入exon信息;
# bedtools intersect \
# -a /home/chenyushao/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed \
# -b /refhub/hg19/target/Q120/Q80.raw.hg19.bed \
# -wa > add_exom.log
# 
# python ~/doctor_assign_tasks/make_panelcn_bed/save_exom.py
# 
# # 第二步加入深度信息；
# source /opt/miniconda3/etc/profile.d/conda.sh
# conda activate no_umitools_py
# 
# bedtools coverage -a /home/chenyushao/doctor_assign_tasks/make_panelcn_bed/add_gene_exon.log \
# -b /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120/2022WSSW000956-T.bwa_mem.bam \
# > ~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log 2>&1
# 
# conda deactivate
# 
# # 第三步过滤 reads 20以下的；
# python ~/doctor_assign_tasks/make_panelcn_bed/filter_and_sort.py
# 
# # 第四步调整为panelcn.bed 需要的格式；
# python ~/doctor_assign_tasks/make_panelcn_bed/format_panelcn_bed.py


##################################
# 第一步加入exon信息;
bedtools intersect \
-a /home/chenyushao/doctor_assign_tasks/hg19_bed/hg19_filter_GTF_add_exon_num.bed \
-b /refhub/hg19/target/SD160/SD160.raw.bed \
-wa > add_exom.log

python ~/doctor_assign_tasks/make_panelcn_bed/save_exom.py

# 第二步加入深度信息；
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate no_umitools_py

bedtools coverage -a /home/chenyushao/doctor_assign_tasks/make_panelcn_bed/add_gene_exon.log \
-b /refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160/2022WSSW002335-T.bwa_mem.bam \
> ~/doctor_assign_tasks/make_panelcn_bed/add_gene_exon_depth.log 2>&1

conda deactivate

# 第三步过滤 reads 20以下的；
python ~/doctor_assign_tasks/make_panelcn_bed/filter_and_sort.py

# 第四步调整为panelcn.bed 需要的格式；
python ~/doctor_assign_tasks/make_panelcn_bed/format_panelcn_bed.py