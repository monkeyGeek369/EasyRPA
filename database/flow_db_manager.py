from database.models import Flow
from database.db_session import db_session,update_common_fields,create_common_fields
from easyrpa.tools import str_tools,number_tool

class FlowDbManager:
    @db_session
    def get_flows(session):
        return session.query(Flow).all()

    @db_session
    def get_flow_by_id(session, flow_id) -> Flow:
        return session.query(Flow).filter(Flow.id == flow_id).first()
    
    @db_session
    def get_flow_by_flow_code(session, flow_code) -> Flow:
        return session.query(Flow).filter(Flow.flow_code == flow_code).first()

    @db_session
    def create_flow(session, flow: Flow):
        # 不可以创建已经存在的flow_code
        if session.query(Flow).filter(Flow.flow_code == flow.flow_code).first():
            raise ValueError("Flow code already exists")
        create_common_fields(flow)
        session.add(flow)
        session.commit()
        session.refresh(flow)
        return flow.id

    @db_session
    def update_flow(session, flow:Flow):
        if not flow or not flow.id:
            raise ValueError("Flow ID cannot be empty")

        existing_flow = session.query(Flow).filter(Flow.id == flow.id).first()
        if existing_flow:
            if flow.flow_code and existing_flow.flow_code != flow.flow_code:
                # Check if flow_code is unique
                if session.query(Flow).filter(Flow.flow_code == flow.flow_code).first():
                    raise ValueError("Flow code already exists")
                existing_flow.flow_code = flow.flow_code

            if str_tools.str_is_not_empty(flow.flow_name) and existing_flow.flow_name != flow.flow_name:
                existing_flow.flow_name = flow.flow_name

            if number_tool.num_is_not_empty(flow.site_id) and existing_flow.site_id != flow.site_id:
                existing_flow.site_id = flow.site_id
                
            if number_tool.num_is_not_empty(flow.flow_rpa_type) and existing_flow.flow_rpa_type != flow.flow_rpa_type:
                existing_flow.flow_rpa_type = flow.flow_rpa_type

            if number_tool.num_is_not_empty(flow.flow_exe_env) and existing_flow.flow_exe_env != flow.flow_exe_env:
                existing_flow.flow_exe_env = flow.flow_exe_env

            if number_tool.num_is_not_empty(flow.flow_biz_type) and existing_flow.flow_biz_type != flow.flow_biz_type:
                existing_flow.flow_biz_type = flow.flow_biz_type
                
            if number_tool.num_is_not_empty(flow.max_retry_number) and existing_flow.max_retry_number != flow.max_retry_number:
                existing_flow.max_retry_number = flow.max_retry_number
            
            if number_tool.num_is_not_empty(flow.max_exe_time) and existing_flow.max_exe_time != flow.max_exe_time:
                existing_flow.max_exe_time = flow.max_exe_time

            if str_tools.str_is_not_empty(flow.retry_code) and existing_flow.retry_code != flow.retry_code:
                existing_flow.retry_code = flow.retry_code

            if str_tools.str_is_not_empty(flow.request_check_script) and existing_flow.request_check_script != flow.request_check_script:
                existing_flow.request_check_script = flow.request_check_script
                
            if str_tools.str_is_not_empty(flow.request_adapt_script) and existing_flow.request_adapt_script != flow.request_adapt_script:
                existing_flow.request_adapt_script = flow.request_adapt_script
                
            if str_tools.str_is_not_empty(flow.flow_exe_script) and existing_flow.flow_exe_script != flow.flow_exe_script:
                existing_flow.flow_exe_script = flow.flow_exe_script
                
            if str_tools.str_is_not_empty(flow.flow_result_handle_script) and existing_flow.flow_result_handle_script != flow.flow_result_handle_script:
                existing_flow.flow_result_handle_script = flow.flow_result_handle_script
            
            existing_flow.is_active = flow.is_active

            update_common_fields(existing_flow)
            session.commit()
            session.refresh(existing_flow)
            return existing_flow
        return None

    @db_session
    def delete_flow(session, flow_id):
        flow = session.query(Flow).filter(Flow.id == flow_id).first()
        if flow:
            session.delete(flow)
            session.commit()
            return True
        return False
    
    @db_session
    def get_flow_by_site_id(session, site_id:int) -> list[Flow]:
        return session.query(Flow).filter(Flow.site_id == site_id).all()
    
    @db_session
    def select_page_list(session,do:Flow,page: int,page_size: int,sorts: dict) -> list[Flow]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(Flow, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(Flow, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(Flow, key).desc())

        # 执行查询
        query = session.query(Flow).filter(
            Flow.id == do.id if do.id is not None else True,
            Flow.site_id == do.site_id if do.site_id is not None else True,
            Flow.flow_code.contains(do.flow_code) if do.flow_code is not None else True,
            Flow.flow_name.contains(do.flow_name) if do.flow_name is not None else True,
            Flow.flow_rpa_type == do.flow_rpa_type if do.flow_rpa_type is not None else True,
            Flow.flow_exe_env == do.flow_exe_env if do.flow_exe_env is not None else True,
            Flow.flow_biz_type == do.flow_biz_type if do.flow_biz_type is not None else True,
            Flow.retry_code.contains(do.retry_code) if do.retry_code is not None else True,
            Flow.created_id == do.created_id if do.created_id is not None else True,
            Flow.modify_id == do.modify_id if do.modify_id is not None else True,
            Flow.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:Flow) -> int:
        query = session.query(Flow).filter(
            Flow.id == do.id if do.id is not None else True,
            Flow.site_id == do.site_id if do.site_id is not None else True,
            Flow.flow_code.contains(do.flow_code) if do.flow_code is not None else True,
            Flow.flow_name.contains(do.flow_name) if do.flow_name is not None else True,
            Flow.flow_rpa_type == do.flow_rpa_type if do.flow_rpa_type is not None else True,
            Flow.flow_exe_env == do.flow_exe_env if do.flow_exe_env is not None else True,
            Flow.flow_biz_type == do.flow_biz_type if do.flow_biz_type is not None else True,
            Flow.retry_code.contains(do.retry_code) if do.retry_code is not None else True,
            Flow.created_id == do.created_id if do.created_id is not None else True,
            Flow.modify_id == do.modify_id if do.modify_id is not None else True,
            Flow.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    