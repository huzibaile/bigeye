from datetime import datetime

from fastapi import APIRouter, status
from sqlalchemy import and_, or_

from config import RW_STRATEGY
from database.connection_back import mysql_session_class, server_session_class
from database.faction_model import RankWarRecord
from database.sqlserver_model import BattleLog
from rank_war.view import construct_rw_report_dict, insert_or_update_rw_recorded, get_weekly_energy
from tools.base import customized_rounding
from tools.torn_api import TornApi

rw_report = APIRouter()

ta = TornApi()


@rw_report.get("/rwRecord")
def get_rw_report(rw_id: int):
    # 1.根据获取rw相关信息,数据库中没有就从api获取并存入数据库
    with mysql_session_class() as session:
        rw_info = session.query(RankWarRecord).filter(RankWarRecord.id == rw_id).first()
        if rw_info is None:
            # 5364 5664
            # todo 检查RW编号是否包含SMTH的帮派
            rw_info = insert_or_update_rw_recorded(rw_id, 'insert')
            # 更新数据出现错误
            if not isinstance(rw_info, dict):
                print(rw_info)
                # raise rw_info
                return {'status_code ': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error': rw_info}
            # 未查到数据
            if rw_info.get('id') is None:
                return {'status_code ': status.HTTP_404_NOT_FOUND, 'error': rw_info}
            # 数据查询错误,需要看看啥原因,讲道理不会出现这种情况
            if rw_info.get('id') != rw_id:
                return {'status_code': status.HTTP_404_NOT_FOUND, 'error': rw_info}
        else:
            # 更新rw_report数据
            insert_or_update_rw_recorded(rw_id)
    # 2. 获取攻击日志
    # 构造查询条件
    faction_id = rw_info.faction_id
    start_time = int(rw_info.start_time)
    end_time = rw_info.end_time or int(datetime.now().timestamp())
    filter_condition_1 = and_(BattleLog.timestamp_ended >= start_time, BattleLog.timestamp_ended <= end_time)
    filter_condition_2 = or_(BattleLog.attacker_faction == faction_id, BattleLog.defender_faction == faction_id)
    with server_session_class() as session:
        attack_rows = session.query(BattleLog).filter(filter_condition_1).filter(filter_condition_2)
        attack_logs = attack_rows.all()
        member = attack_rows.filter(BattleLog.attacker_faction == faction_id).group_by(BattleLog.attacker_id,
                                                                                       BattleLog.attacker_name).with_entities(
            BattleLog.attacker_id, BattleLog.attacker_name).all()
    # 3.构造rw发钱表数据结构
    rw_report_dict = construct_rw_report_dict(faction_id, member)

    # 4.根据日志计算枪数及分数
    # 5364 5664
    enemy_faction_id = rw_info.enemy_faction_id
    attack_rule = RW_STRATEGY.get('attack_enemy')
    daye_rule = RW_STRATEGY.get('attack_others')
    bonus_dict = RW_STRATEGY.get('bonus')
    revive_rule = RW_STRATEGY.get('revive')
    for attack_log in attack_logs:
        result = attack_log.result
        attacker_faction = int(
            attack_log.attacker_faction) if attack_log.attacker_faction != '' else attack_log.attacker_faction
        attacker_name = attack_log.attacker_name
        defender_faction = int(
            attack_log.defender_faction) if attack_log.defender_faction != '' else attack_log.defender_faction
        defender_name = attack_log.defender_name
        chain_num = attack_log.chain
        # 4.1复活 自己人复活自己人
        if result == 'revive' and attacker_faction == faction_id and defender_faction == faction_id:
            if attacker_name not in rw_report_dict or defender_name not in rw_report_dict:
                print(f'revive,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
                continue
            if attack_log.respect_gain:  # 复活成功
                rw_report_dict[attacker_name][revive_rule.get('suc_tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += revive_rule.get(result).get('suc_coefficient')
                continue
            else:  # 复活失败
                rw_report_dict[attacker_name][revive_rule.get('fail_tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += revive_rule.get(result).get('fail_coefficient')
                continue
        # 4.2被对面攻击
        if defender_faction == faction_id and attacker_faction in [enemy_faction_id, '']:
            # 计算失分
            if defender_name in rw_report_dict:
                rw_report_dict[defender_name]['respect_lose'] += attack_log.respect_gain
            else:
                print(f'be_attacked,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
            continue
        # 4.3打中bonus
        if chain_num in bonus_dict and attacker_faction == faction_id:
            if attacker_name not in rw_report_dict:
                print(f'打中bonus,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
                continue
            # 判断是否增加chain
            if result in ['Arrested', 'Attacked', 'Hospitalized', 'Mugged', 'Special']:
                # 判断是否打歪
                if chain_num >= bonus_dict.get('error_criteria') and defender_faction != enemy_faction_id:  # 打歪
                    # 打歪属于打野,这里只扣分,其他逻辑在打野处理
                    rw_report_dict.get(attacker_name)['respect_gain'] -= bonus_dict.get(chain_num)
                else:  # 打中
                    rw_report_dict.get(attacker_name)['respect_gain'] += 10
                    rw_report_dict.get(attacker_name)[attack_rule.get(result).get('tag')] += 1
                    rw_report_dict[attacker_name]['attacks'] += attack_rule.get(result).get('coefficient')
                    continue
        # 4.4打野 攻击帮派是自己 防御帮派不是对方
        if defender_faction != enemy_faction_id and attacker_faction == faction_id:
            if attacker_name not in rw_report_dict:
                print(f'daye,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
                continue
            # 打野失败
            if attack_rule.get(result).get('tag') == 'fail':
                # todo 确认打野失败是否计算枪数
                rw_report_dict.get(attacker_name)[attack_rule.get(result).get('tag')] += 1
                # rw_report_dict[attacker_name]['attacks'] += attack_rule.get(result).get('coefficient')
                continue
            if chain_num <= 500:
                rw_report_dict.get(attacker_name)[daye_rule.get(1).get('tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += daye_rule.get(1).get('coefficient')
            elif chain_num <= 1000:
                rw_report_dict.get(attacker_name)[daye_rule.get(2).get('tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += daye_rule.get(2).get('coefficient')
            elif chain_num <= 2500:
                rw_report_dict.get(attacker_name)[daye_rule.get(3).get('tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += daye_rule.get(3).get('coefficient')
            else:
                rw_report_dict.get(attacker_name)[daye_rule.get(4).get('tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += daye_rule.get(4).get('coefficient')
            continue
        # 4.5正常攻击
        if attacker_faction == faction_id and defender_faction == enemy_faction_id:
            if result not in attack_rule:
                print(f'normal,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
            try:
                # 计算等效枪数
                rw_report_dict.get(attacker_name)[attack_rule.get(result).get('tag')] += 1
                rw_report_dict[attacker_name]['attacks'] += attack_rule.get(result).get('coefficient')
                # 计算分数
                rw_report_dict.get(attacker_name)['respect_gain'] += attack_log.respect_gain
            except Exception as e:
                print(f'normal,有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
                raise e
            continue

        print(f'data_not_processed,可能有bug需要查找, 问题数据：{attack_log.model_to_dict()}')
    # 5.按照获得分数对数据进行排序
    rw_report_dict_sort = dict(sorted(rw_report_dict.items(), key=lambda d: (d[1]['respect_gain']), reverse=True))
    # 5.1 获取上周能量
    energy_data = get_weekly_energy(start_time, faction_id)

    # 对数进行加工
    rank_id = 1
    for key, value in rw_report_dict_sort.items():
        value['rank_id'] = rank_id
        rank_id += 1
        value['attacks'] = customized_rounding(value.get('attacks'))
        value['respect_gain'] = customized_rounding(value.get('respect_gain'))
        value['respect_lose'] = customized_rounding(value.get('respect_lose'))
    return {'msg': 'ok', 'data': rw_report_dict_sort}


@rw_report.get("/rwRecord")
async def get_rw_record():
    with mysql_session_class() as session:
        data = session.query(RankWarRecord).all()
    return data
