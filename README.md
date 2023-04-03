# Bioinformatics_automation
生信自动化相关
以下是 “批处理” 自动化流程的 具体操作顺序：
1、下载文件；auto_down_oss.sh  （在/home/chenyushao下）。
2、生成received.csv文件；先上传 2023项目表2月.csv\ 2023项目表3月.csv\ received.csv（至少写好样本编号和探针两列），再 make_received_csv.py（在/received下）。
3、生成 config.ini 文件,以及 received文件夹下 的 BC17_received.csv 等等文件 （为主要的批处理程序做好最后准备）；make_config.py（~/py_generate下）。
4、正式开始批处理流程；total_connect_env.py（~/py_generate下）。
5、收集批处理结果，并制作summary文件以日期命名；batch_summary_collect.py。
6、一个一个手动生成 word 报告；production_report.py （~/doctor_assign_tasks/生成word报告  文件夹下）。
