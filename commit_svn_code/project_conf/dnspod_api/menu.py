#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import sys
'''00000000000000000000000000'''
from Dnspod import Procedure


product = int(input('\t\t\033[4mDndpod账号\033[0m\n\n'
               '\t\033[34m1\033[0m\tB79市场部账号\n'
               '\t\033[34m2\033[0m\tB79产品账号\n'
               '\t\033[34m3\033[0m\tNWF账号\n\n'
              '请输入本次要操作的账号：'))
#Token and CNAME_Record init
if product == 1:
    #B79市场部
    Login_Token = '69449,16e3ee1cdcebe4e35df337cd497516f1'
elif product == 2:
    #B79产品
    Login_Token = '69573,d1b29ec7f5f1e544b6b6ea0a2a0a0a3f'
elif product == 3:
    #NWF:E03/E04
    Login_Token = '69572,79b1ac75539e5683cb01f391cb844e91'
elif product == 4:
    Login_Token = '71226,e401aa9005d303d1af32b37dce0eb5d8'    
else:
    print('输入错误，请重新输入.')
    sys.exit(0)


choose = input("\n\n\t\t \033[4m功能说明\033[0m\n\n"
               "\t\033[34m1\033[0m \t批量添加域名和解析记录(TCBS运维部添加域名批量操作)\n\n"
               #"\t\033[34m2\033[0m \t添加解析记录\n"
               #"\t\033[34m3\033[0m \t修改解析记录\n"
               #"\t\033[34m4\033[0m \t删除域名\n"
               #"\t\033[34m5\033[0m \t删除解析记录\n"
               #"\t\033[34m6\033[0m \t获取域名列表\n\n"
               "请输入您要操作任务的序号：")

Setup_DICT = {'1':'running.Add_Domain_And_Record()',
        '2':'running.Add_Record()',
        '3':'running.Alter_Record()',
        '4':'running.Del_Domain()',
        '5':'running.Del_Record()',
        '6':'running.Get_Domain_List()'}

running = Procedure(Login_Token)
exec(Setup_DICT[choose])
