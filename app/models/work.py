# -*- coding:utf-8 -*-
# @Time : 4/2/19 3:05 PM
# @Author : zbz
from sqlalchemy import Column, Integer, ForeignKey, String, desc
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.image import Image
from app.models.user import User


class Work(Base):
    id = Column(Integer, primary_key=True)
    user = relationship(User)
    uid = Column(Integer, ForeignKey('user.id'))
    # image = relationship(Image)
    img_path = Column(String(200), nullable=True)

    @classmethod
    def get_user_work(cls, uid):
        works = Work.query.filter_by(uid=uid).orber_by(
            desc(Work.create_time)).all()
        return works
