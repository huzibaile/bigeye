from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SERVER, DATABASE_NAME, SERVER_USERNAME, SERVER_PASSWORD, MYSQL_USER, MYSQL_PWD, MYSQL_URL, \
    MYSQL_DB_NAME


class MySQLDatabase:
    def __init__(self, user, password, host, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name
        self.engine_url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8"
        self.engine = self._create_engine()
        self.Session = self._create_session()

    def _create_engine(self):
        engine = create_engine(self.engine_url,
                               echo=True,
                               future=True,
                               pool_size=5,
                               pool_recycle=3600)
        return engine

    def _create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session

    @property
    def session(self):
        return self.Session()


class SQLServerDatabase:
    def __init__(self, server, user, password, db_name):
        self.server = server
        self.user = user
        self.password = password
        self.db_name = db_name
        self.engine_url = f'mssql+pymssql://{user}:{password}@{server}/{db_name}?charset=utf8'
        self.engine = self._create_engine()
        self.Session = self._create_session()

    def _create_engine(self):
        db_host = ':'.join(self.server.split(','))
        engine = create_engine(self.engine_url,
                               echo=True,
                               future=True,
                               pool_size=5,
                               pool_recycle=3600)
        return engine

    def _create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session

    @property
    def session(self):
        return self.Session()


mysql_db = MySQLDatabase(MYSQL_USER, MYSQL_PWD, MYSQL_URL, MYSQL_DB_NAME)
server_db = SQLServerDatabase(SERVER, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
