from easyrpa.models.flow.flow_task_subscribe_result_dto import FlowTaskSubscribeResultDTO
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
import check.flow_task_subscribe_dto_check as sub_check
from easyrpa.tools import str_tools,number_tool
from database.flow_db_manager import FlowDbManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.flow_configuration_db_manager import FlowConfigurationDBManager
from database.models import FlowTask,MetaDataItem
from core.script_exe_core import *
from database.flow_task_db_manager import FlowTaskDBManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
import json
from core.task_dispatch_core import flow_task_dispatch
from configuration.app_config_manager import AppConfigManager
from database.meta_data_db_manager import MetaDataDbManager
from database.meta_data_item_db_manager import MetaDataItemDbManager
from database.models import Flow
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.flow.flow_detail_model import FlowDetailModel
from easyrpa.tools.common_tools import CommonTools
from transfer.flow_transfer import flows2FlowDetailModels,flow2FlowDetailModel
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty

def flow_task_subscribe(dto:FlowTaskSubscribeDTO)-> FlowTaskSubscribeResultDTO:
    flow_task = FlowTask()
    try:
        # 参数校验
        sub_check.flow_task_subscribe_dto_check(dto)

        # 查询流程
        flow = None
        if str_tools.str_is_not_empty(dto.flow_code):
            flow = FlowDbManager.get_flow_by_flow_code(dto.flow_code)
        else:
            flow = FlowDbManager.get_flow_by_id(dto.flow_id)

        if flow is None:
            raise EasyRpaException("""flow {} not found""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
        
        dto.flow_id = flow.id
        dto.flow_code = flow.flow_code

        if str_tools.str_is_empty(flow.request_check_script):
            raise EasyRpaException("""flow {} not found check script""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
        if str_tools.str_is_empty(flow.request_adapt_script):
            raise EasyRpaException("""flow {} not found adapt script""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

        # 查询流程配置
        flow_configuration = FlowConfigurationDBManager.get_flow_configuration_by_id(dto.flow_configuration_id)
        if flow_configuration is None:
            raise EasyRpaException("""flow configuration {} not found""".format(dto.flow_configuration_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
        
        # 获取执行环境元数据
        rpa_exe_env = get_flow_exe_env_meta_data(flow_exe_env=flow.flow_exe_env)
        app = AppConfigManager()
        conda_env = app.get_console_default_conda_env()

        # 执行校验脚本
        request_check_script_exe(conda_env,dto.request_standard_message,flow.request_check_script,dto.sub_source,flow_configuration.config_json)

        # 执行适配脚本-获取流程报文字典
        dict_adapter_result = request_adapter_script_exe(conda_env,dto.request_standard_message,flow.request_adapt_script,dto.sub_source,flow_configuration.config_json)

        # 创建流程任务
        flow_task.flow_id = dto.flow_id
        flow_task.site_id = flow.site_id
        flow_task.biz_no = dto.biz_no
        flow_task.sub_source = dto.sub_source
        flow_task.status = FlowTaskStatusEnum.WAIT_EXE.value[1]
        flow_task.request_standard_message = dto.request_standard_message
        flow_task.flow_standard_message = json.dumps(dict_adapter_result)
        flow_task.flow_config_id = flow_configuration.id
        FlowTaskDBManager.create_flow_task(flow_task)

        # 流程任务分发
        flow_task_dispatch(flow,flow_task,flow_exe_env=rpa_exe_env.name_en)

        # 返回结果
        return FlowTaskSubscribeResultDTO(flow_task.id,True,"流程任务创建成功")
    except Exception as e:
        return FlowTaskSubscribeResultDTO(flow_task.id,False,str(e))
    
def get_flow_exe_env_meta_data(flow_exe_env:int) -> MetaDataItem:
    if number_tool.num_is_empty(flow_exe_env):
        raise EasyRpaException("""flow exe env is null""".format(flow_exe_env),EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,None)
    app = AppConfigManager()
    code = app.get_flow_exe_env_meta_code()
    meta_data = MetaDataDbManager.get_meta_data_by_code(code=code)
    if meta_data is None:
        raise EasyRpaException("""flow exe env meta data {} not found,please config meta data""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,flow_exe_env)
    
    meta_data_item = MetaDataItemDbManager.get_meta_data_item_by_meta_id_and_business_code(meta_id=meta_data.id,business_code=str(flow_exe_env))
    if meta_data_item is None:
        raise EasyRpaException("""flow exe env meta data item not found,please config meta data item""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,flow_exe_env)
    if str_tools.str_is_empty(meta_data_item.name_en):
        raise EasyRpaException("""flow exe env meta data item name_en not found,please config meta data item""".format(code),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,flow_exe_env)

    return meta_data_item

def search_flows_by_params(do:Flow,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[FlowDetailModel]:
    # search db
    db_result = FlowDbManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 

    # transfer
    result = flows2FlowDetailModels(db_result)
    
    return result

def search_count_by_params(do:Flow) -> int:
    return FlowDbManager.select_count(do=do)

def base_check(flow:Flow):
    if num_is_empty(flow.site_id):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.flow_code):
        raise EasyRpaException("flow_code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.flow_name):
        raise EasyRpaException("flow_name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if num_is_empty(flow.flow_rpa_type):
        raise EasyRpaException("flow_rpa_type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if num_is_empty(flow.flow_exe_env):
        raise EasyRpaException("flow_exe_env is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if num_is_empty(flow.flow_biz_type):
        raise EasyRpaException("flow_biz_type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if num_is_empty(flow.max_retry_number):
        raise EasyRpaException("max_retry_number is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if num_is_empty(flow.max_exe_time):
        raise EasyRpaException("max_exe_time is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.retry_code):
        raise EasyRpaException("retry_code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)

def add_flow(flow: Flow) -> int:
    base_check(flow=flow)
    if str_is_empty(flow.request_check_script):
        raise EasyRpaException("request_check_script is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.request_adapt_script):
        raise EasyRpaException("request_adapt_script is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.flow_exe_script):
        raise EasyRpaException("flow_exe_script is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if str_is_empty(flow.flow_result_handle_script):
        raise EasyRpaException("flow_result_handle_script is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    return FlowDbManager.create_flow(flow=flow)

def updata_flow(flow: Flow) -> bool:
    if num_is_empty(flow.id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    base_check(flow=flow)
    FlowDbManager.update_flow(flow=flow)
    return True

def logic_delete_flow(flow: Flow) -> int:
    if num_is_empty(flow.id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    if flow.is_active is None:
        raise EasyRpaException("is_active is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    return FlowDbManager.update_flow(flow=flow)

def updata_flow_script(flow: Flow) -> bool:
    if num_is_empty(flow.id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow)
    FlowDbManager.update_flow(flow=flow)
    return True

def search_flow_by_ids(ids: list[int]) -> dict[int,Flow]:
    result = FlowDbManager.get_flows_by_ids(flow_ids=ids)
    if result is None:
        return {}
    
    ret = {}
    for item in result:
        ret[item.id] = item
    return ret

def search_flow_by_name_or_code(query_str:str) -> list[FlowDetailModel]:
    result = FlowDbManager.search_flow_by_name_or_code(query_str=query_str)
    if result is None:
        return []
    return flows2FlowDetailModels(flows=result)

def search_flow_by_codes(codes:list[str]) -> list[FlowDetailModel]:
    result = FlowDbManager.search_flow_by_codes(flow_codes=codes)
    if result is None:
        return []
    return flows2FlowDetailModels(flows=result)