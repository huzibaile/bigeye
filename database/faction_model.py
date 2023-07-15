from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Column, Integer, String, BigInteger, update, text, and_, or_

from config import SMTH_FACTION_INFO
from database.connection import mysql_db
from database.enhance import BaseMixin, Base
from database.sqlserver_model import BattleLog
from tools.base import flatten_dict
from tools.torn_api import TornApi

ta = TornApi()


class Faction(Base, BaseMixin):
    __tablename__ = 'faction'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), nullable=False)
    qq_group_num = Column(String(50), nullable=False)

    # 构建rw发钱表的数据结构
    def construct_rw_report(self, attack_member: list) -> dict:
        """
        :param attack_member: 存放玩家名称的列表
        :return: 
        """
        members_dict = self.get_member_info()
        # 初始化报告字典，将所有帮派成员信息加入字典
        rw_report = {members_dict[player_id]['name']: {
            'uid': player_id,
            'attacks': 0,
            'leave': 0,
            'mug': 0,
            'hosp': 0,
            '打野0-500': 0,
            '打野500-1000': 0,
            '打野1000-2500': 0,
            '打野2500+': 0,
            'assist': 0,
            'fail': 0,
            'revive_suc': 0,
            'revive_fail': 0,
            'respect_gain': 0,
            'respect_lose': 0
        } for player_id in members_dict}
        # 更新字典，添加参赛玩家的信息
        for player in attack_member:
            player_name = player[1]
            if player_name not in rw_report:
                rw_report[player_name] = {
                    'uid': player[0],
                    'attacks': 0,
                    'leave': 0,
                    'mug': 0,
                    'hosp': 0,
                    '打野0-500': 0,
                    '打野500-1000': 0,
                    '打野1000-2500': 0,
                    '打野2500+': 0,
                    'assist': 0,
                    'fail': 0,
                    'revive_suc': 0,
                    'revive_fail': 0,
                    'respect_gain': 0,
                    'respect_lose': 0
                }
            rw_report[player_name]['attacks'] += 1

        return rw_report

    # 获取攻击信息
    def get_attack_info(self, start_time: int, end_time: int) -> dict:
        """
        :param start_time: 时间戳，设置要查询的时间范围
        :param end_time: 时间戳，设置要查询的时间范围
        :return:
        """
        # 获取rw期间attack相关信息
        filter_condition_1 = and_(BattleLog.timestamp_ended >= start_time, BattleLog.timestamp_ended <= end_time)
        filter_condition_2 = or_(BattleLog.attacker_faction == self.id, BattleLog.defender_faction == self.id)
        with mysql_db.session as session:
            attack_rows = session.query(BattleLog).filter(filter_condition_1).filter(filter_condition_2)
            attack_logs = attack_rows.all()
            member = attack_rows.filter(BattleLog.attacker_faction == self.id).group_by(BattleLog.attacker_id,
                                                                                        BattleLog.attacker_name).with_entities(
                BattleLog.attacker_id, BattleLog.attacker_name).all()
        return {'member': member, 'attack_logs': attack_logs}

    # 获取当前帮派成员信息
    def get_member_info(self):
        members_dict = ta.get_info('faction', 'basic', self.id).get('members')
        return members_dict

    # 获取周能量
    def get_weekly_energy(self, start_time: int) -> dict:
        rw_start_date = datetime.fromtimestamp(start_time)
        end_date = rw_start_date + timedelta(days=6 - rw_start_date.weekday())
        end_date = min(end_date, datetime.now())
        start_date = end_date - timedelta(days=28)
        sDate = start_date.strftime('%Y%m%d')
        eDate = end_date.strftime('%Y%m%d')
        with mysql_db.session as session:
            stmt = text('EXEC TornBingWaFunction :Type, :sDate, :eDate, :Faction_ID')
            energy_data = session.execute(stmt,
                                          {'Type': '能量', 'sDate': sDate, 'eDate': eDate,
                                           'Faction_ID': self.id}).fetchall()
        print(energy_data)
        return dict()

    def get_day_in_faction(self, player_id: int = None) -> dict:
        # 判断
        # todo 目前直接从api获取， 或许数据存在本地，每天更新一次
        data = ta.get_info('faction', '', self.id)
        if not isinstance(data, dict):
            return data
        members: dict = data.get('members', None)
        day_in_faction = {}
        # todo 业务逻辑待完善
        if player_id is None:
            pass
        return day_in_faction


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

    # 新增或更新rw记录
    @classmethod
    def insert_or_update(cls, rw_id, operation_type: str = 'update'):
        if operation_type not in ('update', 'insert'):
            return f'operation_typec：{operation_type}错误，只能是update或insert'
        data = ta.get_info('torn', 'rankedwarreport', rw_id)
        if not isinstance(data, dict):
            return data
        report = data.get('rankedwarreport')
        # 没有获取到正确数据
        if report is None:
            return data
        # 构造需要存入表中的数据
        try:
            rw_dict: dict[str, str | int | Any] = {
                'id': rw_id,
                'start_time': report.get('war').get('start'),
                'end_time': report.get('war').get('end'),
                'winner': report.get('war').get('winner'),
            }
            for key, value in report.get('factions').items():
                # 压扁字典
                reward_dict = flatten_dict(value)
                if key in SMTH_FACTION_INFO:
                    # 我方rw信息
                    rw_dict.update({
                        'faction_id': key,
                        'faction_name': reward_dict.get('name', ''),
                        'score': reward_dict.get('score', 0),
                        'respect': reward_dict.get('rewards_respect', 0),
                        'points': reward_dict.get('rewards_points', 0),
                        'armor_cache': reward_dict.get('rewards_items_1118_quantity', 0),
                        'melee_cache': reward_dict.get('rewards_items_1119_quantity', 0),
                        'small_cache': reward_dict.get('rewards_items_1120_quantity', 0),
                        'medium_arms_cache': reward_dict.get('rewards_items_1121_quantity', 0),
                        'heavy_armor_cache': reward_dict.get('rewards_items_1122_quantity', 0)
                    })
                else:
                    # 对方rw信息
                    rw_dict.update({
                        'enemy_faction_id': key,
                        'enemy_faction_name': reward_dict.get('name', ''),
                        'enemy_score': reward_dict.get('score', 0),
                        'enemy_respect': reward_dict.get('rewards_respect', 0),
                        'enemy_points': reward_dict.get('rewards_points', 0),
                        'enemy_armor_cache': reward_dict.get('rewards_items_1118_quantity', 0),
                        'enemy_melee_cache': reward_dict.get('rewards_items_1119_quantity', 0),
                        'enemy_small_cache': reward_dict.get('rewards_items_1120_quantity', 0),
                        'enemy_medium_arms_cache': reward_dict.get('rewards_items_1121_quantity', 0),
                        'enemy_heavy_armor_cache': reward_dict.get('rewards_items_1122_quantity', 0)
                    })
        except Exception as e:
            print(e)
            return e
        try:
            with mysql_db.session as session:
                if operation_type == 'insert':
                    obj = RankWarRecord(**rw_dict)
                    session.add(obj)
                    session.commit()
                else:
                    print(rw_dict)
                    session.execute(update(cls), [rw_dict])
                    session.commit()
                    obj = session.query(cls).filter(cls.id == rw_id).first()
        except Exception as e:
            session.rollback()
            print(e)
            raise e
        return obj


class RankWarStrategy(Base, BaseMixin):
    pass
