#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from Dnsapi import *
import sys


class Procedure(Global_Var):
    def Add_Domain_And_Record(self):
        Domains_List = []
        with open('domain.txt', 'r+') as D:
            for d in D.readlines():
                Domains_List.append(d.strip())

        Product = int(input('\t\t\033[4m解析记录选择\033[0m\n\n'
                        '\t\033[34m1\033[0m\tB79市场域名解析记录\n'
                        '\t\033[34m2\033[0m\tB79产品域名解析记录\n'
                        '\t\033[34m3\033[0m\tE03解析记录\n'
                        '\t\033[34m4\033[0m\tE04解析记录\n\n'
                        '请选择要操作的解析记录：'))

        running = Dns_Supermaket_Operating(self.Login_Token)
        Record_Type = 'CNAME'
        Record_Line = '默认'
        Domain_Status = 'disable'

        if Product == 1:
            running.Add_Domain(Domains_List)
            running.Add_Record('b79_s',Domains_List,Record_Type,Record_Line,Domain_Status)
        elif Product == 2:
            running.Add_Domain(Domains_List)
            running.Add_Record('b79_p',Domains_List,Record_Type,Record_Line,Domain_Status)
        elif Product == 3:
            running.Add_Domain(Domains_List)
            running.Add_Record('e03',Domains_List,Record_Type,Record_Line,Domain_Status)
        elif Product == 4:
            running.Add_Domain(Domains_List)
            running.Add_Record('e04',Domains_List,Record_Type,Record_Line,Domain_Status)
        elif Product == 5:
            running.Add_Domain(Domains_List)
            running.Add_Record('b88',Domains_List,Record_Type,Record_Line,Domain_Status)           
        else:
            print('\033[31m未知解析记录，请重新选择.\033[0m')
            sys.exit(0)