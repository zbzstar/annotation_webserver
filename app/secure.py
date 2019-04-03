# -*- coding:utf-8 -*-
# @Time : 3/19/19 4:11 PM
# @Author : zbz

DEBUG = True

SECRET_KEY = 'zbz'

# 变量名称不可变　 mysql数据库类型　cymysql数据库驱动 root用户名　':'后是密码这里为空　@服务器密码　3306端口号　fisher表名
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:@localhost:3306/ai_annotation'
SQLALCHEMY_TRACK_MODIFICATIONS = False