import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

# 读取数据库配置
config = configparser.ConfigParser()
config.read('configuration/database_config.ini')
db_config = config['database']

# 构建数据库连接字符串
DATABASE_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# 创建数据库引擎
#engine = create_engine(DATABASE_URL, convert_unicode=True, pool_size=10, max_overflow=20, pool_timeout=30, echo=True)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    pool_recycle=1600,  # 假设数据库超时时间大于1600秒
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo_pool=True,
    max_overflow=5
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 定义一个装饰器来处理数据库会话
def db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = None
        try:
            session = SessionLocal()
            result = func(session,*args, **kwargs)
            return result
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            raise e
        finally:
            if session:
                session.close()
    return wrapper