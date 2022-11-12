#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

mssql = {'host': 'dbhost',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}

postgresql = {'host': '0.0.0.0',
         'user': 'postgres',
         'passwd': 'magical_password',
         'db': 'db'}


mssqlConfig = 'mysql+pymysql://root:localMysql.87@localhost/livestock'
postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])

