from job.job_type_impl.job_type_abstract import JobTypeAbstractClass
from easyrpa.enums.job_type_enum import JobTypeEnum
from database.models import DispatchJob
from database.dispatch_job_db_manager import DispatchJobDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import DispatchJob,DispatchRecord,DispatchHandlerData
from easyrpa.tools import str_tools,number_tool,logs_tool
from easyrpa.enums.job_type_enum import JobTypeEnum
from easyrpa.enums.job_status_enum import JobStatusEnum
from database.dispatch_record_db_manager import DispatchRecordDBManager
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
from database.dispatch_data_db_manager import DispatchDataDBManager
from job.job_type_impl.job_type_abstract import JobTypeAbstractClass
from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from database.dispatch_handler_data_db_manager import DispatchHandlerDataDBManager
import json,threading

lock = threading.Lock()

class PushJobImplClass(JobTypeAbstractClass):
    def __init__(self):
        super().__init__(JobTypeEnum.DATA_PUSH.value[0], JobTypeEnum.DATA_PUSH.value[1])

    def job_type_exe_param_builder(self,job:DispatchJob,record:DispatchRecord,sub_source:int) -> FlowTaskSubscribeDTO:
        with lock:
            # base check
            if number_tool.num_is_empty(job.parent_job):
                raise EasyRpaException('push job execute, parent_job cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
            
            # get all error handler data
            error_handler_datas = DispatchHandlerDataDBManager.get_all_by_status(status=JobStatusEnum.DISPATCH_FAIL.value[1])

            # get next data
            is_error_handler_data = False
            next_data = None
            if error_handler_datas is not None and len(error_handler_datas) > 0:
                next_data = DispatchDataDBManager.get_dispatch_data_by_id(id=error_handler_datas[0].data_id)
                is_error_handler_data = True
            elif number_tool.num_is_not_empty(job.last_record_id):
                last_record = DispatchRecordDBManager.get_dispatch_record_by_id(id=job.last_record_id)
                if last_record is not None and (last_record.status == JobStatusEnum.DISPATCH_SUCCESS.value[1] or last_record.status == JobStatusEnum.DISPATCHING.value[1]):
                    # get executing handler data
                    executing_handler_datas = DispatchHandlerDataDBManager.get_all_by_status(status=JobStatusEnum.DISPATCHING.value[1])
                    if executing_handler_datas is not None and len(executing_handler_datas) > 0:
                        max_data_id = max([item.data_id for item in executing_handler_datas])
                        next_data = DispatchDataDBManager.get_next_sort_asc_by_id(id=max_data_id,job_id=job.parent_job)
                    else:
                        next_data = DispatchDataDBManager.get_next_sort_asc_by_id(id=job.current_data_id,job_id=job.parent_job)
                else:
                    # get current_data_id
                    next_data = DispatchDataDBManager.get_dispatch_data_by_id(id=job.current_data_id)
            else:
                # get job first data
                next_data = DispatchDataDBManager.get_first_sort_asc_by_id(job_id=job.parent_job)

            # check
            if next_data is None:
                raise EasyRpaException('push job execute, next data is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

            # build sub_param
            sub_param = FlowTaskSubscribeDTO(flow_id=0,
                                            flow_configuration_id=job.flow_config_id,
                                            biz_no=str(record.id),
                                            sub_source=sub_source,
                                            request_standard_message=next_data.data_json,
                                            flow_code=job.flow_code)
            
            # update data_id
            up_job = DispatchJob(id=job.id,current_data_id=next_data.id)
            DispatchJobDBManager.update_dispatch_job(data=up_job)

            # update handler data
            handler_data = None
            if is_error_handler_data:
                # update
                handler_data = DispatchHandlerData(id=error_handler_datas[0].id,status=JobStatusEnum.DISPATCHING.value[1])
                DispatchHandlerDataDBManager.update_dispatch_handler_data(data=handler_data)
            else:
                # insert
                handler_data = DispatchHandlerData(job_id=job.id,data_job_id=job.parent_job,data_id=next_data.id,status=JobStatusEnum.DISPATCHING.value[1])
                handler_data = DispatchHandlerDataDBManager.create_dispatch_handler_data(dispatch_handler_data=handler_data)

            # update dispatch record
            if handler_data is not None:
                up_record = DispatchRecord(id=record.id,handler_data_id=handler_data.id)
                DispatchRecordDBManager.update_dispatch_record(data=up_record)
                record.handler_data_id = handler_data.id

            return sub_param
    
    def job_type_result_handler(self,dto:FlowTaskExeResultNotifyDTO):
        record = None

        try:
            # search job record by biz_no
            if str_tools.str_is_empty(dto.biz_no):
                raise EasyRpaException('task result job handler fail: biz_no is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
            
            record = DispatchRecordDBManager.get_dispatch_record_by_id(id=int(dto.biz_no))
            if record is None:
                raise EasyRpaException('task result job handler fail: record not found',EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

            # if fail then return
            if dto.status != FlowTaskStatusEnum.SUCCESS.value[1]:
                raise EasyRpaException('task result job handler fail: task error',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,dto)

            # search job by id
            if number_tool.num_is_empty(record.job_id):
                raise EasyRpaException('task result job handler fail: record job_id is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

            job = DispatchJobDBManager.get_dispatch_job_by_id(id=record.job_id)
            if job is None:
                raise EasyRpaException('task result job handler fail: job not found',EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

            # check job status is active
            if job.is_active != 1:
                raise EasyRpaException('task result job handler fail: job status is not active',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,dto)

            # update job record status and message
            up_record = DispatchRecord(id=record.id,
                                    status=JobStatusEnum.DISPATCH_SUCCESS.value[1],
                                    result_message=JobStatusEnum.DISPATCH_SUCCESS.value[0])
            DispatchRecordDBManager.update_dispatch_record(data=up_record)

            # update handler data
            if record.handler_data_id is not None:
                DispatchHandlerDataDBManager.update_dispatch_handler_data(data=DispatchHandlerData(id=record.handler_data_id,status=JobStatusEnum.DISPATCH_SUCCESS.value[1]))

            # log record
            logs_tool.log_business_info("job_type_result_handler","push task result job handler success",dto)

        except Exception as e:
            logs_tool.log_business_error("job_type_result_handler","push task result job handler fail",dto,e)

            if record is not None:
                up_record = DispatchRecord(id=record.id,
                                        status=JobStatusEnum.DISPATCH_FAIL.value[1],
                                        result_message=str(e))
                DispatchRecordDBManager.update_dispatch_record(data=up_record)

            raise e