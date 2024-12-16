import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from easyrpa.tools.logs_tool import log_db_error
from easyrpa.tools import request_tool 
from datetime import datetime

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
    pool_size=50,  # 增加连接池大小
    pool_timeout=30,  # 调整连接超时时间
    pool_recycle=3600,  # 假设数据库超时时间大于3600秒
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
            log_db_error("db_session","sqlalchemy error",args,e)
            raise e
        except Exception as e:
            log_db_error("db_session","db operation failed",args,e)
            raise e
        finally:
            if session:
                session.close()
    return wrapper

def update_common_fields(obj):     
    obj.modify_id = request_tool.get_current_header().user_id
    obj.modify_time = datetime.now()
    obj.trace_id = request_tool.get_current_header().trace_id

def create_common_fields(obj):    
    obj.created_id = request_tool.get_current_header().user_id
    obj.created_time = datetime.now()
    obj.trace_id = request_tool.get_current_header().trace_id
    obj.is_active=True