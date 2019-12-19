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

        Product = int(input('\t\t\033[4m������¼ѡ��\033[0m\n\n'
                        '\t\033[34m1\033[0m\tB79�г�����������¼\n'
                        '\t\033[34m2\033[0m\tB79��Ʒ����������¼\n'
                        '\t\033[34m3\033[0m\tE03������¼\n'
                        '\t\033[34m4\033[0m\tE04������¼\n\n'
                        '��ѡ��Ҫ�����Ľ�����¼��'))

        running = Dns_Supermaket_Operating(self.Login_Token)
        Record_Type = 'CNAME'
        Record_Line = 'Ĭ��'
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
            print('\033[31mδ֪������¼��������ѡ��.\033[0m')
            sys.exit(0)