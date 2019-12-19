#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from my_logger import mylogger

'''
Global_Var   - ͨ�ñ���

'''



class Global_Var:
    '''ͨ�ñ���'''
    def __init__(self,Login_Token):
        self.Login_Token = Login_Token
        self.Format = 'json'

        #self.Batch_Add_Domain_URL = 'https://dnsapi.cn/Batch.Record.Create'  #�����������
        #self.Batch_Add_Record_URL = 'https://dnsapi.cn/Batch.Record.Create'  #������Ӽ�¼
        #self.Alter_Record_URL = 'https://dnsapi.cn/Batch.Record.Modify'     #�����޸ļ�¼

        self.Add_Domain_URL = 'https://dnsapi.cn/Domain.Create'             #�������
        self.Add_Record_URL = 'https://dnsapi.cn/Record.Create'             #��Ӽ�¼
        #self.Alter_Record_URL = 'https://dnsapi.cn/Record.Modify'          #�޸ļ�¼
        #self.Get_Record_URL = 'https://dnsapi.cn/Record.List'              #��ȡ��¼�б�
        #self.Del_Domain_URL = 'https://dnsapi.cn/Domain.Remove'            #ɾ������
        #self.Del_Record_URL = 'https://dnsapi.cn/Record.Remove'            #ɾ����¼
        #self.Get_Domain_List_URL = 'https://dnsapi.cn/Domain.List'         #��ȡ�����б�
        self.mat = "{:20}\t{:20}\t{:40}\t{:30}"

        self.B79_supermaket_record = {'slot':'slotweb.mktcname.com','@':'yyweb.mktcname.com','www':'yyweb.mktcname.com','m':'b79_mobile.mktcname.com','999':'b79gi.cdnp4.com','vip':'b79_vipweb.mktcname.com','vipm':'b79_vipmobile.mktcname.com'}
        self.B79_product_record = {'slot':'slotweb.cdnspod.com.','@':'218.253.216.145','www':'218.253.216.145','m':'b79_mobile.cdnspod.com.','999':'b79gi.cdnspod.com.','vip':'b79_vipweb.cdnspod.com','vipm':'b79_vipmobile.cdnspod.com'}
        self.E03_record = {'@':'e03web.cdnv7.com','www':'e03web.cdnv7.com','999':'e03gi.cdnp4.com','m':'e03_mobile.cdnv7.com'}
        self.E04_record = {'999':'e04gi.cdnp4.com','@':'e04web.cdnv8.com','www':'e04web.cdnv8.com','m':'e04_mobile.cdnv8.com'}


class Dns_Supermaket_Operating(Global_Var):
    '''������������'''
    def Add_Domain(self,Domains_List):
        '''�������'''
        pass
#        for Domain in Domains_List:
#            r = requests.post(self.Add_Domain_URL, data={'login_token': self.Login_Token,
#                                                         'format': self.Format,
#                                                         'domain': Domain,
#                                                         })
#            response_record_json = r.json()
#            if response_record_json["status"]["code"] == "1":
#                #��ӡ��Ϣ��д����־
#                print('������\033[32m{}\033[0m ��ӳɹ�������ID��\033[32m{}\033[0m'.format(response_record_json["domain"]["domain"], response_record_json["domain"]["id"])
#                mylogger.info('���β����ˣ�--- ��������{} ��ӳɹ�������ID��{}'.format(response_record_json["domain"]["domain"], response_record_json["domain"]["id"]))
#
#            else:
#                print('������\033[31m{}\033[0m ���ʧ��,������Ϣ��\033[31m{}\033[0m'.format(Domain, response_record_json["status"]["message"]))
#                mylogger.error('���β����ˣ�--- ��������{} ���ʧ��,������Ϣ��{}'.format(Domain, response_record_json["status"]["message"]))


    def Add_Record(self,select,Domains_List,Record_Type,Record_Line,Domain_Status):
        '''��ӽ���'''
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
                        print('������\033[32m{}\033[0m ��Ӽ�¼��\033[32m{}\033[0m �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('���β����ˣ�--- ��������{} ��Ӽ�¼ {} �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('������\033[31m{}\033[0m ��Ӽ�¼��\033[31m{}\033[0m ʧ�ܣ�������Ϣ��\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
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
                        print('������\033[32m{}\033[0m ��Ӽ�¼��\033[32m{}\033[0m �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('���β����ˣ�--- ��������{} ��Ӽ�¼ {} �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('������\033[31m{}\033[0m ��Ӽ�¼��\033[31m{}\033[0m ʧ�ܣ�������Ϣ��\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
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
                        print('������\033[32m{}\033[0m ��Ӽ�¼��\033[32m{}\033[0m �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('���β����ˣ�--- ��������{} ��Ӽ�¼ {} �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('������\033[31m{}\033[0m ��Ӽ�¼��\033[31m{}\033[0m ʧ�ܣ�������Ϣ��\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
                        mylogger.info('���β����ˣ�--- ��������{} ��Ӽ�¼ {} ʧ��,������Ϣ��{}'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))
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
                        print('������\033[32m{}\033[0m ��Ӽ�¼��\033[32m{}\033[0m �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                        mylogger.info('���β����ˣ�--- ��������{} ��Ӽ�¼ {} �ɹ�'.format(Domain, response_record_json["record"]["name"]))
                    else:
                        print('������\033[31m{}\033[0m ��Ӽ�¼��\033[31m{}\033[0m ʧ�ܣ�������Ϣ��\033[31m{}\033[0m'.format(Domain, Sub_Domain,response_record_json["status"]["message"]))