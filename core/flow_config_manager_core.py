from database.models import FlowConfiguration
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.flow_config.flow_config_detail_model import FlowConfigDetailModel
from easyrpa.tools.common_tools import CommonTools
from database.flow_configuration_db_manager import FlowConfigurationDBManager
from transfer.flow_config_transfer import configs2ConfigDetailModels
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import number_tool,str_tools


def search_flow_configs_by_params(do:FlowConfiguration,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[FlowConfigDetailModel]:
    # search db
    db_result = FlowConfigurationDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = configs2ConfigDetailModels(db_result)
    
    return result

def search_count_by_params(do:FlowConfiguration) -> int:
    return FlowConfigurationDBManager.select_count(do=do)

def add_config(flow_id:int,config_name:str,config_description:str,config_json:str) -> int:
    # base check
    if number_tool.num_is_empty(flow_id):
        raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow_id)
    if str_tools.str_is_empty(config_name):
        raise EasyRpaException("config name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_name)
    if str_tools.str_is_empty(config_description):
        raise EasyRpaException("config description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_description)
    if str_tools.str_is_empty(config_json):
        raise EasyRpaException("config json is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_json)
    
    config = FlowConfiguration(
        flow_id=flow_id,
        config_name=config_name,
        config_description=config_description,
        config_json=config_json
    )

    flow_configuration = FlowConfigurationDBManager.create_flow_configuration(flow_configuration=config)
    if flow_configuration is None:
        return -1
    return flow_configuration.id

def modify_config(id:int,flow_id:int,config_name:str,config_description:str,config_json:str,is_active:bool) -> bool:
    # base check 
    if number_tool.num_is_empty(id):
        raise EasyRpaException("config id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    if number_tool.num_is_empty(flow_id):
        raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,flow_id)
    if str_tools.str_is_empty(config_name):
        raise EasyRpaException("config name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_name)
    if str_tools.str_is_empty(config_description):
        raise EasyRpaException("config description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_description)
    if str_tools.str_is_empty(config_json):
        raise EasyRpaException("config json is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config_json)
    
    config = FlowConfiguration(
        id=id,
        flow_id=flow_id,
        config_name=config_name,
        config_description=config_description,
        config_json=config_json,
        is_active=is_active
    )
    FlowConfigurationDBManager.update_flow_configuration(data=config)
    return True

def delete_config(id:int) -> bool:
    if number_tool.num_is_empty(id):
        raise EasyRpaException("config id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)

    return FlowConfigurationDBManager.delete_flow_configuration(id=id)

def search_config_by_ids(ids:list[int]) -> list[FlowConfigDetailModel]:
    if not ids:
        return []

    configs = FlowConfigurationDBManager.search_config_by_ids(ids=ids)
    return configs2ConfigDetailModels(configs)

def search_config_by_name(name:str) -> list[FlowConfigDetailModel]:
    if str_tools.str_is_empty(name):
        return []

    configs = FlowConfigurationDBManager.search_config_by_name(name=name)
    return configs2ConfigDetailModels(configs)
