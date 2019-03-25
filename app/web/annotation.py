# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:51 PM
# @Author : zbz
import json

from flask import render_template, jsonify, request
from . import web

@web.route('/jl_ai/annotation', methods=['GET', 'POST'])
def annotaion():
    # data={}
    if request.method == 'POST':
        # data = request.data.decode()  # change byte to str
        data = str(request.data, encoding='utf-8')
        print("get post")
        json_data = json.loads(data)  # load str as json
        # print(json.loads(data))
        print(json_data.keys())

    image_urls = {
        "urls": [
            'http://localhost/images/1.jpeg',
            'http://localhost/images/2.png',
            'http://localhost/images/3.png'
        ]
    }
    # image_urls = {
    #     "urls": [
    #         'http://222.128.6.153:8008/images/1.jpeg',
    #         'http://222.128.6.153:8008/images/2.png',
    #         'http://222.128.6.153:8008/images/3.png'
    #     ]
    # }

    image_urls_json = json.dumps((image_urls))
    image_marks = {
        "http://localhost/images/1.jpeg-1": {
            "filename": "http://localhost/images/1.jpeg",
            "size": -1,
            "regions": [
                {
                    "shape_attributes": {"name": "rect", "x": 144, "y": 260, "width": 65, "height": 170},
                    "region_attributes": {"name": "1"}
                },
                {
                    "shape_attributes": {"name": "rect", "x": 223, "y": 259, "width": 39, "height": 184},
                    "region_attributes": {"name": "2"}
                },
                {
                    "shape_attributes": {"name": "rect", "x": 384, "y": 269, "width": 56, "height": 166},
                    "region_attributes": {"name": "3"}
                },
                {
                    "shape_attributes": {"name": "rect", "x": 321, "y": 274, "width": 59, "height": 161},
                    "region_attributes": {"name": "3"}
                },
                {
                    "shape_attributes": {"name": "rect", "x": 275, "y": 259, "width": 48, "height": 181},
                    "region_attributes": {"name": "3"}
                }
            ],
            "file_attributes": {}
        },
        "http://localhost/images/2.png-1": {
            "filename": "http://localhost/images/2.png",
            "size": -1,
            "regions": [
                {
                    "shape_attributes": {"name": "rect", "x": 163, "y": 235, "width": 50, "height": 137},
                    "region_attributes": {"name": "2"}
                },
                {
                    "shape_attributes": {"name": "rect", "x": 327, "y": 231, "width": 72, "height": 141},
                    "region_attributes": {"name": "3"}
                }
            ],
            "file_attributes": {}
        }
    }
    # image_marks = {
    #     "http://222.128.6.153:8008/images/1.jpeg-1": {
    #         "filename": "http://222.128.6.153:8008/images/1.jpeg",
    #         "size": -1,
    #         "regions": [
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 144, "y": 260, "width": 65, "height": 170},
    #                 "region_attributes": {"name": "1"}
    #             },
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 223, "y": 259, "width": 39, "height": 184},
    #                 "region_attributes": {"name": "2"}
    #             },
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 384, "y": 269, "width": 56, "height": 166},
    #                 "region_attributes": {"name": "3"}
    #             },
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 321, "y": 274, "width": 59, "height": 161},
    #                 "region_attributes": {"name": "3"}
    #             },
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 275, "y": 259, "width": 48, "height": 181},
    #                 "region_attributes": {"name": "3"}
    #             }
    #         ],
    #         "file_attributes": {}
    #     },
    #     "http://222.128.6.153:8008/images/2.png-1": {
    #         "filename": "http://222.128.6.153:8008/images/2.png",
    #         "size": -1,
    #         "regions": [
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 163, "y": 235, "width": 50, "height": 137},
    #                 "region_attributes": {"name": "2"}
    #             },
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 327, "y": 231, "width": 72, "height": 141},
    #                 "region_attributes": {"name": "3"}
    #             }
    #         ],
    #         "file_attributes": {}
    #     }
    # }
    image_marks_json = json.dumps(image_marks)
    # print(str)
    return render_template('via_wikimedia_demo.html', image_urls=image_urls_json, image_marks=image_marks_json)

@web.route('/jl_ai/annotations', methods =['GET','POST'] )
def test():
    if request.method == 'POST':
        print("get post")
    return render_template('index.html')