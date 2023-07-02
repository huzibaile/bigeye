from sqlalchemy import Column, Integer, String, BigInteger

from database.enhance import BaseMixin, Base


class Faction(Base, BaseMixin):
    pass


class RankWarRecord(Base, BaseMixin):
    __tablename__ = 'rw_records'
    id = Column(Integer, primary_key=True, autoincrement=False)
    faction_id = Column(Integer, nullable=False)
    faction_name = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False, default=0)
    respect = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)
    armor_cache = Column(Integer, nullable=False, default=0)
    melee_cache = Column(Integer, nullable=False, default=0)
    small_cache = Column(Integer, nullable=False, default=0)
    medium_arms_cache = Column(Integer, nullable=False, default=0)
    heavy_armor_cache = Column(Integer, nullable=False, default=0)
    enemy_faction_id = Column(Integer, nullable=False)
    enemy_faction_name = Column(String(50), nullable=False)
    enemy_score = Column(Integer, nullable=False, default=0)
    enemy_respect = Column(Integer, nullable=False, default=0)
    enemy_points = Column(Integer, nullable=False, default=0)
    enemy_armor_cache = Column(Integer, nullable=False, default=0)
    enemy_melee_cache = Column(Integer, nullable=False, default=0)
    enemy_small_cache = Column(Integer, nullable=False, default=0)
    enemy_medium_arms_cache = Column(Integer, nullable=False, default=0)
    enemy_heavy_armor_cache = Column(Integer, nullable=False, default=0)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger)
    winner = Column(Integer, nullable=False)


class RankWarStrategy(Base, BaseMixin):
    pass
