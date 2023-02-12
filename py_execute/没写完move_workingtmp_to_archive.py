# coding=utf-8 

# 情况一：workingtmp 出现archive 没有的dir，则在archive中新建一个dir，放进去要的东西。
# 情况二：workingtmp 已有文件夹（如288）中 出现 archive 对应文件夹（如288）中未出现的文件
#         ，则cp 此文件 进archive 对应文件夹（如288）中。

import os,configparser
config = configparser.ConfigParser()
config.read('config.ini')
generate_location = config['generate']['location']   # "/working_tmp"
archive_location = config['archive']['location']     # '/archive'

working_tmp_list = os.listdir(generate_location)
archive_list = os.listdir(archive_location)
for working_tmp_ele in working_tmp_list:
    print(working_tmp_ele)
    if working_tmp_ele not in archive_list:
        os.mkdir(archive_location + "/"+ working_tmp_ele)
