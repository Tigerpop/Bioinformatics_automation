# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys

class tool():
    def process_fastp_log(self,sample,sample_path,generate_location): 
        # 主动抛出异常，看看父进程的父进程显示效果。
        # aaa
        
        base_quality,inser_size_peak,duplication_rate = '没找到，手动找找','没找到，手动找找','没找到，手动找找'
        os.chdir(sample_path)
        quality_dir = sample_path+"/"+"quality_control"
        if not os.path.exists(quality_dir):
            os.mkdir(quality_dir)
        with open(sample_path+"/"+'fastp_extract_debug.log','r') as f0:
            i = 0 
            for lines in f0:
                if len(lines.split(' ')) >= 3:
                    v1,v2,v3 = lines.split(' ')[0],lines.split(' ')[1],lines.split(' ')[2]
                    if v1 == 'Q30' and v2 == 'bases:' and i==0:
                        base_quality = re.findall('\((.*?)\)',v3)[0]
                        print('base_quality: ',base_quality)
                        i += 1
                if lines[:-5] == 'Insert size peak (evaluated by paired-end reads):':
                    inser_size_peak = lines[-5:-1]
                    print('inser_size_peak: ',inser_size_peak)
                if lines[:17] == 'Duplication rate:':
                    duplication_rate = lines[18:]
                    print('duplication_rate: ',duplication_rate)
        return base_quality,inser_size_peak,duplication_rate
    
    def process_bam(self,sample,log_path,sample_path,generate_location,bed):
        mapped,Coverage,ontarget,depth,cleandepth = '没找到，手动找找','没找到，手动找找','没找到，手动找找','没找到，手动找找','没找到，手动找找'
        
        os.chdir(f"{log_path}/quality_control")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        # quality_dir = generate_location+"/"+log_path+"/"+"quality_control"
        # if not os.path.exists("quality_control"):
        #     os.mkdir("quality_control")
            
        bam_file = generate_location +"/"+ sample_path +"/"+ sample +".markdup.bam"
        cmd = f'samtools flagstat {bam_file} > {log_path}/quality_control/output.flagstat'
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        cmd = f'/opt/bamdst/bamdst -p {bed} -o {log_path}/quality_control/ {bam_file}'
        p = subprocess.Popen(cmd,shell=True)
        p.communicate()
        
        with open(f'{log_path}/quality_control/output.flagstat','r') as f0:
            for lines in f0:
                mapped = re.findall('.*mapped \((.*?)\)',lines)
                if mapped != []:          # 第一个出现mapped 的地方。
                    print('mapped: ',mapped)
                    mapped = mapped[0].split(':')[0]
                    break
        with open(f'{log_path}/quality_control/coverage.report','r')as f:
            for lines in f:
                Coverage_line = re.findall(r'\[Target\] Coverage \(>=4x\)', lines)
                if Coverage_line!=[]:                # 定位到目标行。
                    [Coverage] = re.findall(r'\d*\.\d*%$',lines)
                    print(Coverage)
                ontarget_line = re.findall(r'Fraction of Target Reads in all reads', lines)
                if ontarget_line != []:  # 定位到目标行。
                    [ontarget] = re.findall(r'\d*\.\d*%$', lines)
                    # print(lines)
                    print(ontarget)
                depth_line = re.findall(r'\[Target\] Average depth',lines)
                if depth_line != [] and re.findall(r'\(.*?\)',lines)==[]: # 同时无括号。
                    [depth] = re.findall(r'\d*\.\d*$', lines)
                    # print(lines)
                    print(depth)
                cleandepth_line = re.findall(r'\[Target\] Average depth\(rmdup\)',lines)
                if cleandepth_line != []:
                    [cleandepth] = re.findall(r'\d*\.\d*$', lines)
                    # print(lines)
                    print(cleandepth)
        return mapped,Coverage,ontarget,depth,cleandepth

    def NGScheckmate(self,sample,sample_path,sample_dir,log_path):
        try:
            quality_dir = log_path +'/'+'quality_control'
            if not os.path.exists(quality_dir):
                os.makedirs(quality_dir)# os.mkdir(quality_dir)
            # 用 TN 表示对照样本的区分，如果sample 是 1008-T sample_TN 就是 1008-N。
            def determine_sample_type(sample):
                pattern1 = r'.*(-T|-N|-T-1|-N-1)$'  # 样本类型1的正则表达式模式
                pattern2 = r'^\d{8}C?L\d{3}$'  # 样本类型2和3的正则表达式模式
                if re.match(pattern1, sample):
                    print('这是 解码的样本')
                    return "解码"
                elif re.match(pattern2, sample):
                    print('这是 睿明的样本')
                    return "睿明"
                else:
                    return "未知样本类型"
            if determine_sample_type(sample)=="解码":
                sample_path_TN = sample_path[:-1]+'N' if sample_path[-1] == 'T' else sample_path[:-1]+'T'
            elif determine_sample_type(sample)=="睿明":
                sample_path_TN = sample_path.replace('CL','L') if 'CL' in sample_path else sample_path.replace('L','CL')
            # sample_TN = sample_path_TN.split("/")[-1]
            [fq_1] = [ ele for ele in os.listdir(f'{sample_dir}/{sample_path}') if re.search('_1.fq',ele)!=None ]
            [fq_2] = [ ele for ele in os.listdir(f'{sample_dir}/{sample_path}') if re.search('_2.fq',ele)!=None ]
            [fq_1_TN] = [ ele for ele in os.listdir(f'{sample_dir}/{sample_path_TN}') if re.search('_1.fq',ele)!=None ]
            [fq_2_TN] = [ ele for ele in os.listdir(f'{sample_dir}/{sample_path_TN}') if re.search('_2.fq',ele)!=None ]
            print(fq_1)
            print(fq_2)
            print(fq_1_TN)
            print(fq_2_TN)
            cmd1 = f'/opt/NGScheckmate/ngscheckmate_fastq \
                  -1 {sample_dir}/{sample_path}/{fq_1}\
                  -2 {sample_dir}/{sample_path}/{fq_2}\
                  /opt/NGScheckmate//SNP/SNP.pt \
                  -p 8 > {quality_dir}/sample.vaf'
            cmd2 = f'/opt/NGScheckmate/ngscheckmate_fastq \
                  -1 {sample_dir}/{sample_path_TN}/{fq_1_TN}\
                  -2 {sample_dir}/{sample_path_TN}/{fq_2_TN}\
                  /opt/NGScheckmate//SNP/SNP.pt \
                  -p 8 > {quality_dir}/sample_TN.vaf'        
            cmd3 = f'python2 /opt/NGScheckmate/vaf_ncm.py -f \
                  -I {quality_dir} \
                  -O {quality_dir} \
                  -N {sample}_Similarity'
            for cmd in [cmd1,cmd2,cmd3]:
                p = subprocess.Popen(cmd,shell=True)
                p.communicate()
                if p.returncode != 0:
                    exit(3)
            with open(f'{quality_dir}/{sample}_Similarity_all.txt','r')as f:
                for line in f:
                    TN_similarity = float(line.split('\t')[3])
            return TN_similarity
        except:
            TN_similarity = 0.80
            print(TN_similarity ,'出现  问题')
            return TN_similarity
          
# def concat_fastp_and_bam(sample_path):
#     os.chdir(generate_location+"/"+sample_path)
#     quality_dir = generate_location+"/"+sample_path+"/"+"quality_control"
#     if not os.path.exists("quality_control"):
#         os.mkdir("quality_control")
#     
#     base_quality,inser_size_peak,duplication_rate = process_fastp_log(sample_path)
#     mapped = process_bam(sample_path)
#     with open('./quality_control/quality_control.txt','a+')as f0:
#         f0.write('mapped: '+str(mapped)+'\n')
#         f0.write('base_quality: '+str(base_quality)+'\n')
#         f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
#         f0.write('duplication_rate: '+str(duplication_rate)+'\n')
  

# if __name__=="__main__":
#     process_fastp_log(sample_path)
#     process_bam(sample_path)
#     concat_fastp_and_bam(sample_path)
#     
    
        
    
