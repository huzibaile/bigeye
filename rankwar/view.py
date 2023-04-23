from fastapi import APIRouter

from sqlalchemy.orm import Session

from database.connection import get_server_engine
from database.sqlserver_model import BattleLog

rw_report = APIRouter()


@rw_report.get("/attackLog")
async def get_attack_log():
    with Session(get_server_engine) as session:
        data = await session.query(BattleLog).first()
    return data


@rw_report.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
