#coding=utf8 
import pandas as pd 
import warnings,re,sys
warnings.filterwarnings('ignore')

sample_list_str = sys.argv[1] # 第一个参数,先把list 变成了str方便 传参，在脚本中还原list 。
sample_list = sample_list_str.split(',')

def make_received(sample_list): # 主要就是从 读取一批文件名， 然后在 received 模版中填入 “样本编号*” 字段。 
    df = pd.read_csv('/received/received.csv',sep=',',header=1)
    if 'is_new' not in df.columns: # 打标签。
        if not df.empty:
            df['is_new'] = False # 打标签。
        else:
            df['is_new'] = None
    # print(sample_list)
    # print(df) 
    for i in sample_list:
        df = df.append({'样本编号*': i}, ignore_index=True)
    # print(df)
    with open('/received/received.csv','w')as f:
        f.write(',,患者信息,,,,,,检测项目,,,,肿瘤样本,,,,,,,,,,对照样本,,,,'+'\n')
    df.to_csv('/received/received.csv',sep=',',header=1,mode='a',index=False) # 注意 mode='a'在前者基础上保存。


def fill_received():
    try:   # 处理新加入的部分，再把新的部分和老的部分合并，用is_new 标签字段来区分。
        df_raw = pd.read_csv('/received/received.csv',sep=',',header=1)
        df_last = df_raw[df_raw['is_new'] == False]
        df = df_raw[df_raw['is_new'] != False]
        Project_2,Project_3,Project_4 = '/received/2023项目表2月.csv','/received/2023项目表3月.csv','/received/2023项目表4月.csv'
        df_ref = pd.concat([pd.read_csv(Project_2,sep=','),pd.read_csv(Project_3,sep=','),pd.read_csv(Project_4,sep=',')])
        # print(df['样本编号*'])
        df['项目编号*'] = df['样本编号*'].apply(lambda x: x.replace("-T","").replace("-N",""))
        for i in range(len(df)):
            # print(i,df['项目编号*'].iloc[i])
            # print(type(df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['客户姓名'].tolist()))
            # print('看这里:',df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]])
            df['姓名*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['客户姓名'].tolist()[0]
            df['性别'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['性别'].tolist()[0]
            df['年龄'].iloc[i] = str(float(df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['年龄'].tolist()[0]))
            df['送检医院'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['医院'].tolist()[0]
            df['肿瘤类型*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['肿瘤类型'].tolist()[0]
            df['临床诊断*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['临床诊断'].tolist()[0]
            df['样本类型*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['肿瘤样本类型'].tolist()[0]
            df['到样日期*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['到样日期'].tolist()[0]
            df['检测项目*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['检测内容'].tolist()[0].replace('+PDL1','')
            bed_match_str = df['检测项目*'].iloc[i]# 根据检测项目识别探针类型。
            num,Tissue_or_blood = re.findall(r'(\d+)基因',bed_match_str)[0],re.findall(r'(组织|液)',bed_match_str)[0]
            def choose_bed(num,Tissue_or_blood)-> str:  # 这样的dict写法其实是为了避免if else 嵌套太多，python又没有case的办法。
                options = {
                    ('17','组织'): 'BC17',('17','液'): 'BC17',
                    ('20','组织'): 'Q80',('20','液'): 'Q80', ('21','组织'): 'Q80',('21','液'): 'Q80',('25','组织'): 'Q80',('25','液'): 'Q80',('80','组织'): 'Q80',('80','液'): 'Q80',
                    ('110','组织'): 'Q120',('110','液'): 'Q120',
                    ('160','组织'): 'SD160',('160','液'): 'SD160',('223','组织'): 'SD160',('223','液'): 'SD160',
                    ('682','组织'): 'BCP650', ('624','组织'): 'BCP650',
                    ('682','液'): 'NBC650', ('624','液'): 'NBC650'
                }
                return options.get((num,Tissue_or_blood),'您需要的panel不存在，请核查panel情况。')
            df['探针*'].iloc[i] = choose_bed(num,Tissue_or_blood)
        df['探针仅仅保留数字'] = df['探针*'].str.replace(r'[^0-9]', '')
        df['报告模板*'] = '解码'+df['探针仅仅保留数字'] +'基因'
        df = df.drop(columns=['探针仅仅保留数字'])
        df['is_new'] = False
        if not df_last.empty:      # 这里小心一点，一旦是空的df，会让bool值变成 0.0 这样的形式。
            df_result = pd.concat([df_last,df])
            return df_result
        return df
        # if df['姓名*'].iloc[i] != None:           # Project_2 中找到了匹配的，就跳过Project_3.
        #     return df 
    except Exception as e:
        print(e)
        df = pd.read_csv('/received/received.csv',sep=',',header=1)
        df['is_new'] = False
        return df
   
if __name__=='__main__':
  
    make_received(sample_list)
    
    df_result = fill_received()
    print(df_result[['样本编号*','姓名*','性别','年龄','肿瘤类型*','临床诊断*','送检医院','探针*','检测项目*','报告模板*','样本类型*','到样日期*']])
    with open('/received/received.csv','w')as f:
        f.write(',,患者信息,,,,,,检测项目,,,,肿瘤样本,,,,,,,,,,对照样本,,,,'+'\n')
    df_result.to_csv('/received/received.csv',sep=',',header=1,mode='a',index=False)
    
    

