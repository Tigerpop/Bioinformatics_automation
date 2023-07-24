# -*- coding: utf-8 -*-
import subprocess,re,os,sys
import pandas as pd
from multiprocessing import Process,Pool
import warnings
warnings.filterwarnings('ignore')

sample = sys.argv[1] # 第一个参数
sample_path = sys.argv[2]
generate_location = sys.argv[3]
bed_key = sys.argv[4]

if __name__=='__main__':
    if bed_key in ['BCP650','NBC650']:
        os.chdir(generate_location+"/"+sample_path)
        if not os.path.exists("optitype_generate"):
            os.mkdir("optitype_generate")
        os.chdir(generate_location+"/"+sample_path+"/"+"optitype_generate")
        
        
        # extract_mode = config['extract_mode']['choose']
        # if extract_mode == 'umi_mode':
        #     extracted1,extracted2 = "_extracted.1.fq.gz","_extracted.2.fq.gz"
        # elif extract_mode == 'fastp_mode':
        #     extracted1,extracted2 = "_1.extract.fq.gz","_2.extract.fq.gz"
        extracted1,extracted2 = "_1.extract.fq.gz","_2.extract.fq.gz"
        
        
        razers3_pool = '/opt/optitype/razers3 -i 95 -m 1 -dr 0'
        razers3_reffa = '/refhub/hg19/toolbox_and_RefFile/hla_reference_dna.fasta' # config['razers3']['reffa']
        optitype_tool = '/opt/optitype/OptiTypePipeline.py' # config['optitype']['tools']
        optitype_pool = '--dna -v -p fished' # config['optitype']['optitype_pool']
        input_fq1 = generate_location+'/'+sample_path +'/'+sample+extracted1
        input_fq2 = generate_location+'/'+sample_path +'/'+sample+extracted2
        out_razers3_1 = '-o '+generate_location+'/'+sample_path +'/'+ "optitype_generate"+'/'+'fished_1.bam'
        out_razers3_2 = '-o '+generate_location+'/'+sample_path +'/'+ "optitype_generate"+'/'+'fished_2.bam'
        print(input_fq1,out_razers3_1)
        
        cmd1 = "{razers3_pool} \
                {out_razers3_1} \
                {razers3_reffa} \
                {input_fq1}".format(razers3_pool=razers3_pool,input_fq1=input_fq1,out_razers3_1=out_razers3_1,razers3_reffa=razers3_reffa)
        cmd2 = "{razers3_pool} \
                {out_razers3_2} \
                {razers3_reffa} \
                {input_fq2}".format(razers3_pool=razers3_pool,input_fq2=input_fq2,out_razers3_2=out_razers3_2,razers3_reffa=razers3_reffa)
        cmd3 = "samtools fastq fished_1.bam > sample_1_fished.fastq"
        cmd4 = "samtools fastq fished_2.bam > sample_2_fished.fastq"
        for i in range(1,5):
            cmd = "cmd"+str(i)
            print(i)
            # p = subprocess.Popen(locals()[cmd],shell=True)
            p = subprocess.Popen(eval(cmd), shell=True)
            p.communicate()
            if p.returncode != 0:
                exit('razers3 is false!')
            else:
                print('razers3 is success!')
        cmd = "python {optitype_tool} \
              -i sample_1_fished.fastq sample_2_fished.fastq \
              {optitype_pool} \
              -o ./ ".format(optitype_tool=optitype_tool,optitype_pool=optitype_pool)
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        if p.returncode != 0:
            exit('optitype is false!')
            
            
# ###########################################################
# #!/bin/bash
# reffa_dir=/home/chenyushao/draft/optitype/OptiType-master/data
# tool_dir=/home/chenyushao/draft/optitype/OptiType-master
# sample_dir=/home/chenyushao/draft/optitype
# 
# razers3 -i 95 -m 1 -dr 0 \
# 	-o $sample_dir/fished_1.bam \
# 	$reffa_dir/hla_reference_dna.fasta \
# 	$sample_dir/E150000432_L01_2022WSSW004468-N_extracted.1.fq
# samtools fastq $sample_dir/fished_1.bam > $sample_dir/sample_1_fished.fastq
# razers3 -i 95 -m 1 -dr 0 \
# 	-o $sample_dir/fished_2.bam \
# 	$reffa_dir/hla_reference_dna.fasta \
# 	$sample_dir/E150000432_L01_2022WSSW004468-N_extracted.2.fq
# samtools fastq $sample_dir/fished_2.bam > $sample_dir/sample_2_fished.fastq
# 
# # 注意上面生成的两个 中间产物bam文件，接下来他们的前缀用 -p 来指定以防出现找不到bam文件的错误。
# python $tool_dir/OptiTypePipeline.py \
# 	-i $sample_dir/sample_1_fished.fastq  $sample_dir/sample_2_fished.fastq \
# 	--dna -v -o $sample_dir/extracted_result/  -p fished 
