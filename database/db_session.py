import configparser
from sqlalchemy import create_engine, scoped_session
from sqlalchemy.orm import sessionmaker

# 读取数据库配置
config = configparser.ConfigParser()
config.read('../configuration/database.ini')
db_config = config['database']

# 构建数据库连接字符串
DATABASE_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, convert_unicode=True, pool_size=10, max_overflow=20, pool_timeout=30)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建全局会话
session = scoped_session(SessionLocal)

class DatabaseSession:
    def __init__(self):
        self._session = session()

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()

# 用于在程序中获取数据库会话的全局函数
def get_db_session():
    return DatabaseSession()