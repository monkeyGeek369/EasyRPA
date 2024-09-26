from easyrpa.tools.apscheduler_tool import APSchedulerTool
from configuration.app_config_manager import AppConfigManager
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from database.dispatch_job_db_manager import DispatchJobDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import DispatchJob,DispatchRecord
from easyrpa.tools import str_tools,number_tool,logs_tool
from check.dispatch_job_check import check_dispatch_job
from easyrpa.enums.job_type_enum import JobTypeEnum
from easyrpa.enums.job_status_enum import JobStatusEnum
from database.dispatch_record_db_manager import DispatchRecordDBManager
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
from database.meta_data_item_db_manager import MetaDataItemDbManager
from configuration.app_config_manager import AppConfigManager
from core.flow_manager_core import flow_task_subscribe
from database.dispatch_data_db_manager import DispatchDataDBManager

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

def job_execute_func(job:DispatchJob):
    # 基础校验
    check_dispatch_job(job=job)

    # 类型校验
    if job.job_type != JobTypeEnum.DATA_PULL.value[1] and job.job_type != JobTypeEnum.DATA_PUSH.value[1]:
        raise EasyRpaException('job type not support',EasyRpaExceptionCodeEnum.SYSTEM_NOT_IMPLEMENT.value[1],None)
    
    # 参数创建
    dispatch_record = None

    try:
        if number_tool.num_is_empty(job.id):
            raise EasyRpaException('job_id cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

        # 创建执行记录
        record = DispatchRecord(job_id=job.id,
                                status= JobStatusEnum.DISPATCHING.value[1]
                                )
        dispatch_record = DispatchRecordDBManager.create_dispatch_record(dispatch_record=record)

        # 触发任务执行
        app = AppConfigManager.get_app_config()
        sub_source = MetaDataItemDbManager.get_meta_data_item_by_meta_code_and_name_en(meta_code=app.get_flow_task_sub_source_meta_code(),
                                                                                       name_en=app.get_flow_task_sub_source_inner_job_dispatch_name_en())
        sub_param = None
        if job.job_type == JobTypeEnum.DATA_PULL.value[1]:
            # 数据拉取参数组装
            sub_param = FlowTaskSubscribeDTO(flow_configuration_id=job.flow_config_id,
                                    biz_no=dispatch_record.id,
                                    sub_source=sub_source,
                                    request_standard_message='{}',
                                    flow_code=job.flow_code)
        elif job.job_type == JobTypeEnum.DATA_PUSH.value[1]:
            # 数据推送参数组装
            sub_param = build_data_push_sub_param(job=job,record=dispatch_record,sub_source=sub_source)
        
        sub_result = flow_task_subscribe(dto=sub_param)

        # 判断调度结果
        if sub_result is None:
            raise EasyRpaException('job dispatch failed',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None)
        
        if not sub_result.status:
            raise EasyRpaException('job dispatch failed, result: {}'.format(sub_result.error_msg),EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None)

        # 更新执行记录
        dispatch_record.flow_task_id = sub_result.task_id
        DispatchRecordDBManager.update_dispatch_record(data=dispatch_record)

        # 更新job记录:last_record_id
        up_job = DispatchJob(id=job.id,last_record_id=dispatch_record.id)
        DispatchJobDBManager.update_dispatch_job(data=up_job)

        # 记录日志
        logs_tool.log_business_info("job_execute_pull","job execute success",dispatch_record)
    except Exception as e:
        # 记录日志
        logs_tool.log_business_error("job_execute_pull","job execute failed",dispatch_record,e)

        # 更新执行记录
        if dispatch_record is not None:
            dispatch_record.status = JobStatusEnum.DISPATCH_FAIL.value[1]
            dispatch_record.result_message = str(e)
            DispatchRecordDBManager.update_dispatch_record(data=dispatch_record)

def build_data_push_sub_param(job:DispatchJob,record:DispatchRecord,sub_source:int) -> FlowTaskSubscribeDTO:
    # base check
    if number_tool.num_is_empty(job.parent_job):
        raise EasyRpaException('push job execute, parent_job cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    # judge last_record is success
    next_data = None
    if number_tool.num_is_not_empty(job.last_record_id):
        last_record = DispatchRecordDBManager.get_dispatch_record_by_id(id=job.last_record_id)
        if last_record is not None and last_record.status != JobStatusEnum.DISPATCH_SUCCESS.value[1]:
            next_data = DispatchDataDBManager.get_dispatch_data_by_id(id=job.current_data_id)
            

    # get next data
    if next_data is None:
        if number_tool.num_is_empty(job.current_data_id):
            # get job first data
            next_data = DispatchDataDBManager.get_first_sort_asc_by_id(job_id=job.id)
        else:
            # get current_data_id next data_id
            pass

    # update data_id
    

    # todo
    pass