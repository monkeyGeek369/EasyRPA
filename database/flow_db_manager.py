from database.models import Flow
from database.db_session import db_session,update_common_fields,create_common_fields

class FlowDbManager:
    @db_session
    def get_flows(session):
        return session.query(Flow).all()

    @db_session
    def get_flow_by_id(session, flow_id) -> Flow:
        return session.query(Flow).filter(Flow.id == flow_id).first()

    @db_session
    def create_flow(session, flow: Flow):
        # 不可以创建已经存在的flow_code
        if session.query(Flow).filter(Flow.flow_code == flow.flow_code).first():
            raise ValueError("Flow code already exists")
        create_common_fields(flow)
        session.add(flow)
        session.commit()
        return flow.id

    @db_session
    def update_flow(session, flow:Flow):
        if not flow or not flow.id:
            raise ValueError("Flow ID cannot be empty")

        existing_flow = FlowDbManager.get_flow_by_id(session, flow_id=flow.id)
        if existing_flow:
            if flow.flow_code and existing_flow.flow_code != flow.flow_code:
                # Check if flow_code is unique
                if session.query(Flow).filter(Flow.flow_code == flow.flow_code).first():
                    raise ValueError("Flow code already exists")
                existing_flow.flow_code = flow.flow_code

            if not flow.flow_name and existing_flow.flow_name != flow.flow_name:
                existing_flow.flow_name = flow.flow_name

            if not flow.site_id and existing_flow.site_id != flow.site_id:
                existing_flow.site_id = flow.site_id
                
            if not flow.flow_rpa_type and existing_flow.flow_rpa_type != flow.flow_rpa_type:
                existing_flow.flow_rpa_type = flow.flow_rpa_type

            if not flow.flow_exe_env and existing_flow.flow_exe_env != flow.flow_exe_env:
                existing_flow.flow_exe_env = flow.flow_exe_env

            if not flow.flow_biz_type and existing_flow.flow_biz_type != flow.flow_biz_type:
                existing_flow.flow_biz_type = flow.flow_biz_type
                
            if not flow.max_retry_number and existing_flow.max_retry_number != flow.max_retry_number:
                existing_flow.max_retry_number = flow.max_retry_number
            
            if not flow.max_exe_time and existing_flow.max_exe_time != flow.max_exe_time:
                existing_flow.max_exe_time = flow.max_exe_time

            if not flow.retry_code and existing_flow.retry_code != flow.retry_code:
                existing_flow.retry_code = flow.retry_code

            if not flow.request_check_script and existing_flow.request_check_script != flow.request_check_script:
                existing_flow.request_check_script = flow.request_check_script
                
            if not flow.request_adapt_script and existing_flow.request_adapt_script != flow.request_adapt_script:
                existing_flow.request_adapt_script = flow.request_adapt_script
                
            if not flow.flow_exe_script and existing_flow.flow_exe_script != flow.flow_exe_script:
                existing_flow.flow_exe_script = flow.flow_exe_script
                
            if not flow.flow_result_handle_script and existing_flow.flow_result_handle_script != flow.flow_result_handle_script:
                existing_flow.flow_result_handle_script = flow.flow_result_handle_script

            update_common_fields(existing_flow)
            session.commit()
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