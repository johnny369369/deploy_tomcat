#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import requests
from mysql_common import *



class Public_parameter(object):
    '''公共参数'''
    def __init__(self, login_token=None, Format='json', lang='en', error_on_empty='no'):
        self.Login_Token = login_token
        self.Format = Format
        self.Lang = lang
        self.Error_on_empty = error_on_empty

        #self.Response_record_file = 'record_log.txt'
        self.Add_Domain_URL = 'https://dnsapi.cn/Domain.Create'             # 添加域名
        self.Del_Domain_URL = 'https://dnsapi.cn/Domain.Remove'             # 删除域名
        self.Get_Domain_List_URL = 'https://dnsapi.cn/Domain.List'          # 获取域名列表
        self.Set_Domain_Status_URL = 'https://dnsapi.cn/Domain.Status'      # 设置域名状态
        self.Add_Record_URL = 'https://dnsapi.cn/Record.Create'             # 添加记录
        self.Get_Record_URL = 'https://dnsapi.cn/Record.List'               # 获取记录列表
        self.Modify_Record_URL = 'https://dnsapi.cn/Record.Modify'          # 修改记录
        self.Remove_Record_URL = 'https://dnsapi.cn/Record.Remove'          # 删除记录

        self.data = {
            'login_token': self.Login_Token,
            'format': self.Format,
            'lang': self.Lang,
            'error_on_empty': self.Error_on_empty
        }



