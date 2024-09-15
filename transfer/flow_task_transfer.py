from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO

def request_json_to_FlowTaskExeResDTO(json_data:dict) -> FlowTaskExeResDTO:
    return FlowTaskExeResDTO(**json_data)