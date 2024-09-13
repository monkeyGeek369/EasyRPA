from flask import Blueprint
from flask import jsonify,Blueprint,request
from easyrpa.tools import logs_tool
from core.script_exe_core import request_check_script_exe

flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/result/handler', methods=['POST'])
def flow_task_result_handler():
    # 获取请求对象
    req_json = request.get_json()
    
    # 记录日志
    logs_tool.log_business_info("flow_task_result_handler","流程执行结果推送记录",req_json)

    # 模型转换

    # 查询流程

    # 执行返回值脚本
    #dict_response_result = request_check_script_exe("playwright",,,dto.sub_source,None)