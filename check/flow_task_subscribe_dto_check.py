from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.tools import str_tools,number_tool
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum

def flow_task_subscribe_dto_check(dto:FlowTaskSubscribeDTO)->bool:
    if number_tool.num_is_empty(dto.flow_id):
        raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.flow_configuration_id):
        raise EasyRpaException("flow configuration id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.biz_no):
        raise EasyRpaException("biz no is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.sub_source):
        raise EasyRpaException("subscribe source is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.request_standard_message):
        raise EasyRpaException("request standard message is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True
