from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import declarative_base

from database.connection import mysql_db

Base = declarative_base()


# mysql和sqlserver通用类, sqlserver表结构和数据都不允许修改，只能查询数据
class MetaMixin:
    def get_column_name(self) -> list:
        dir_list = self.__dir__()
        return [element for element in dir_list if element[0] != '_' and isinstance(getattr(self, element, None), str)]

    def model_to_dict(self) -> dict:
        column_list = self.get_column_name()
        return {column: getattr(self, column, None) for column in column_list}


# 仅仅只有mysql能使用
class BaseMixin(MetaMixin):
    is_deleted = Column(Boolean, default=False)  # 是否删除
    create_time = Column(DateTime, default=datetime.now)  # 创建日期
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新日期

    # def insert(self, data):
    #     pass
    #
    # def update(self, data):
    #     pass
    #
    # def delete(self):
    #     pass


Base.metadata.create_all(mysql_db.engine)
