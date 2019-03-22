# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:40 PM
# @Author : zbz

from app import creat_app
import sys
sys.path.append('/home/zbz/tmp/jl_annotation/app')

app = creat_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'],
            port=5200, threaded=True)