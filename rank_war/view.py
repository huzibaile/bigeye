from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import update, text

from config import SMTH_FACTION_INFO
from database.connection_back import mysql_session_class, server_session_class
from database.faction_model import RankWarRecord
from tools.base import flatten_dict
from tools.torn_api import TornApi

ta = TornApi()


# 新增rw_recorded
def insert_or_update_rw_recorded(rw_id, operation_type: str = 'update'):
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
        with mysql_session_class() as session:
            if operation_type == 'insert':
                obj = RankWarRecord(**rw_dict)
                session.add(obj)
                session.commit()
            else:
                print(rw_dict)
                session.execute(update(RankWarRecord), [rw_dict])
                session.commit()
                obj = session.query(RankWarRecord).filter(RankWarRecord.id == rw_id).first()
    except Exception as e:
        session.rollback()
        print(e)
        raise e
    return obj


# 构建rw发钱表的数据结构
def construct_rw_report_dict(faction_id, member: list[tuple[str]]):
    dict_attacker = {}
    #  rw结束后构造，存在人员离开的情况，bug处理
    for player in member:
        dict_attacker[player[1]] = {}
        dict_attacker[player[1]]['uid'] = player[0]
        dict_attacker[player[1]]['attacks'] = 0
        dict_attacker[player[1]]['leave'] = 0
        dict_attacker[player[1]]['mug'] = 0
        dict_attacker[player[1]]['hosp'] = 0
        dict_attacker[player[1]]['打野0-500'] = 0
        dict_attacker[player[1]]['打野500-1000'] = 0
        dict_attacker[player[1]]['打野1000-2500'] = 0
        dict_attacker[player[1]]['打野2500+'] = 0
        dict_attacker[player[1]]['assist'] = 0
        dict_attacker[player[1]]['fail'] = 0
        dict_attacker[player[1]]['revive_suc'] = 0
        dict_attacker[player[1]]['revive_fail'] = 0
        dict_attacker[player[1]]['respect_gain'] = 0
        dict_attacker[player[1]]['respect_lose'] = 0
    # 追加所有在帮派成员
    dict_members = ta.get_info('faction', 'basic', faction_id).get('members')
    for player_id in dict_members:
        if player_id not in dict_attacker:
            dict_attacker[dict_members[player_id]["name"]] = {}
            dict_attacker[dict_members[player_id]["name"]]['uid'] = player_id
            dict_attacker[dict_members[player_id]["name"]]['attacks'] = 0
            dict_attacker[dict_members[player_id]["name"]]['leave'] = 0
            dict_attacker[dict_members[player_id]["name"]]['mug'] = 0
            dict_attacker[dict_members[player_id]["name"]]['hosp'] = 0
            dict_attacker[dict_members[player_id]["name"]]['打野0-500'] = 0
            dict_attacker[dict_members[player_id]["name"]]['打野500-1000'] = 0
            dict_attacker[dict_members[player_id]["name"]]['打野1000-2500'] = 0
            dict_attacker[dict_members[player_id]["name"]]['打野2500+'] = 0
            dict_attacker[dict_members[player_id]["name"]]['assist'] = 0
            dict_attacker[dict_members[player_id]["name"]]['fail'] = 0
            dict_attacker[dict_members[player_id]["name"]]['revive_suc'] = 0
            dict_attacker[dict_members[player_id]["name"]]['revive_fail'] = 0
            dict_attacker[dict_members[player_id]["name"]]['respect_gain'] = 0
            dict_attacker[dict_members[player_id]["name"]]['respect_lose'] = 0
    return dict_attacker


# rw策略处理

# 获取周能量
def get_weekly_energy(start_time: int, faction_id: int) -> dict:
    rw_start_date = datetime.fromtimestamp(start_time)
    end_date = rw_start_date + timedelta(days=6 - rw_start_date.weekday())
    end_date = min(end_date, datetime.now())
    start_date = end_date - timedelta(days=28)
    sDate = start_date.strftime('%Y%m%d')
    eDate = end_date.strftime('%Y%m%d')
    with server_session_class() as session:
        stmt = text('EXEC TornBingWaFunction :Type, :sDate, :eDate, :Faction_ID')
        energy_data = session.execute(stmt,
                                      {'Type': '能量', 'sDate': sDate, 'eDate': eDate,
                                       'Faction_ID': faction_id}).fetchall()
    print('-------------------------------------------------------------')
    print(energy_data)
    return dict()


def get_day_in_faction(faction_id: int, player_id: int = None) -> dict:
    data = ta.get_info('faction', '', faction_id)
    if not isinstance(data, dict):
        return data
    members = data.get('members', None)
    day_in_faction = {}
    if player_id is None:
        pass

    return day_in_faction
