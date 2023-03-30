#coding=utf8 
import pandas as pd 
import warnings,re 
warnings.filterwarnings('ignore')


def make_received():
    df = pd.read_csv('/received/received.csv',sep=',',header=1)
    Project_2,Project_3 = '/received/2023项目表2月.csv','/received/2023项目表3月.csv'
    df_ref = pd.concat([pd.read_csv(Project_2,sep=','),pd.read_csv(Project_3,sep=',')])
    print(df['样本编号*'])
    df['项目编号*'] = df['样本编号*'].apply(lambda x: x.replace("-T","").replace("-N",""))
    df['探针仅仅保留数字'] = df['探针*'].str.replace(r'[^0-9]', '')
    df['报告模板*'] = '解码'+df['探针仅仅保留数字'] +'基因'
    df = df.drop(columns=['探针仅仅保留数字'])
    for i in range(len(df)):
        # print(i)
        # print(type(df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['客户姓名'].tolist()))
        # print(df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]])
        df['姓名*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['客户姓名'].tolist()[0]
        df['性别'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['性别'].tolist()[0]
        df['年龄'].iloc[i] = str(float(df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['年龄'].tolist()[0]))
        df['送检医院'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['医院'].tolist()[0]
        df['肿瘤类型*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['肿瘤类型'].tolist()[0]
        df['临床诊断*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['临床诊断'].tolist()[0]
        df['样本类型*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['肿瘤样本类型'].tolist()[0]
        df['到样日期*'].iloc[i] = df_ref[df_ref['客户编号']==df['项目编号*'].iloc[i]]['到样日期'].tolist()[0]
    return df
    # if df['姓名*'].iloc[i] != None:           # Project_2 中找到了匹配的，就跳过Project_3.
    #     return df 
        
df_result = make_received()
print(df_result[['样本编号*','姓名*','性别','年龄','肿瘤类型*','临床诊断*','送检医院','探针*','检测项目*','报告模板*','样本类型*','到样日期*']])
with open('/received/received.csv','w')as f:
    f.write(',,患者信息,,,,,,检测项目,,,,肿瘤样本,,,,,,,,,,对照样本,,,,'+'\n')
df_result.to_csv('/received/received.csv',sep=',',header=1,mode='a',index=False)

