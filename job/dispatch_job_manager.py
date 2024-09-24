from easyrpa.tools.apscheduler_tool import APSchedulerTool
from configuration.app_config_manager import AppConfigManager
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from database.dispatch_job_db_manager import DispatchJobDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import DispatchJob
from easyrpa.tools import str_tools,number_tool

def init_APSchedulerTool():
    app = AppConfigManager()

    if app.get_jobstores_default() != 'MemoryJobStore':
        raise EasyRpaException('not support jobstore:' + app.get_jobstores_default(),EasyRpaExceptionCodeEnum.DATA_TYPE_ERROR.value[1],None)

    scheduler_tool = APSchedulerTool(
        scheduler_type=app.get_scheduler_type(),
        executors={
            'default': ThreadPoolExecutor(max_workers=app.get_executors_default_thread_pool_max_workers()),
            'processpool': ProcessPoolExecutor(max_workers=app.get_executors_default_process_pool_max_workers())
        },
        job_defaults={
            'coalesce': app.get_job_default_coalesce(),
            'max_instances': app.get_job_default_max_instances(),
            'misfire_grace_time': app.get_job_default_misfire_grace_time(),
        },
        timezone=app.get_job_timezone(),
        jobstores={
            'default': MemoryJobStore()
        }
    )
    
    # 启动定时任务
    scheduler_tool.start()

    # 添加job任务
    add_all_jobs_to_scheduler()

    return scheduler_tool

def add_all_jobs_to_scheduler():
    # 查询所有启用的job
    dispatch_jobs = DispatchJobDBManager.get_all_active_dispatch_job()

    if dispatch_jobs is None:
        return
    if len(dispatch_jobs) == 0:
        return

    # 添加job
    for dispatch_job in dispatch_jobs:
        add_job_to_scheduler(dispatch_job)

def add_job_to_scheduler(dispatch_job:DispatchJob):
    if str_tools.str_is_empty(dispatch_job.cron):
        raise EasyRpaException('cron cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

    # 获取调度工具对象
    scheduler = APSchedulerTool()

    # 分割cron表达式
    cron_list = dispatch_job.cron.split(' ')
    if len(cron_list) != 6:
        raise EasyRpaException('cron format error, example: 0 0 0 * * *',EasyRpaExceptionCodeEnum.DATA_FORMAT_ERROR.value[1],None)

    # 执行job
    scheduler.add_job(job_execute_func,'cron',
                      second=cron_list[0],
                      minute=cron_list[1],
                      hour=cron_list[2],
                      day=cron_list[3],
                      month=cron_list[4],
                      day_of_week=cron_list[5],
                      kwargs={'dispatch_job':dispatch_job})

def job_execute_func(dispatch_job:DispatchJob):
    # todo
    print('job execute func')