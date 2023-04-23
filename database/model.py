from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseMixin:
    is_deleted = Column(Boolean, default=False)  # 是否删除
    create_time = Column(DateTime, default=datetime.now)  # 创建日期
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新日期
