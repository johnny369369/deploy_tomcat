#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import pymysql
from functools import wraps

# 定义数据库信息
host = 'host'
db = 'mysql_db'
user = 'mysql_user'
password = 'db_password'


class My_mysql(object):
    '''mysql操作'''

    def __init__(self, host=host, user=user, password=password, db=db):
        self._host = host
        self._user = user
        self._password = password
        self._db = db


    def safe_operation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                params = {
                        'host': self._host,
                        'user': self._user,
                        'password': self._password,
                        'database': self._db
                        }
                self.__connect = pymysql.connect(**params)
                self.__cursor = self.__connect.cursor()

                return func(self, *args, **kwargs)
            except Exception as e:
                print(e.__str__())
                self.__connect.rollback()
            finally:
                self.__cursor.close()
                self.__connect.close()
        return wrapper

    @safe_operation
    def insert(self, table, insert_data):
        key = (',').join(insert_data.keys())
        value = tuple(insert_data.values())
        sql = f"insert into {table} ({key}) values {value}"

        self.__cursor.execute(sql)
        self.__connect.commit()

    @safe_operation
    def update(self, table, update_data, condition=None):
        update_data = (',').join([ f"{k}='{v}'" for k,v in update_data.items() ])

        if condition:
            condition = (' and ').join([ f"{k}='{v}'" for k,v in condition.items() ])
            sql = f"update {table} set {update_data} where {condition}"
            self.__cursor.execute(sql)
            self.__connect.commit()
        else:
            sql = f"update {table} set {update_data}"
            self.__cursor.execute(sql)
            self.__connect.commit()


    @safe_operation
    def get(self, table, select_list='*', condition=None, get_one=False):
        select_list = (',').join(select_list)

        if condition:
            sql = f"select {select_list} from {table} where {condition}"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        else:
            sql = f"select {select_list} from {table}"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        return result

    @safe_operation
    def delete(self, table, condition):
        condition = (' and ').join([f"{k}='{v}'" for k, v in condition.items()])
        sql = f"delete from {table} where {condition}"

        self.__cursor.execute(sql)
        self.__connect.commit()



if __name__ == '__main__':
    m = My_mysql()
#     insert_data = {'ID': 0, 'domain_id': 854214, 'status': 'enable', 'ttl': '600', 'name': 'zvdf.live', 'owner': 'aggamingsa02@gmail.com', 'records': '5'}
#     m.insert('dtest', insert_data)
#     update_data = {'domain_total': 30, 'pause_total': 10}
#     condition = {'ID': 7, 'name': 'a.com'}
#     m.update('dtest', update_data, condition=condition)
    select_list = ['ID', 'domain_id', 'name']
    condition = "domain_id=70160583 and name='zywx99.live'"
    # print(m.get('dtest', select_list, condition=condition))
    print(m.get('dtest', condition=condition))

    # delete_codition = {'ID': 3, 'ttl': 600}
    # m.delete('dtest', delete_codition)


