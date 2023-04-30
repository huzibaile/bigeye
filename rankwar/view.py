from sqlalchemy import update

from config import SMTH_FACTION_INFO
from database.connection import mysql_session_class
from rankwar.model import RankWarRecord
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
        rw_dict = {
            'id': rw_id,
            'start_time': report.get('war').get('start'),
            'end_time': report.get('war').get('end'),
            'winner': report.get('war').get('winner'),
        }
        for key, value in report.get('factions').items():
            # 压扁字典
            reaward_dict = flatten_dict(value)
            if key in SMTH_FACTION_INFO:
                # 我方rw信息
                rw_dict.update({
                    'faction_id': key,
                    'faction_name': reaward_dict.get('name', ''),
                    'score': reaward_dict.get('score', 0),
                    'respect': reaward_dict.get('rewards_respect', 0),
                    'points': reaward_dict.get('rewards_points', 0),
                    'armor_cache': reaward_dict.get('rewards_items_1118_quantity', 0),
                    'melee_cache': reaward_dict.get('rewards_items_1119_quantity', 0),
                    'small_cache': reaward_dict.get('rewards_items_1120_quantity', 0),
                    'medium_arms_cache': reaward_dict.get('rewards_items_1121_quantity', 0),
                    'heavy_armor_cache': reaward_dict.get('rewards_items_1122_quantity', 0)
                })
            else:
                # 对方rw信息
                rw_dict.update({
                    'enemy_faction_id': key,
                    'enemy_faction_name': reaward_dict.get('name', ''),
                    'enemy_score': reaward_dict.get('score', 0),
                    'enemy_respect': reaward_dict.get('rewards_respect', 0),
                    'enemy_points': reaward_dict.get('rewards_points', 0),
                    'enemy_armor_cache': reaward_dict.get('rewards_items_1118_quantity', 0),
                    'enemy_melee_cache': reaward_dict.get('rewards_items_1119_quantity', 0),
                    'enemy_small_cache': reaward_dict.get('rewards_items_1120_quantity', 0),
                    'enemy_medium_arms_cache': reaward_dict.get('rewards_items_1121_quantity', 0),
                    'enemy_heavy_armor_cache': reaward_dict.get('rewards_items_1122_quantity', 0)
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
def construct_rw_report_dict(faction_id):
    dict_members = ta.get_info('faction', 'basic', faction_id).get('members')
    # todo rw结束后构造，存在人员离开的情况，会产生bug
    dict_attacker = {}
    dict_id_name = {}
    for player_id in dict_members:
        dict_id_name[dict_members[player_id]["name"]] = player_id
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
    return [dict_id_name, dict_attacker]

# rw策略处理
