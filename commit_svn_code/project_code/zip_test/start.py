#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import sys
from mysql_common import *
import dnspod_api
import threading



def menu(Login_Token, you_arg):
    '''菜单'''

    domain_first = input('\033[33m请输入要操作的域名(已,为分隔符),留空则从文件读入域名：\033[0m')
    with open('/opt/dnspod_api/domain.txt', 'r') as f:
        domain_second = domain_first.split(',') if domain_first else f.read().splitlines()

    domain_api_instance = dnspod_api.Dnspod_Api_Domain(Login_Token)
    record_api_instance = dnspod_api.Dnspod_Api_Record(Login_Token)
    my_mysql_instance = My_mysql()
    insert_data = {}

    while True:
        choose = int(input("\n\n\t\t \033[4m功能说明\033[0m\n\n"
                       "\t\033[34m1\033[0m \t添加域名\n"
                       "\t\033[34m2\033[0m \t删除域名\n"
                       "\t\033[34m3\033[0m \t设置域名状态\n"
                       "\t\033[34m4\033[0m \t添加记录\n"
                       "\t\033[34m5\033[0m \t修改记录\n"
                       "\t\033[34m6\033[0m \t查询功能(域名和记录列表)\n"
                       "\t\033[34m7\033[0m \t退出\n\n"
                       "\033[33m请输入您要操作任务的序号：\033[0m"))

        if choose == 1:
            # threads = []
            for d in domain_second:
                return_data = domain_api_instance.add_domain(d)
                if return_data['status'] == 'success':
                    print(f"\033[32m域名{d}添加成功，并存入DB \033[0m")
                    my_mysql_instance.insert('domain_list', return_data['data'])
                else:
                    print(f"\033[31m域名{d}添加失败，失败原因：{return_data['message']}\033[0m")

        elif choose == 2:
            for d in domain_second:
                return_data = domain_api_instance.delete_domain(d)
                if return_data['status'] == 'success':
                    print(f"\033[32m域名{d}删除成功，从DB去除 \033[0m")
                    my_mysql_instance.delete('domain_list', return_data['data'])
                else:
                    print(f"\033[31m域名{d}删除失败，失败原因：{return_data['message']}\033[0m")

        elif choose == 3:
            statu = input('\033[33m将域名状态修改为(enable|disable)：\033[0m')
            for d in domain_second:
                return_data = domain_api_instance.set_domain_status(d, status=statu)
                if return_data['status'] == 'success':
                    print(f"\033[32m域名{d}修改状态成功，更新DB状态 \033[0m")
                    my_mysql_instance.update('domain_list', return_data['data']['change_to'], return_data['data']['domain'])
                else:
                    print(f"\033[31m域名{d}修改状态失败，失败原因：{return_data['message']}\033[0m")

        elif choose == 4:
            input('从文件导入添加记录，请确认record.txt文件，回车继续...')
            with open('/opt/dnspod_api/record.txt', 'r') as f:
                for r in f.readlines():
                    l = r.strip().split()
                    return_data = record_api_instance.add_record(*l)
                    if return_data['status'] == 'success':
                        print(f"\033[32m域名{l[0]}添加主机头{l[1]}、记录类型{l[2]}到记录{l[4]}成功，并存入DB \033[0m")
                        my_mysql_instance.insert('record_list', return_data['data'])
                    else:
                        print(f"\033[31m域名{l[0]}添加记录失败，失败原因：{return_data['message']}\033[0m")

        elif choose == 5:
            pass

        elif choose == 6:
            select_table = input('\033[33m请输入要查询的表(domain_list|record_list)：\033[0m')
            print('''\033[33m\tdomain_list可供查询的列：\033[0mID,domain_id,status,ttl,name,owner,records\n\033[33m\trecord_list可供查询的列：\033[0mrecord_id,sub_domain,record_line,record_type,ttl,value,status,belong_domain''')
            select_l = input('\033[33m请输入要查询的列(以,分隔),回车查询所有列：\033[0m')
            select_list = select_l.split(',') if select_l else '*'
            condition = input("\033[33m请输入要查询过滤的条件(例: domain_id=111 and name='a.com'),回车全部查找：\033[0m")

            return_data = my_mysql_instance.get(select_table, select_list, condition=condition) if condition else my_mysql_instance.get(select_table, select_list)
            print(f"\n\033[35m-->查询结果:\033[0m\n"
                  f"\033[032m本次查询列：\033[0m\n{select_list}\n\033[032m对应结果:\033[0m")
            for r in return_data:
                print(r)

        #elif choose == 7:
        #    # add domain
        #    for d in domain_second:
        #        return_data = domain_api_instance.add_domain(d)
        #        if return_data['status'] == 'success':
        #            print(f"\033[32m域名{d}添加成功，并存入DB \033[0m")
        #            my_mysql_instance.insert('domain_list', return_data['data'])
        #        else:
        #            print(f"\033[31m域名{d}添加失败，失败原因：{return_data['message']}\033[0m")
        #    # add record
        #    record_type = 'CNAME'
        #    record_line = '默认'
        #    for d in domain_second:
        #        for k,v in you_arg.items():
        #            return_data = record_api_instance.add_record(d, k, record_type,record_line, v)
        #            if return_data['status'] == 'success':
        #                print(f"\033[32m域名{d}添加主机头{k}到记录{v}成功，并存入DB \033[0m")
        #                my_mysql_instance.insert('record_list', return_data['data'])
        #            else:
        #                print(f"\033[31m域名{d}添加记录失败，失败原因：{return_data['message']}\033[0m")

        else:
            sys.exit(0)



if __name__ == '__main__':
    My_Login_Token = 'you_login_token'

    select_product = sys.argv[1]
    if select_product == 'aaa':
        menu(My_Login_Token, 'you_arg')
    elif select_product == 'bbb':
        pass
    else:
        print('''
        未找到对应产品，请检查!
        用法：
            python start.py you_arg
        ''')


