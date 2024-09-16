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

# 将json字符串转换为dict取值
header = ast.literal_eval(os.environ.get("header"))
standart = json.loads(os.environ.get("standard"),object_hook=dict)
config = json.loads(os.environ.get("flow_config"),object_hook=dict)

# 构建json字符串对象
dict_params = {
    "home_url":standart.get("home_url"),
    "login_url":standart.get("login_url"),
    "search_key":standart.get("search_key"),
    "account":config.get("account"),
    "password":config.get("password")
}

# 必须保证key/value由双引号包裹，否则后续取值是问题
print(json.dumps(dict_params))