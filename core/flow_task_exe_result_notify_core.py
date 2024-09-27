from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
from easyrpa.tools import str_tools,number_tool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from configuration.app_config_manager import AppConfigManager
from database.meta_data_db_manager import MetaDataDbManager
from database.meta_data_item_db_manager import MetaDataItemDbManager
from database.models import MetaDataItem,FlowTaskLog
from database.flow_task_db_manager import FlowTaskLogDBManager
from easyrpa.enums.log_type_enum import LogTypeEnum
import jsonpickle
from job import dispatch_job_manager
from database.dispatch_job_db_manager import DispatchJobDBManager

def flow_task_exe_result_notify(dto:FlowTaskExeResultNotifyDTO):
    try:
        # 查询订阅来源
        meta_data_item = get_sub_source_meta_data_item(dto.sub_source)

        # 如果是内置job调度则进行处理
        app = AppConfigManager()
        inner_job_dispatch_name = app.get_flow_task_sub_source_inner_job_dispatch_name_en()
        if meta_data_item.name_en == inner_job_dispatch_name:
            job = DispatchJobDBManager.get_job_by_record_id(record_id=int(dto.biz_no))
            if job is None:
                raise EasyRpaException('job not found',EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

            abs = dispatch_job_manager.get_job_type_impl(job_type=job.job_type)
            abs.job_type_result_handler(dto=dto)
        else:
            # 其它来源的结果通知：理论上整个平台只有一种结果通知方式，例如mq、callback等，不应根据不同的来源方来自定义构建通知代码
            # todo
            pass

        # 日志记录
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= dto.flow_task_id
                                                            ,log_type=LogTypeEnum.TASK_RESULT_NOTIFY.value[1]
                                                            ,message="""flow task exe result notify success: {}""".format(jsonpickle.encode(dto))))
    except Exception as e:
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= dto.flow_task_id
                                                            ,log_type=LogTypeEnum.TASK_RESULT_NOTIFY.value[1]
                                                            ,message="""flow task exe result notify error: {}""".format(str(e))))
    

def get_sub_source_meta_data_item(sub_source:int) -> MetaDataItem:
    if number_tool.num_is_empty(sub_source):
        raise EasyRpaException("""sub_source is empty""".format(sub_source),EasyRpaExceptionCodeEnum.DATA_NULL.value[1])
    
    app = AppConfigManager()
    code = app.get_flow_task_sub_source_meta_code()
    meta_data = MetaDataDbManager.get_meta_data_by_code(code=code)
    if meta_data is None:
        raise EasyRpaException("""sub_source meta data {} not found,please config meta data""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,sub_source)
    
    meta_data_item = MetaDataItemDbManager.get_meta_data_item_by_meta_id_and_business_code(meta_id=meta_data.id,business_code=str(sub_source))
    if meta_data_item is None:
        raise EasyRpaException("""sub_source meta data item not found,please config meta data item""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,sub_source)
    if str_tools.str_is_empty(meta_data_item.name_en):
        raise EasyRpaException("""sub_source meta data item name_en not found,please config meta data item""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,sub_source)

    return meta_data_item
