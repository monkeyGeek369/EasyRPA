# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"home_url":"https://github.com","login_url":"https://github.com/login","search_key":"playwright"}'''
config = '''{"account":"123","password":"456"}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=config)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------

import os
import ast
import json
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import number_tool,str_tools

# 将json字符串转换为dict取值
header = ast.literal_eval(os.environ.get("header"))
standart = json.loads(os.environ.get("standard"),object_hook=dict)
config = json.loads(os.environ.get("flow_config"),object_hook=dict)

# 校验header
if not header or len(header) <= 0:
    raise EasyRpaException("header params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)
if number_tool.num_is_empty(header.get("user_id")):
    raise EasyRpaException("user_id params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)
if str_tools.str_is_empty(header.get("trace_id")):
    raise EasyRpaException("trace_id params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)

# 校验标准参数
if not standart or len(standart) <= 0:
    raise EasyRpaException("standard params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("home_url")):
    raise EasyRpaException("home_url params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("login_url")):
    raise EasyRpaException("login_url params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("search_key")):
    raise EasyRpaException("search_key params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)

# 校验配置参数
if not config or len(config) <= 0:
    raise EasyRpaException("flow_config params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
if str_tools.str_is_empty(config.get("account")):
    raise EasyRpaException("account params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
if str_tools.str_is_empty(config.get("password")):
    raise EasyRpaException("password params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
