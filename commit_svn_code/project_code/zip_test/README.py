
###################  使用方法

'''
1. 建议使用python3.X
2. 需要安装requests模块
..
'''

#################  login_token的说明
API Token 生成方法详见：https://support.dnspod.cn/Kb/showarticle/tsid/227/，完整的 API Token 是由 ID,Token 组合而成的，用英文的逗号分割。

###################  文件简介

'''

'''

#####################  API

'''

self.Add_Domain_URL = 'https://dnsapi.cn/Domain.Create'           # 添加域名
self.Del_Domain_URL = 'https://dnsapi.cn/Domain.Remove'           # 删除域名
self.Add_Record_URL = 'https://dnsapi.cn/Record.Create'           # 添加记录
#self.Alter_Record_URL = 'https://dnsapi.cn/Record.Modify'      #修改记录
self.Alter_Record_URL = 'https://dnsapi.cn/Batch.Record.Modify'   # 批量修改记录
self.Get_Record_URL = 'https://dnsapi.cn/Record.List'             # 获取记录列表
self.Del_Record_URL = 'https://dnsapi.cn/Record.Remove'           # 删除记录
self.Get_Domain_List_URL = 'https://dnsapi.cn/Domain.List'        # 获取域名列表

'''

################### 参数解析

#子域名                  Sub_Domian
#记录类型                Record_Type
#记录线路                Record_Line
#解析记录值              Value
#域名                   domain
#记录ID                 record_id
#子域名                  sub_domain
#记录值                  alue
#记录类型                record_type
#记录线路                record_line
