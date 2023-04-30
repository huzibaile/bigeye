from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MetaMixin:
    def get_column_name(self):
        dir_list = self.__dir__()
        return [element for element in dir_list if element[0] != '_' and isinstance(getattr(self, element, None), str)]

    def model_to_dict(self):
        column_list = self.get_column_name()
        return {column: getattr(self, column, None) for column in column_list}


class BaseMixin(MetaMixin):
    is_deleted = Column(Boolean, default=False)  # 是否删除
    create_time = Column(DateTime, default=datetime.now)  # 创建日期
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新日期
