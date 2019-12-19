#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from my_logger import mylogger

'''
Global_Var   - 通用变量

'''



class Global_Var:
    '''通用变量'''
    def __init__(self,Login_Token):
        self.Login_Token = Login_Token
        self.Format = 'json'

        #self.Batch_Add_Domain_URL = 'https://dnsapi.cn/Batch.Record.Create'  #批量添加域名
        #self.Batch_Add_Record_URL = 'https://dnsapi.cn/Batch.Record.Create'  #批量添加记录
        #self.Alter_Record_URL = 'https://dnsapi.cn/Batch.Record.Modify'     #批量修改记录

        self.Add_Domain_URL = 'https://dnsapi.cn/Domain.Create'             #添加域名
        self.Add_Record_URL = 'https://dnsapi.cn/Record.Create'             #添加记录
        #self.Alter_Record_URL = 'https://dnsapi.cn/Record.Modify'          #修改记录
        #self.Get_Record_URL = 'https://dnsapi.cn/Record.List'              #获取记录列表
        #self.Del_Domain_URL = 'https://dnsapi.cn/Domain.Remove'            #删除域名
        #self.Del_Record_URL = 'https://dnsapi.cn/Record.Remove'            #删除记录
        #self.Get_Domain_List_URL = 'https://dnsapi.cn/Domain.List'         #获取域名列表
        self.mat = "{:20}\t{:20}\t{:40}\t{:30}"

        self.B79_supermaket_record = {'@':'your record','www':'your record','m':'your record'}
        self.B79_product_record = {'@':'your record5','www':'your record','m':'your record'}
        self.E03_record = {'@':'your record','www':'your record','m':'your record'}
        self.E04_record = {'@':'your record','www':'your record','m':'your record'}


class Dns_Supermaket_Operating(Global_Var):
    '''添加域名或解析'''
    def Add_Domain(self,Domains_List):
        '''添加域名'''
        pass
#        for Domain in Domains_List:
#            r = requests.post(self.Add_Domain_URL, data={'login_token': self.Login_Token,
#                                                         'format': self.Format,
#                                                         'domain': Domain,
#                                                         })
#            response_record_json = r.json()
#            if response_record_json["status"]["code"] == "1":
#                #打印信息并写入日志
#                print('域名：\033[32m{}\033[0m 添加成功；域名ID：\033[32m{}\033[0m'.format(response_record_json["domain"]["domain"], response_record_json["domain"]["id"])
#                mylogger.info('本次操作人：--- ；域名：{} 添加成功；域名ID：{}'.format(response_record_json["domain"]["domain"], response_record_json["domain"]["id"]))
#
#            else:
#                print('域名：\033[31m{}\033[0m 添加失败,错误信息：\033[31m{}\033[0m'.format(Domain, response_record_json["status"]["message"]))
#                mylogger.error('本次操作人：--- ；域名：{} 添加失败,错误信息：{}'.format(Domain, response_record_json["status"]["message"]))


    def Add_Record(self,select,Domains_List,Record_Type,Record_Line,Domain_Status):
        '''添加解析'''
        if select == 'b79_s':
            for Domain in Domains_List:
                for Sub_Domain in self.B79_product_record.keys():
                    Value = self.B79_product_record[Sub_Domain]
                    r = requests.post(self.Add_Record_URL, data={'login_token': self.Login_Token,
                                                                 'format': self.Format,
                                                                 'domain': Domain,
                                                                 'sub_domain': Sub_Domain,
                                                                 'record_type': Record_Type,
                                                                 'record_line': Record_Line,
                                                                 'value': Value,
                                                                 'status': Domain_Status
                                                                 })
                    response_record_json = r.json()
                    if response_record_json["status"]["code"] == "1":
                        print('域名：\033[32m{}\033[0m 添加记录：\033[32m{}\033[0m 成功'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('本次操作人：--- ；域名：{} 添加记录 {} 成功'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('域名：\033[31m{}\033[0m 添加记录：\033[31m{}\033[0m 失败，错误信息：\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
        elif select == 'b79_p':
            for Domain in Domains_List:
                for Sub_Domain in self.B79_product_record.keys():
                    Value = self.B79_product_record[Sub_Domain]
                    r = requests.post(self.Add_Record_URL, data={'login_token': self.Login_Token,
                                                                 'format': self.Format,
                                                                 'domain': Domain,
                                                                 'sub_domain': Sub_Domain,
                                                                 'record_type': Record_Type,
                                                                 'record_line': Record_Line,
                                                                 'value': Value,
                                                                 'status': Domain_Status
                                                                 })
                    response_record_json = r.json()
                    if response_record_json["status"]["code"] == "1":
                        print('域名：\033[32m{}\033[0m 添加记录：\033[32m{}\033[0m 成功'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('本次操作人：--- ；域名：{} 添加记录 {} 成功'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('域名：\033[31m{}\033[0m 添加记录：\033[31m{}\033[0m 失败，错误信息：\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
        elif select == 'e03':
            for Domain in Domains_List:
                for Sub_Domain in self.E03_record.keys():
                    Value = self.E03_record[Sub_Domain]
                    r = requests.post(self.Add_Record_URL, data={'login_token': self.Login_Token,
                                                                 'format': self.Format,
                                                                 'domain': Domain,
                                                                 'sub_domain': Sub_Domain,
                                                                 'record_type': Record_Type,
                                                                 'record_line': Record_Line,
                                                                 'value': Value,
                                                                 'status': Domain_Status
                                                                 })
                    response_record_json = r.json()
                    if response_record_json["status"]["code"] == "1":
                        print('域名：\033[32m{}\033[0m 添加记录：\033[32m{}\033[0m 成功'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('本次操作人：--- ；域名：{} 添加记录 {} 成功'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('域名：\033[31m{}\033[0m 添加记录：\033[31m{}\033[0m 失败，错误信息：\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
                        mylogger.info('本次操作人：--- ；域名：{} 添加记录 {} 失败,错误信息：{}'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
        elif select == 'e04':
            for Domain in Domains_List:
                for Sub_Domain in self.E04_record.keys():
                    Value = self.E04_record[Sub_Domain]
                    r = requests.post(self.Add_Record_URL, data={'login_token': self.Login_Token,
                                                                 'format': self.Format,
                                                                 'domain': Domain,
                                                                 'sub_domain': Sub_Domain,
                                                                 'record_type': Record_Type,
                                                                 'record_line': Record_Line,
                                                                 'value': Value,
                                                                 'status': Domain_Status
                                                                 })
                    response_record_json = r.json()
                    if response_record_json["status"]["code"] == "1":
                        print('域名：\033[32m{}\033[0m 添加记录：\033[32m{}\033[0m 成功'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('本次操作人：--- ；域名：{} 添加记录 {} 成功'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('域名：\033[31m{}\033[0m 添加记录：\033[31m{}\033[0m 失败，错误信息：\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
