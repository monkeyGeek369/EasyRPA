# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"home_url":"https://github.com","login_url":"https://github.com/login","search_key":"playwright"}'''
config = '''{"account":"123","password":"456"}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=config)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------
