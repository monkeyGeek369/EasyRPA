from easyrpa.tools.str_tools import str_to_str_dict
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.script_type_enum import ScriptTypeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import easyrpa.tools.debug_tools as my_debug
from easyrpa.tools import logs_tool,str_tools,blake3_tool
from easyrpa.script_exe import sync_python_script
import json

def request_check_script_exe(flow_code:str,flow_standard_message:str,
                    flow_exe_script:str,sub_source:int,flow_config:str) -> bool:
    """request check script exe method

    Args:
        flow_code (str): flow code
        flow_standard_message (str): standard message
        flow_exe_script (str): execute script
        sub_source (int): subscribe source
        flow_config (int): configuration

    Returns:
        ScriptExeResult: script exe result

    Raises:
        EasyRpaException: exception

    Returns:
        bool: true
    """
    # execute check script
    script_result = script_exe_base(flow_code=flow_code,script_type=ScriptTypeEnum.CHECK.value[0],flow_standard_message=flow_standard_message
                                    ,flow_exe_script=flow_exe_script,sub_source=sub_source,flow_config=flow_config)

    # check script result
    if script_result is None:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow_standard_message)
    if script_result.status is None or not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.error_msg)

    return True

def request_adapter_script_exe(flow_code:str,flow_standard_message:str,
                    flow_exe_script:str,sub_source:int,flow_config:str) -> dict:
    """request adapter script exe method

    Args:
        flow_code (str): flow code
        flow_standard_message (str): standard message
        flow_exe_script (str): execute script
        sub_source (int): subscribe source
        flow_config (int): configuration

    Returns:
        ScriptExeResult: script exe result

    Raises:
        EasyRpaException: exception

    Returns:
        dict: dict
    """
    
    # execute adapter script
    script_result = script_exe_base(flow_code=flow_code,script_type=ScriptTypeEnum.ADAPTER.value[0],flow_standard_message=flow_standard_message
                                    ,flow_exe_script=flow_exe_script,sub_source=sub_source,flow_config=flow_config)

    # check script result
    if not script_result:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow_standard_message)
    if not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.error_msg)
    if not script_result.result:
        raise EasyRpaException("script result result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.error_msg)
    
    # 执行结果转dict
    dict_result = str_to_str_dict(script_result.result)
    return dict_result


def response_result_script_exe(flow_code:str,response_message:str,
                    flow_exe_script:str,sub_source:int,flow_config:str) -> ScriptExeResult:
    """result script exe method

    Args:
        flow_code (str): flow code
        response_message (str): response message
        flow_exe_script (str): execute script
        sub_source (int): subscribe source
        flow_config (int): configuration

    Returns:
        ScriptExeResult: response script exe result

    Raises:
        EasyRpaException: exception

    Returns:
        ScriptExeResult: script exe result
    """
    
    # script exe
    script_result = script_exe_base(flow_code=flow_code,script_type=ScriptTypeEnum.RESPONSE.value[0],flow_standard_message=response_message
                                    ,flow_exe_script=flow_exe_script,sub_source=sub_source,flow_config=flow_config)

    # script result error
    if script_result is None or str_tools.str_is_empty(script_result.result):
        return script_result
    
    # script result success
    result_dict = json.loads(script_result.result)

    result = ScriptExeResult(status=result_dict.get("status")
                             ,error_msg=result_dict.get("error_msg")
                             ,result=result_dict.get("result")
                             ,code = result_dict.get("code"))

    return result

def script_exe_base(flow_code:str,script_type:str,flow_standard_message:str,
                    flow_exe_script:str,sub_source:int,flow_config:str) -> ScriptExeResult:
    """script exe base method

    Args:
        flow_code (str): flow code
        script_type (str): ScriptTypeEnum
        flow_standard_message (str): standard message
        flow_exe_script (str): execute script
        sub_source (int): subscribe source
        flow_config (int): configuration

    Returns:
        ScriptExeResult: script exe result
    """

    # get script hash
    hash_tools = blake3_tool.Blake3Tool(salt=flow_code,key="script_exe")
    script_hash = hash_tools.hash(data=flow_exe_script)
    if str_tools.str_is_empty(script_hash):
        raise EasyRpaException(script_type + "script hash generate error",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow_code)

    # check script is exist
    is_exist = sync_python_script.script_is_exist(flow_code=flow_code,script_type=script_type,script_hash=script_hash)

    # if not exist, create script file
    if not is_exist:
        sync_python_script.create_script_file(flow_code=flow_code,script_type=script_type,script_hash=script_hash,script=flow_exe_script)

    # builder script exe params
    param = my_debug.env_params_build(header=None,sub_source=sub_source,flow_standard_message=flow_standard_message,flow_config=flow_config)
    logs_tool.log_business_info("script_exe_base","script exe params",param)

    # run script
    script_result = sync_python_script.sync_script_run(flow_code=flow_code,script_type=script_type,script_hash=script_hash,params=param)
    
    logs_tool.log_business_info("script_exe_base","script exe result",script_result)
    return script_result