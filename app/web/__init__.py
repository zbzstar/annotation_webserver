# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:52 PM
# @Author : zbz

from flask import Blueprint
from flask import render_template

web = Blueprint('web', __name__)  # __name__ 指明蓝图所在包

from app.web import annotation
from app.web import auth