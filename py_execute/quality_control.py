# -*- coding: utf-8 -*-
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
hg_19_or_38 = config['hg_19_or_38']['hg_19_or_38']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]


def process_fastp_log(sample_path):    
    os.chdir(generate_location+"/"+sample_path)
    quality_dir = generate_location+"/"+sample_path+"/"+"quality_control"
    if not os.path.exists("quality_control"):
        os.mkdir("quality_control")
    with open('fastp.log','r') as f0:
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
            if lines[:-10] == 'Duplication rate:':
                duplication_rate = lines[-10:]
                print('duplication_rate: ',duplication_rate)
    return base_quality,inser_size_peak,duplication_rate

def process_bam(sample_path):
    os.chdir(generate_location+"/"+sample_path)
    quality_dir = generate_location+"/"+sample_path+"/"+"quality_control"
    if not os.path.exists("quality_control"):
        os.mkdir("quality_control")
    extract_mode = config['extract_mode']['choose']
    if extract_mode == 'umi_mode':
        dedup_or_markdup = 'dedup'
    elif extract_mode == 'fastp_mode':
        dedup_or_markdup = 'markdup'
        
    bam_file = generate_location +"/"+ sample_path +"/"+ sample +"."+ dedup_or_markdup + ".bam"
    cmd = f'samtools flagstat {bam_file} > {quality_dir}/output.flagstat'
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    cmd = f'/opt/bamdst/bamdst -p /refhub/hg19/target/BC17.raw.hg19.bed -o {quality_dir}/ {bam_file}'
    p = subprocess.Popen(cmd,shell=True)
    p.communicate()
    
    with open(f'{quality_dir}/output.flagstat','r') as f0:
        for lines in f0:
            mapped = re.findall('.*mapped \((.*?)\)',lines)
            if mapped != []:
                print('mapped: ',mapped)
                mapped = mapped[0].split(':')[0]
                return mapped

def concat_fastp_and_bam(sample_path):
    os.chdir(generate_location+"/"+sample_path)
    quality_dir = generate_location+"/"+sample_path+"/"+"quality_control"
    if not os.path.exists("quality_control"):
        os.mkdir("quality_control")
    
    base_quality,inser_size_peak,duplication_rate = process_fastp_log(sample_path)
    mapped = process_bam(sample_path)
    with open('./quality_control/quality_control.txt','a+')as f0:
        f0.write('mapped: '+str(mapped)+'\n')
        f0.write('base_quality: '+str(base_quality)+'\n')
        f0.write('inser_size_peak: '+str(inser_size_peak)+'\n')
        f0.write('duplication_rate: '+str(duplication_rate)+'\n')
  

if __name__=="__main__":
    process_fastp_log(sample_path)
    process_bam(sample_path)
    concat_fastp_and_bam(sample_path)
    
    
        
    
