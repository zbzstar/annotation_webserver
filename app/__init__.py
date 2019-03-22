# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:44 PM
# @Author : zbz

from flask import Flask

def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    return app

def register_blueprint(app):
    from app.web.annotation import web
    app.register_blueprint(web)