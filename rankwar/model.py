from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database.model import BaseMixin, Base


class RankWarRecord(Base, BaseMixin):
    __tablename__ = 'rw_records'
    id = Column(Integer, primary_key=True)
    faction_id = Column(Integer, nullable=False)
    faction_name = Column(String(50), nullable=False)
    enemy_faction_id = Column(Integer, nullable=False)
    enemy_faction_name = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    is_ended = Column(Boolean, default=False)

# Base.metadata.create_all(get_mysql_engine())
