#coding=utf8
import pandas as pd
import subprocess
import warnings
warnings.filterwarnings('ignore')
import docx, copy, re, os,datetime,math,shutil,logging,inspect,sys
import numpy as np
from docx import Document

# , '睿明226基因': f'python /home/chenyushao/make_word/SD160_word.py {sample} {date} {word_name}'
# , '睿明110基因': f'python /home/chenyushao/make_word/Gene110_ty_LangCancerTissue_word.py {sample} {date} {word_name}'
def choose_channe(mode:str,sample:str,date:str,word_name:str)-> str:
    dict_ = {'解码17基因':f'python /home/chenyushao/make_word/BC17_word.py {sample} {date} {word_name}'
              ,'解码25基因': f'python /home/chenyushao/make_word/Q80_word.py {sample} {date} {word_name}'
              ,'解码80基因':f'python /home/chenyushao/make_word/Q80_word.py {sample} {date} {word_name}'
              ,'解码110基因':f'python /home/chenyushao/make_word/Q110_word.py {sample} {date} {word_name}'
              ,'解码223基因':f'python /home/chenyushao/make_word/SD160_word.py {sample} {date} {word_name}'
              ,'解码682基因':f'python /home/chenyushao/make_word/NBC650_word.py {sample} {date} {word_name}'
              , '睿明660基因': f'python /home/chenyushao/make_word/NBC650_word.py {sample} {date} {word_name}'
              , '睿明120基因': f'python /home/chenyushao/make_word/Q110_word.py {sample} {date} {word_name}'
              , '睿明80基因': f'python /home/chenyushao/make_word/Q80_word.py {sample} {date} {word_name}'
              , '睿明70基因': f'python /home/chenyushao/make_word/Gene60_rm_LangCancerTissue_word.py {sample} {date} {word_name}'
              ,'睿明66基因':f'python /home/chenyushao/make_word/Gene60_rm_LangCancerTissue_word.py {sample} {date} {word_name}'
              , '睿明65基因': f'python /home/chenyushao/make_word/Gene60_rm_LangCancerTissue_word.py {sample} {date} {word_name}'
              ,'睿明60基因':f'python /home/chenyushao/make_word/Gene60_rm_LangCancerTissue_word.py {sample} {date} {word_name}'
              ,'睿明25基因':f'python /home/chenyushao/make_word/Q80_word.py {sample} {date} {word_name}'
              ,'睿明17基因':f'python /home/chenyushao/make_word/BC17_word.py {sample} {date} {word_name}'
              ,'融享17基因': f'python /home/chenyushao/make_word/BC17_word.py {sample} {date} {word_name}'
              , '融享55基因': f'python /home/chenyushao/make_word/BC17_word.py {sample} {date} {word_name}'
              , '融享80基因': f'python /home/chenyushao/make_word/Gene65_ty_IntestinalCancerTissue_word.py {sample} {date} {word_name}'
              , '融享671基因': f'python /home/chenyushao/make_word/NBC650_word.py {sample} {date} {word_name}'
              , 'MSI': f'python /home/chenyushao/make_word/Q80_word.py {sample} {date} {word_name}'
              }
    return dict_.get(mode, f'echo no_this_mode {mode}')
    
def process(folder_path,date):
    for filename in os.listdir(folder_path):
        if filename.endswith(".summary.xlsx"):
            print(f'正在处理文件：{filename}')
            df = pd.read_excel(f'{folder_path}/{filename}', sheet_name=None)
            meta = df['meta'].fillna('')
            print(meta['样本类型*'].iloc[0],meta['报告模版'].iloc[0],meta['id'].iloc[0],meta['name'].iloc[0],meta['panel'].iloc[0])
            
            sample = meta['id'].iloc[0]
            date = date
            material_version = '组织版' if '液' not in meta['样本类型*'].iloc[0] else '血液版'
            if '-N' in meta['id'].iloc[0] and '解码682基因' in meta['报告模版'].iloc[0]:
                word_name = meta['报告模版'].iloc[0]+'对照检测报告_'+meta['name'].iloc[0]+f'_{material_version}'
            else:
                word_name = meta['报告模版'].iloc[0]+'检测报告_'+meta['name'].iloc[0]+f'_{material_version}'
            cmd = choose_channe(meta['报告模版'].iloc[0],sample,date,word_name)
            print(cmd,'\n')
            p = subprocess.Popen(cmd,shell=True)
            p.communicate()
            
if __name__=='__main__':
    # date = '20230627' # 要改改这里就够了。
    date = sys.argv[1] # '20230627'
    folder_path = "/archive/"+date
    process(folder_path,date)
