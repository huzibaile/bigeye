from sqlalchemy import Column, Integer, String

from database.enhance import Base, BaseMixin


class User(Base, BaseMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=False)
    torn_id = Column(Integer, nullable=False)
    torn_name = Column(String(50), nullable=False)
    torn_key = Column(String(36))
