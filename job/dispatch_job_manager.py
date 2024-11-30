from easyrpa.tools.apscheduler_tool import APSchedulerTool
from configuration.app_config_manager import AppConfigManager
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from database.dispatch_job_db_manager import DispatchJobDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import DispatchJob
from easyrpa.tools import str_tools,logs_tool
from easyrpa.enums.job_type_enum import JobTypeEnum
from configuration.app_config_manager import AppConfigManager
from job.job_type_impl.job_type_abstract import JobTypeAbstractClass
from job.job_type_impl.pull_job_impl import PullJobImplClass
from job.job_type_impl.push_job_impl import PushJobImplClass

def init_APSchedulerTool():
    '''
    init easyrpa scheduler job
    '''
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
            'coalesce': False if str(app.get_job_default_coalesce()).lower() == 'false' else True,
            'max_instances': int(app.get_job_default_max_instances()),
            'misfire_grace_time': int(app.get_job_default_misfire_grace_time()),
        },
        timezone=app.get_job_timezone(),
        jobstores={
            'default': MemoryJobStore()
        }
    )
    
    # 启动定时任务
    scheduler_tool.start()

    # 添加job任务
    if app.isRegisterJobOnAppStart():
        add_all_jobs_to_scheduler()
    else:
        logs_tool.log_business_info('init_APSchedulerTool','not register job on app start',None)

    return scheduler_tool

def add_all_jobs_to_scheduler():
    '''
    add all jobs to scheduler
    '''
    # 查询所有启用的job
    dispatch_jobs = DispatchJobDBManager.get_all_active_dispatch_job()

    if dispatch_jobs is None:
        return
    if len(dispatch_jobs) == 0:
        return

    # 添加job
    for dispatch_job in dispatch_jobs:
        try:
            add_job_to_scheduler(dispatch_job)
        except Exception as e:
            logs_tool.log_business_error("add_all_jobs_to_scheduler","add job error",dispatch_job,e)

def add_job_to_scheduler(dispatch_job:DispatchJob):
    '''
    add job to scheduler
    '''

    if str_tools.str_is_empty(dispatch_job.cron):
        raise EasyRpaException('cron cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

    # 获取调度工具对象
    scheduler = APSchedulerTool()

    # 分割cron表达式
    cron_list = dispatch_job.cron.split(' ')
    if len(cron_list) != 6:
        raise EasyRpaException('cron format error, example: 0 0 0 * * *',EasyRpaExceptionCodeEnum.DATA_FORMAT_ERROR.value[1],None)

    # 执行job
    job_type_abc = get_job_type_impl(job_type=dispatch_job.job_type)
    scheduler.add_job(job_type_abc.execute_job,'cron',
                      second=cron_list[0],
                      minute=cron_list[1],
                      hour=cron_list[2],
                      day=cron_list[3],
                      month=cron_list[4],
                      day_of_week=cron_list[5],
                      kwargs={'job_id':dispatch_job.id})

def get_job_type_impl(job_type:int) -> JobTypeAbstractClass:
    '''
    get job type impl
    '''
    if job_type == JobTypeEnum.DATA_PULL.value[1]:
        return PullJobImplClass()
    elif job_type == JobTypeEnum.DATA_PUSH.value[1]:
        return PushJobImplClass()
    else:
        raise EasyRpaException('job type not support',EasyRpaExceptionCodeEnum.SYSTEM_NOT_IMPLEMENT.value[1],None)
    
def get_job_from_scheduler_by_id(job_id:int):
    '''
    get scheduler job by dispatch job id from scheduler
    '''
    # get scheduler
    scheduler = APSchedulerTool()

    # get all scheduler jobs
    scheduler_jobs = scheduler.get_all_jobs()
    if scheduler_jobs is None or len(scheduler_jobs) == 0:
        return None

    for job in scheduler_jobs:
        if job is not None and job.kwargs is not None and job.kwargs.get('job_id') is not None:
            if job.kwargs.get('job_id') == job_id:
                return job

def delete_job_from_scheduler_by_id(job_id:int):
    '''
    delete job by id
    '''
    # get scheduler job
    job = get_job_from_scheduler_by_id(job_id=job_id)

    if job is None:
        return
    
    scheduler_job_id = ''
    if job is not None and job.id is not None:
        scheduler_job_id = job.id
    else:
        return

    # delete job
    scheduler = APSchedulerTool()
    scheduler.delete_job(job_id=scheduler_job_id)

def update_scheduler_job_by_id(dispatch_job:DispatchJob):
    '''
    update scheduler job by dispatch job id
    '''
    if dispatch_job is None or dispatch_job.id is None:
        return
        
    # delete scheduler job
    delete_job_from_scheduler_by_id(job_id=dispatch_job.id)

    # add scheduler job
    add_job_to_scheduler(dispatch_job=dispatch_job)


