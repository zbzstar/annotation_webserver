# -*- coding:utf-8 -*-
# @Time : 3/19/19 3:51 PM
# @Author : zbz
from datetime import datetime
import json

import requests
from flask import render_template, jsonify, request, current_app
from flask_login import login_required,current_user

from annotation import log
from app import db
from app.models.image import Image
from app.models.work import Work
from app.models.user import User
from . import web
import numpy as np

# from flask.ext.login import current_user


raw_region_id = []
# nick_name = ''
contral = {}
# contral['nickname'] = ''
@web.route('/annotation', methods=['GET', 'POST'])
@login_required
def annotation():
    if request.method == 'POST':
        data = str(request.data, encoding='utf-8')
        log.logger.debug('get post')
        json_data = json.loads(data)  # load str as json
        curve_flag = False
        if json_data['type'] == 'curve':
            curve_flag = True
        for key in json_data:
            if key == "type":
                continue
            filename = json_data[key]['filename'].split('/')
            for anno in json_data[key]['regions']:
                if anno['id'] == 0:  # add new region

                    # get curve points
                    if anno['shape_attributes']['name'] == 'rect' and curve_flag:
                        region = []
                        region.append(anno['shape_attributes']['x'])
                        region.append(anno['shape_attributes']['y'])
                        region.append(anno['shape_attributes']['width'])
                        region.append(anno['shape_attributes']['height'])
                        img_path = json_data[key]['filename']

                        r = get_curve_points(img_path, region)
                        poly = np.array(r['poly'])
                        poly = np.trunc(poly).astype(np.int16)
                        curve_string = {
                            'name': 'polygon',
                            'all_points_x': poly[:, 0].tolist(),
                            'all_points_y': poly[:, 1].tolist(),
                        }
                        # save curve points 只保存新获取curve points,不保存矩形框
                        with db.auto_commit():
                            image = Image()
                            image.img_name = filename[-1]
                            image.img_path = str('/'.join(filename[3:]))
                            image.anno_type = 'polygon'
                            image.anno_string = str(curve_string).replace(' ', '')
                            if anno['region_attributes']:
                                image.tag = anno['region_attributes']['name']
                            else:
                                image.tag = "Default"
                            db.session.add(image)
                    else:
                        with db.auto_commit():
                            image = Image()
                            image.img_name = filename[-1]
                            image.img_path = str('/'.join(filename[3:]))
                            image.anno_string = str(anno['shape_attributes'])
                            image.anno_type = anno['shape_attributes']['name']
                            # keys = anno['region_attributes'].keys
                            # for tmp_key in  anno['region_attributes']:
                            if anno['region_attributes']:
                                image.tag = anno['region_attributes']['name']
                            else:
                                image.tag = "Default"
                            db.session.add(image)
                else:
                    if anno['id'] in raw_region_id:
                        raw_region_id.remove(anno['id'])   # 有返回，未被删除
                        with db.auto_commit():
                            image = Image.query.get_or_404(anno['id'])
                            image.anno_string = str(anno['shape_attributes'])
                            image.anno_type = anno['shape_attributes']['name']
                            image.tag = anno['region_attributes']['name']
                            image.update_time = int(datetime.now().timestamp())
                    else:
                        # print("error... 有多次提交 复制导致错误")
                        log.logger.error('收到携带非法id的提交')
                        log.logger.error(anno['id'])

        if raw_region_id:  # 有标记被删除
            for r_id in raw_region_id:
                raw_region_id.remove(r_id)
                with db.auto_commit():
                    image = Image.query.get_or_404(r_id)
                    image.status = 0
                    image.update_time = int(datetime.now().timestamp())

    uid = current_user.id
    image_pathes = db.session.query(Work.img_path).filter_by(uid=uid).all()

    image_server = current_app.config['IMAGE_SERVER']

    image_urls = {}
    image_marks = {}
    tmp_url = []
    region_shapes = db.session.query(
        Work.anno_type).filter_by(
        uid=uid).distinct().all()
    for path in image_pathes:
        # get image_urls info
        url = image_server + path[0]
        tmp_url.append(url)

        # get image_marks info
        mask_key = url + "-1"
        mark_info = {}
        mark_info['filename'] = url
        mark_info['size'] = -1
        mark_info['file_attributes'] = {}
        mark_info['regions'] = []
        for shape in region_shapes:
            anno_strings = db.session.query(
                                Image.anno_string, Image.tag, Image.id).filter_by(
                                img_path=path[0], anno_type=shape[0], status=1).all()
            # 拼接标记字典
            for anno in anno_strings:
                anno_info={}
                anno_info['shape_attributes'] = eval(anno[0])
                anno_info['region_attributes'] = {"name": anno[1]}
                anno_info['id'] = anno[2]
                mark_info['regions'].append(anno_info)
                if not anno[2] in raw_region_id:
                    raw_region_id.append(anno[2])  # 保存任务id
            image_marks[mask_key] = mark_info

    image_urls['urls'] = tmp_url

    # image_marks = {
    #     "http://localhost/images/1.jpeg-1": {
    #         "filename": "http://localhost/images/1.jpeg",
    #         "size": -1,
    #         "regions": [
    #             {
    #                 "shape_attributes": {"name": "rect", "x": 144, "y": 260, "width": 65, "height": 170},
    #                 "region_attributes": {"name": "1"},
    #                 "id": "123456"
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
    #     }


    contral['image_urls'] = image_urls
    contral['image_marks'] = image_marks
    contral['region_shape'] = []
    # region_shapes = db.session.query(
    #                     Work.anno_type).filter_by(
    #                     uid=uid).distinct().all()
    for shape in region_shapes:
        contral['region_shape'].append(shape[0])

    # if not contral['nickname']:
    contral['nickname'] = db.session.query(User.nickname).filter_by(id=uid).first()[0]

    contral_json = json.dumps(contral)
    # image_urls_json = json.dumps(image_urls)
    image_marks_json = json.dumps(image_marks)

    # 将最新结果返回
    if request.method == 'POST':
        return image_marks_json
    return render_template('via_wikimedia_demo.html',
                           image_marks=image_marks_json,  # 前端函数内做的JSON.parse,保留
                           contral=contral_json,
                           nickname=contral['nickname'])


# @login_required
@web.route('/add', methods=['GET', 'POST'])
def test():
    # if request.method == 'POST':
    print("add work for current user")
    tmp_add_work()
    return render_template('via_demo.html')


def tmp_add_work():
    uid = current_user.id
    img_pathes = get_all_img_path()
    # for path in img_pathes:
    with db.auto_commit():
        work = Work()
        work.uid = uid
        work.img_path = 'images/1.jpeg'
        work.anno_type = 'circle'
        db.session.add(work)


def get_all_img_path():
    img_pathes = db.session.query(Image.img_path).distinct().all()  #distinct() 去重
    print("image_pathes:", img_pathes)
    return img_pathes


def get_curve_points(img_path, region):
    curve_point_curl = current_app.config['CURVE_CURL']
    d = {
        'img_path': img_path,
        'region': {
            'bbox': region
        }
    }
    r = requests.post(curve_point_curl, data=json.dumps(d))
    return json.loads(r.text)
