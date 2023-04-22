import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import DRIVER, SERVER, DATABASE_NAME, SERVER_USERNAME, SERVER_PASSWORD, MYSQL_USER, MYSQL_PWD, MYSQL_URL, \
    MYSQL_DB_NAME

# mysql配置信息
mysql_engine_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_URL}/{MYSQL_DB_NAME}"
# sqlserver配置信息
db_host = ':'.join(SERVER.split(','))
server_engine_url = f'mssql+pymssql://{SERVER_USERNAME}:{SERVER_PASSWORD}@{db_host}/{DATABASE_NAME}?charset=utf8'


def get_sql_server_data(sql: str):
    sql_server_url = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE_NAME};UID={SERVER_USERNAME};PWD={SERVER_PASSWORD};ENCRYPT=yes;TrustServercertificate=yes; '
    with pyodbc.connect(sql_server_url) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows


def sql_server_data_to_list(sql: str):
    engine = create_engine(server_engine_url,
                           encoding='utf-8',
                           echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
                           future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
                           pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
                           pool_recycle=3600,  # 设置时间以限制数据库自动断开
                           )
    with engine.connect() as connection:
        result = connection.execute(text(sql))
        result_list = [temp for temp in result.mappings()]
    return result_list


# 创建数据库会话
def create_mysql_session(engine_url: str = mysql_engine_url):
    engine = create_engine(engine_url,
                           encoding='utf-8',
                           echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
                           future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
                           pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
                           pool_recycle=3600,  # 设置时间以限制数据库自动断开
                           )
    Session = sessionmaker(engine)
    return Session