class Dnspod_Api_Domain(Public_parameter):
    '''域名'''
    def add_domain(self, domain, group_id=None, is_mark=None):
        return_data = {}
        self.data['domain'] = domain

        try:
            r = requests.post(url=self.Add_Domain_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Add_Domain_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            data = {}

            if return_data['status'] == 'fail':
                data['code'] = result_json['status']['code']
                return_data['data'] = data
            else:
                data['domain_id'] = result_json['domain']['id']
                data['status'] = 'enable'
                data['name'] = result_json['domain']['domain']

                return_data['data'] = data

            return return_data


    def delete_domain(self, domain, status='disable'):
        return_data = {}
        self.data['domain'] = domain
        self.data['status'] = status

        try:
            r = requests.post(url=self.Del_Domain_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            data = {}
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']

            data['name'] = domain
            return_data['data'] = data

            return return_data


    def set_domain_status(self, domain, status='enable'):
        return_data = {}
        self.data['domain'] = domain
        self.data['status'] = status

        try:
            r = requests.post(url=self.Set_Domain_Status_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            data = {}
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']

            data['change_to'] = {'status': status}
            data['domain'] = {'name': domain}
            return_data['data'] = data

            return return_data


    def get_domain_list(self, Type='all', offset=None, length=None, group_id=None, keyword=None):
        return_data = {}
        self.data['length'] = length

        try:
            r = requests.post(url=self.Get_Domain_List_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            data = {'info': {}, 'domains': []}

            if return_data['status'] == 'fail':
                pass
            else:
                data['info'] = result_json['info']
                for D in result_json['domains']:
                    data['domains'].append(D)
                return_data['data'] = data

            return return_data



class Dnspod_Api_Record(Public_parameter):
    '''记录'''
    def add_record(self, domain, sub_domain, record_type, record_line, value, mx=None, ttl=None, status=None):
        return_data = {}
        self.data['domain'] = domain
        self.data['sub_domain'] = sub_domain
        self.data['record_type'] = record_type
        self.data['record_line'] = record_line
        self.data['value'] = value
        self.data['mx'] = mx
        self.data['ttl'] = ttl
        self.data['status'] = status

        try:
            r = requests.post(url=self.Add_Record_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            data = {}

            if return_data['status'] == 'fail':
                data['code'] = result_json['status']['code']
                return_data['data'] = data
            else:
                data['record_id'] = result_json['record']['id']
                data['sub_domain'] = result_json['record']['name']
                data['record_line'] = record_line
                data['record_type'] = record_type
                data['ttl'] = ttl if ttl else 600
                data['value'] = value
                data['status'] = result_json['record']['status']
                data['belong_domain'] = domain
                return_data['data'] = data

            return return_data


    def modify_record(self, record_id, domain, sub_domain, record_type, record_line, value, mx=None, ttl=None, status=None):
        return_data = {}
        self.data['record_id'] = record_id
        self.data['domain'] = domain
        self.data['sub_domain'] = sub_domain
        self.data['record_type'] = record_type
        self.data['record_line'] = record_line
        self.data['value'] = value
        self.data['mx'] = mx
        self.data['ttl'] = ttl
        self.data['status'] = status

        try:
            r = requests.post(url=self.Modify_Record_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            data = {}

            if return_data['status'] == 'fail':
                data['code'] = result_json['status']['code']
                return_data['data'] = data
            else:
                data['record_id'] = result_json['record']['id']
                data['domain'] = domain
                data['sub_domain'] = result_json['record']['name']
                data['value'] = result_json['record']['value']
                data['domain_status'] = result_json['record']['status']
                return_data['data'] = data

            return return_data


    def remove_record(self, domain, record_id):
        return_data = {}
        self.data['domain'] = domain
        self.data['record_id'] = record_id

        try:
            r = requests.post(url=self.Remove_Record_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            return_data['data'] = {}

            return return_data


    def get_record_list(self, domain, offset=None, length=None, sub_domain=None, record_type=None, record_line=None, keyword=None):
        return_data = {}
        self.data['domain'] = domain
        self.data['sub_domain'] = sub_domain
        self.data['record_type'] = record_type
        self.data['record_line'] = record_line
        self.data['length'] = length

        try:
            r = requests.post(url=self.Get_Record_URL, data=self.data)
            result_json = r.json()
        except Exception as e:
            return_data['status'] = 'Error'
            return_data['message'] = f"{self.Get_Domain_List_URL} 连接失败: {e.__str__()}"
            return return_data
        else:
            return_data['status'] = 'success' if result_json['status']['code'] == '1' else 'fail'
            return_data['message'] = result_json['status']['message']
            data = {'info': {}, 'records': []}

            if return_data['status'] == 'fail':
                pass
            else:
                data['info'] = result_json['info']
                for r in result_json['records']:
                    data['records'].append(r)
                return_data['data'] = data

            return return_data




# if __name__ == '__main__':
    # d = Dnspod_api_record(login_token='71226,e401aa9005d303d1af32b37dce0eb5d8')
    # print(d.get_record_list('zywx100.live', length=3, sub_domain='www'))

    # insert_data = {}
    # m = My_mysql()

    # domain_list
    # d = Dnspod_api_Domain(login_token='71226,e401aa9005d303d1af32b37dce0eb5d8')
    # domain_result = d.get_domain_list()
    # for data in domain_result['data']['domains']:
    #     insert_data['domain_id'] = data['id']
    #     insert_data['status'] = data['status']
    #     insert_data['ttl'] = data['ttl']
    #     insert_data['name'] = data['name']
    #     insert_data['owner'] = data['owner']
    #     insert_data['records'] = data['records']
    #     m.insert('domain_list', insert_data=insert_data)

    # record_list
    # r = Dnspod_api_record(login_token='71226,e401aa9005d303d1af32b37dce0eb5d8')
    # domains = m.get('domain_list', ['name'],condition='limit 1' )
    # for d in domains:
    #     record_list = r.get_record_list(d)['data']['records']
    #     for record_result in record_list:
    #         insert_data['record_id'] = record_result['id']
    #         insert_data['sub_domain'] = record_result['name']
    #         insert_data['record_line'] = record_result['line']
    #         insert_data['record_type'] = record_result['type']
    #         insert_data['ttl'] = record_result['ttl']
    #         insert_data['value'] = record_result['value']
    #         insert_data['status'] = record_result['status']
    #         insert_data['belong_domain'] = d[0]
    #         print(insert_data)
    #         m.insert('record_list', insert_data=insert_data)


