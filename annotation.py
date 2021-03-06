# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:40 PM
# @Author : zbz

from app import create_app
import sys

from app.tools.log import Logger

sys.path.append('/home/zbz/tmp/jl_annotation/app')

app = create_app()
log = Logger('./logs/jl_annotation.log', level='debug')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'],
            port=5200, threaded=True)
