from abc import ABC, abstractmethod
from database.models import DispatchJob
from configuration.app_config_manager import AppConfigManager
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
from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
import jsonpickle

class JobTypeAbstractClass(ABC):
    def __init__(self, name:str, type:int):
        self.name = name
        self.type = type

    def execute_job(self,job:DispatchJob):    
        # job test
        #print('execute_job_test:'+str(jsonpickle.encode(job)))
        #return

        # 基础校验
        check_dispatch_job(job=job)

        # 类型校验
        if job.job_type != JobTypeEnum.DATA_PULL.value[1] and job.job_type != JobTypeEnum.DATA_PUSH.value[1]:
            raise EasyRpaException('execute_job:job type not support',EasyRpaExceptionCodeEnum.SYSTEM_NOT_IMPLEMENT.value[1],None)
        
        # 参数创建
        dispatch_record = None

        try:
            if number_tool.num_is_empty(job.id):
                raise EasyRpaException('execute_job:job_id cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

            # 创建执行记录
            record = DispatchRecord(job_id=job.id,
                                    status= JobStatusEnum.DISPATCHING.value[1]
                                    )
            dispatch_record = DispatchRecordDBManager.create_dispatch_record(dispatch_record=record)

            # 触发任务执行
            app = AppConfigManager()
            sub_source_item = MetaDataItemDbManager.get_meta_data_item_by_meta_code_and_name_en(meta_code=app.get_flow_task_sub_source_meta_code(),
                                                                                        name_en=app.get_flow_task_sub_source_inner_job_dispatch_name_en())
            sub_param = self.job_type_exe_param_builder(job=job,record=dispatch_record,sub_source=int(sub_source_item.business_code))
            sub_result = flow_task_subscribe(dto=sub_param)

            # 判断调度结果
            if sub_result is None:
                raise EasyRpaException('execute_job:job dispatch failed',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None)
            
            if not sub_result.status:
                raise EasyRpaException('execute_job:job dispatch failed, result: {}'.format(sub_result.error_msg),EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None)

            # 更新执行记录
            dispatch_record.flow_task_id = sub_result.task_id
            DispatchRecordDBManager.update_dispatch_record(data=dispatch_record)

            # 更新job记录:last_record_id
            up_job = DispatchJob(id=job.id,last_record_id=dispatch_record.id)
            DispatchJobDBManager.update_dispatch_job(data=up_job)

            # 记录日志
            logs_tool.log_business_info("execute_job:","job execute success",dispatch_record)
        except Exception as e:
            # 记录日志
            logs_tool.log_business_error("execute_job:","job execute failed",dispatch_record,e)

            # 更新执行记录
            if dispatch_record is not None:
                dispatch_record.status = JobStatusEnum.DISPATCH_FAIL.value[1]
                dispatch_record.result_message = str(e)
                DispatchRecordDBManager.update_dispatch_record(data=dispatch_record)

    @abstractmethod
    def job_type_exe_param_builder(self,job:DispatchJob,record:DispatchRecord,sub_source:int) -> FlowTaskSubscribeDTO:
        pass

    @abstractmethod
    def job_type_result_handler(self,dto:FlowTaskExeResultNotifyDTO):
        pass