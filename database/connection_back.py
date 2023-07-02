from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SERVER, DATABASE_NAME, SERVER_USERNAME, SERVER_PASSWORD, MYSQL_USER, MYSQL_PWD, MYSQL_URL, \
    MYSQL_DB_NAME

# mysql配置信息
mysql_engine_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_URL}/{MYSQL_DB_NAME}?charset=utf8"
# sqlserver配置信息
db_host = ':'.join(SERVER.split(','))
server_engine_url = f'mssql+pymssql://{SERVER_USERNAME}:{SERVER_PASSWORD}@{db_host}/{DATABASE_NAME}?charset=utf8'


# 创建数据库会话
def get_server_engine(engine_url: str = server_engine_url):
    engine = create_engine(engine_url,
                           echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
                           future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
                           pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
                           pool_recycle=3600,  # 设置时间以限制数据库自动断开
                           )
    return engine


def get_mysql_engine(engine_url: str = mysql_engine_url):
    engine = create_engine(engine_url,
                           echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
                           future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
                           pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
                           pool_recycle=3600,  # 设置时间以限制数据库自动断开
                           )
    return engine


def get_mysql_session_class():
    Session = sessionmaker(get_mysql_engine())
    return Session


def get_server_session_class():
    Session = sessionmaker(get_server_engine())
    return Session


server_session_class = sessionmaker(get_server_engine())
mysql_session_class = sessionmaker(get_mysql_engine())
