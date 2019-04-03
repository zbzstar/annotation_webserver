# -*- coding:utf-8 -*-
# @Time : 4/2/19 3:04 PM
# @Author : zbz
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Image(Base):
    id = Column(Integer, primary_key=True)
    img_name = Column(String(200), nullable=False)
    img_path = Column(String(200), nullable=True)
    tag = Column(String(50), nullable=True)
    anno_string = Column(String(200), nullable=True)
    # 矩形 rect;圆 circle；椭圆 ellipse; 点 point; 折线 polyline;多边封闭空间 polygon
    anno_type = Column(String(20), nullable=True)

