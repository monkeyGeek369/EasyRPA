from job.job_type_impl.job_type_abstract import JobTypeAbstractClass
from easyrpa.enums.job_type_enum import JobTypeEnum
from database.models import DispatchJob
from database.models import DispatchJob,DispatchRecord
from easyrpa.enums.job_type_enum import JobTypeEnum
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
from job.job_type_impl.job_type_abstract import JobTypeAbstractClass
from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.tools import str_tools,number_tool,logs_tool
from database.dispatch_job_db_manager import DispatchJobDBManager
from database.dispatch_record_db_manager import DispatchRecordDBManager
from database.dispatch_data_db_manager import DispatchDataDBManager
from easyrpa.tools.blake3_tool import Blake3Tool
from database.models import DispatchData,DispatchRecord
from easyrpa.enums.job_status_enum import JobStatusEnum
import json

class PullJobImplClass(JobTypeAbstractClass):
    def __init__(self):
        super().__init__(JobTypeEnum.DATA_PULL.value[0], JobTypeEnum.DATA_PULL.value[1])

    def job_type_exe_param_builder(self,job:DispatchJob,record:DispatchRecord,sub_source:int) -> FlowTaskSubscribeDTO:
        return FlowTaskSubscribeDTO(flow_id=0,
                                    flow_configuration_id=job.flow_config_id,
                                    biz_no=str(record.id),
                                    sub_source=sub_source,
                                    request_standard_message='{}',
                                    flow_code=job.flow_code)

    def job_type_result_handler(self,dto:FlowTaskExeResultNotifyDTO):
        record = None

        try:
            # if fail then return
            if dto.status != FlowTaskStatusEnum.SUCCESS.value[1]:
                raise EasyRpaException('task result job handler fail: task error',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,dto)

            # if result is empty then return
            if str_tools.str_is_empty(dto.result_data):
                raise EasyRpaException('task result job handler fail: task result is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

            # check result str is list
            data = json.loads(dto.result_data)
            if not isinstance(data,list):
                raise EasyRpaException('task result job handler fail: task result is not list',EasyRpaExceptionCodeEnum.DATA_TYPE_ERROR.value[1],None,dto)

            # search job record by biz_no
            if str_tools.str_is_empty(dto.biz_no):
                raise EasyRpaException('task result job handler fail: biz_no is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
            
            record = DispatchRecordDBManager.get_dispatch_record_by_id(id=int(dto.biz_no))
            if record is None:
                raise EasyRpaException('task result job handler fail: record not found',EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

            # search job by id
            if number_tool.num_is_empty(record.job_id):
                raise EasyRpaException('task result job handler fail: record job_id is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

            job = DispatchJobDBManager.get_dispatch_job_by_id(id=record.job_id)
            if job is None:
                raise EasyRpaException('task result job handler fail: job not found',EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

            # check job status is active
            if job.is_active != 1:
                raise EasyRpaException('task result job handler fail: job status is not active',EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,dto)

            # get item from list
            for item in data:
                if item is None:
                    continue
                item_str = json.dumps(item,ensure_ascii=False)
                # blake item,get hash key
                tool = Blake3Tool(salt=str(job.id), key='job')
                hash_key = tool.hash(item_str)
                if str_tools.str_is_empty(hash_key):
                    raise EasyRpaException('task result job handler fail: item hash key is empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
                # check hash key is exists
                data_search = DispatchDataDBManager.search_by_job_id_and_data_business_no(job_id=job.id,data_business_no=hash_key)
                if data_search is not None:
                    continue
                # insert into db
                insert_item = DispatchData(job_id=job.id,data_business_no=hash_key,data_json=item_str)
                DispatchDataDBManager.create_dispatch_data(dispatch_data=insert_item)

            # update job record status and message
            up_record = DispatchRecord(id=record.id,
                                    status=JobStatusEnum.DISPATCH_SUCCESS.value[1],
                                    result_message=JobStatusEnum.DISPATCH_SUCCESS.value[0])
            DispatchRecordDBManager.update_dispatch_record(data=up_record)

            # log record
            logs_tool.log_business_info("job_type_result_handler","pull task result job handler success",dto)

        except Exception as e:
            logs_tool.log_business_error("job_type_result_handler","pull task result job handler fail",dto,e)

            if record is not None:
                up_record = DispatchRecord(id=record.id,
                                        status=JobStatusEnum.DISPATCH_FAIL.value[1],
                                        result_message=str(e))
                DispatchRecordDBManager.update_dispatch_record(data=up_record)

            raise e