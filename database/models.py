# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String,Text
from sqlalchemy.dialects.mysql import BIT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

# 生成数据库模型如下
# sqlacodegen --outfile=models.py mysql+pymysql://root:w/7714995779@127.0.0.1/easy_rpa


class DispatchData(Base):
    __tablename__ = 'dispatch_data'
    __table_args__ = {'comment': '调度数据表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='调度数据主键')
    job_id = Column(BigInteger, nullable=False, comment='所属jobid')
    data_business_no = Column(String(255), comment='数据业务编号（用于标记数据唯一性）')
    data_json = Column(LONGTEXT, nullable=False, comment='数据json')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')

class DispatchJob(Base):
    __tablename__ = 'dispatch_job'
    __table_args__ = {'comment': '调度计划表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='调度计划主键')
    job_name = Column(String(255), nullable=False, comment='计划名称')
    cron = Column(String(255), nullable=False, comment='调度规则')
    flow_code = Column(String(255), nullable=False, comment='流程code')
    flow_config_id = Column(BigInteger, comment='流程配置id')
    job_type = Column(Integer, nullable=False, comment='job类型（1数据爬取，2数据推送）')
    parent_job = Column(BigInteger, comment='父jobid')
    current_data_id = Column(BigInteger, comment='当前处理data表主键id')
    last_record_id = Column(BigInteger, comment='上一次调度记录id')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')

class DispatchRecord(Base):
    __tablename__ = 'dispatch_record'
    __table_args__ = {'comment': '调度记录表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='调度记录主键id')
    job_id = Column(BigInteger, nullable=False, comment='所属jobid')
    flow_task_id = Column(BigInteger, comment='流程任务id')
    status = Column(Integer, nullable=False, comment='调度状态（1、调度中，2、成功，3失败）')
    result_message = Column(Text, comment='结果消息内容')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')
    handler_data_id = Column(BigInteger, comment='对应处理数据id')

class DispatchHandlerData(Base):
    __tablename__ = 'dispatch_handler_data'
    __table_args__ = {'comment': '调度处理数据表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='调度记录主键id')
    job_id = Column(BigInteger, nullable=False, comment='所属jobid')
    data_job_id = Column(BigInteger, comment='调度数据归属jobid')
    data_id = Column(BigInteger, comment='调度数据id')
    status = Column(Integer, nullable=False, comment='处理状态（1、处理中，2、成功，3失败）')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')

class Flow(Base):
    __tablename__ = 'flow'
    __table_args__ = {'comment': '流程表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='流程主键')
    site_id = Column(BigInteger, nullable=False, comment='站点id')
    flow_code = Column(String(255), nullable=False, comment='流程code')
    flow_name = Column(String(255), nullable=False, comment='流程名称')
    flow_rpa_type = Column(Integer, nullable=False, comment='流程自动化类型（1网站/2桌面端）')
    flow_biz_type = Column(Integer, nullable=False, comment='流程业务类型（1、数据爬取/2、数据推送）')
    max_retry_number = Column(Integer, comment='最大重试次数')
    max_exe_time = Column(BigInteger, comment='最大执行时间（秒）')
    retry_code = Column(String(255), comment='重试code（逗号分隔）')
    request_check_script = Column(LONGTEXT, comment='请求数据校验脚本')
    request_adapt_script = Column(LONGTEXT, comment='请求数据适配脚本')
    flow_exe_script = Column(LONGTEXT, comment='流程执行脚本')
    flow_result_handle_script = Column(LONGTEXT, comment='流程执行结果处理脚本')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class FlowConfiguration(Base):
    __tablename__ = 'flow_configuration'
    __table_args__ = {'comment': '流程配置表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='流程配置主键')
    flow_id = Column(BigInteger, nullable=False, comment='流程id')
    config_name = Column(String(100), nullable=False, comment='流程配置名称')
    config_description = Column(String(255), comment='流程配置描述')
    config_json = Column(LONGTEXT, nullable=False, comment='流程配置json字符串')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class FlowTask(Base):
    __tablename__ = 'flow_task'
    __table_args__ = {'comment': '流程任务表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='流程任务主键')
    site_id = Column(BigInteger, nullable=False, comment='站点id')
    flow_id = Column(BigInteger, nullable=False, comment='流程id')
    flow_config_id = Column(BigInteger, nullable=False, comment='流程配置id')
    biz_no = Column(String(255), comment='业务编号')
    sub_source = Column(Integer, nullable=False, comment='订阅来源（1调度计划）')
    status = Column(Integer, nullable=False, comment='任务状态（1待执行2执行中3成功4失败）')
    result_code = Column(Integer, comment='任务结果code')
    result_message = Column(String(255), comment='任务消息')
    result_data = Column(LONGTEXT, comment='任务结果数据')
    retry_number = Column(Integer, comment='任务重试次数')
    screenshot_base64 = Column(LONGTEXT, comment='任务执行截图')
    request_standard_message = Column(LONGTEXT, comment='请求标准消息')
    flow_standard_message = Column(LONGTEXT, comment='流程标准消息')
    task_result_message = Column(LONGTEXT, comment='任务执行结果消息')
    flow_result_handle_message = Column(LONGTEXT, comment='流程结果处理消息')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class FlowTaskLog(Base):
    __tablename__ = 'flow_task_log'
    __table_args__ = {'comment': '流程任务日志表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='任务日志主键')
    task_id = Column(BigInteger, nullable=False, comment='任务id')
    log_type = Column(Integer, nullable=False, comment='日志类型（1文字2截图3任务结果）')
    message = Column(LONGTEXT, comment='日志消息体')
    screenshot = Column(LONGTEXT, comment='截图')
    robot_ip = Column(String(50), comment='机器人ip')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class RobotLog(Base):
    __tablename__ = 'robot_log'
    __table_args__ = {'comment': '机器人日志表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='机器人日志主键')
    robot_id = Column(BigInteger, nullable=False, comment='机器人id')
    task_id = Column(BigInteger, comment='任务id')
    log_type = Column(Integer, nullable=False, comment='日志类型（1info2warn3debug4biz）')
    message = Column(LONGTEXT, comment='日志消息')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class RobotStatu(Base):
    __tablename__ = 'robot_status'
    __table_args__ = {'comment': '机器人状态表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='机器人状态主键')
    robot_code = Column(String(255), nullable=False, comment='机器人code')
    robot_ip = Column(String(50), nullable=False, comment='机器人ip')
    status = Column(Integer, nullable=False, comment='机器人状态（1已关机2空闲3执行中4已关机）')
    port = Column(Integer, nullable=True, comment='服务端口')
    current_task_id = Column(BigInteger, comment='当前任务id')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {'comment': '站点表'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='站点主键')
    site_name = Column(String(100), nullable=False, unique=True, comment='站点名称')
    site_description = Column(String(255), comment='站点描述')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class MetaData(Base):
    __tablename__ = 'meta_data'
    __table_args__ = {'comment': '元数据'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='主键id')
    name = Column(String(255), nullable=False, comment='元数据名称')
    code = Column(String(255), nullable=False, comment='元数据code')
    description = Column(String(255), nullable=False, comment='元数据描述')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


class MetaDataItem(Base):
    __tablename__ = 'meta_data_item'
    __table_args__ = {'comment': '元数据项'}

    id = Column(BigInteger, primary_key=True, unique=True, comment='主键id')
    meta_id = Column(BigInteger, nullable=False, comment='元数据id')
    business_code = Column(String(255), nullable=False, comment='业务code标识')
    name_en = Column(String(255), nullable=False, comment='英文名称')
    name_cn = Column(String(255), nullable=False, comment='中文名称')
    created_id = Column(BigInteger, nullable=False, comment='创建人')
    created_time = Column(DateTime, nullable=False, comment='创建日期')
    modify_id = Column(BigInteger, comment='修改人')
    modify_time = Column(DateTime, comment='修改日期')
    trace_id = Column(String(255), comment='跟踪链路id')
    is_active = Column(BIT(1), nullable=False, comment='是否启用')


