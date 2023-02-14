# -*- coding: utf-8 -*-
import quality_control as qc
import configparser,subprocess,re,os,sys
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']
sample_path = sys.argv[1]
sample = sample_path.split("/")[-1]

base_quality,inser_size_peak,duplication_rate = qc.process_fastp_log(sample_path)
mapped = qc.process_bam(sample_path)
qc.concat_fastp_and_bam(sample_path)
print(base_quality,inser_size_peak,duplication_rate,mapped)

