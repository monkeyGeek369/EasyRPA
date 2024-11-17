from models.flow.flow_detail_model import FlowDetailModel
from models.site.site_detail_model import SiteDetailModel
from database.models import Flow
from copy import deepcopy
from core import site_manager_core,meta_data_manager_core,meta_data_item_manager_core
from configuration.app_config_manager import AppConfigManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum

def flow2FlowDetailModel(flow:Flow,site_detail:SiteDetailModel,exe_env_item:dict,biz_type_item:dict,rpa_type_item:dict) -> FlowDetailModel:
    # copy
    flow_detail = FlowDetailModel(
        id=flow.id,
        site_id=flow.site_id,
        site_name=site_detail.site_name if site_detail is not None else None,
        flow_code=flow.flow_code,
        flow_name=flow.flow_name,
        flow_rpa_type=flow.flow_rpa_type,
        flow_rpa_type_name=rpa_type_item.name_cn if rpa_type_item is not None else None,
        flow_exe_env=flow.flow_exe_env,
        flow_exe_env_name=exe_env_item.name_cn if exe_env_item is not None else None,
        flow_biz_type=flow.flow_biz_type,
        flow_biz_type_name=biz_type_item.name_cn if biz_type_item is not None else None,
        max_retry_number=flow.max_retry_number,
        max_exe_time=flow.max_exe_time,
        retry_code=flow.retry_code,
        request_check_script=flow.request_check_script,
        request_adapt_script=flow.request_adapt_script,
        flow_exe_script=flow.flow_exe_script,
        flow_result_handle_script=flow.flow_result_handle_script,
        created_id=flow.created_id,
        created_time=flow.created_time,
        modify_id=flow.modify_id,
        modify_time=flow.modify_time,
        trace_id=flow.trace_id,
        is_active=flow.is_active
    )

    return flow_detail

def flows2FlowDetailModels(flows:list[Flow]) -> list[FlowDetailModel]:
    if flows is None or len(flows) <= 0:
        return []
    
    # get site ids
    site_ids = []
    for item in flows:
        if item.site_id is not None and item.site_id not in site_ids:
            site_ids.append(item.site_id)

    # search sites
    site_details = []
    if len(site_ids) > 0:
        site_details = site_manager_core.search_sites_by_ids(site_ids=site_ids)
    # site_details to map
    site_details_map = {item.id:item for item in site_details}
    if site_details_map is None or len(site_details_map) <= 0:
        raise EasyRpaException("site details is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)

    # search meta data
    app = AppConfigManager()
    codes = []
    codes.append(app.get_flow_exe_env_meta_code())
    codes.append(app.get_flow_biz_type_meta_code())
    codes.append(app.get_flow_rpa_type_meta_code())
    meta_datas = meta_data_manager_core.search_meta_datas_by_codes(codes=codes)
    if meta_datas is None or len(meta_datas) <= 0:
        raise EasyRpaException("flow meta data is empty(env,biz_type,rpa_type)",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)
    meta_data_map = {item.code:item for item in meta_datas}

    # search meta data item
    if meta_data_map[app.get_flow_exe_env_meta_code()] is None:
        raise EasyRpaException("flow exe env meta data is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)
    exe_env_item_map = meta_data_item_manager_core.get_meta_data_item_map(meta_id=meta_data_map[app.get_flow_exe_env_meta_code()].id)
    if exe_env_item_map is None or len(exe_env_item_map) <= 0:
        raise EasyRpaException("flow exe env meta data item is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)

    if meta_data_map[app.get_flow_biz_type_meta_code()] is None:
        raise EasyRpaException("flow biz type meta data is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)
    biz_type_item_map = meta_data_item_manager_core.get_meta_data_item_map(meta_id=meta_data_map[app.get_flow_biz_type_meta_code()].id)
    if biz_type_item_map is None or len(biz_type_item_map) <= 0:
        raise EasyRpaException("flow biz type meta data item is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)
    
    if meta_data_map[app.get_flow_rpa_type_meta_code()] is None:
        raise EasyRpaException("flow rpa type meta data is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)
    rpa_type_item_map = meta_data_item_manager_core.get_meta_data_item_map(meta_id=meta_data_map[app.get_flow_rpa_type_meta_code()].id)
    if rpa_type_item_map is None or len(rpa_type_item_map) <= 0:
        raise EasyRpaException("flow rpa type meta data item is empty",EasyRpaExceptionCodeEnum.DATA_EMPTY.value[1],None,None)

    # transfer
    result = []
    for flow in flows:
        if flow is None:
            continue
        site_detail_item = site_details_map[flow.site_id] if flow.site_id in site_details_map else None
        exe_env_item = exe_env_item_map[str(flow.flow_exe_env)] if str(flow.flow_exe_env) in exe_env_item_map else None
        biz_type_item = biz_type_item_map[str(flow.flow_biz_type)] if str(flow.flow_biz_type) in biz_type_item_map else None
        rpa_type_item = rpa_type_item_map[str(flow.flow_rpa_type)] if str(flow.flow_rpa_type) in rpa_type_item_map else None
        result.append(flow2FlowDetailModel(flow,site_detail_item,exe_env_item,biz_type_item,rpa_type_item))

    return result