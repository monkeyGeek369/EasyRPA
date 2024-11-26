from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import FlowTask
from database.flow_task_log_db_manager import FlowTaskLogDBManager
from database.models import FlowTaskLog
from easyrpa.enums.log_type_enum import LogTypeEnum
from easyrpa.tools import str_tools,number_tool


class FlowTaskDBManager:

    @db_session
    def get_all_flow_task(session):
        return session.query(FlowTask).all()

    @db_session
    def get_flow_task_by_id(session, id):
        return session.query(FlowTask).filter(FlowTask.id == id).first()

    @db_session
    def create_flow_task(session, flow_task: FlowTask):
        # site_id不可以为空
        if number_tool.num_is_empty(flow_task.site_id):
            raise ValueError("Site ID cannot be empty")
        
        # flow_id不可以为空
        if number_tool.num_is_empty(flow_task.flow_id):
            raise ValueError("Flow ID cannot be empty")
        
        # biz_no不可以为空
        if str_tools.str_is_empty(flow_task.biz_no):
            raise ValueError("Biz No cannot be empty")
        
        # sub_source不可以为空
        if number_tool.num_is_empty(flow_task.sub_source):
            raise ValueError("Sub Source cannot be empty")
        
        # status不可以为空
        if flow_task.status is None:
            raise ValueError("Status cannot be empty")
        
        # request_standard_message不可以为空
        if str_tools.str_is_empty(flow_task.request_standard_message):
            raise ValueError("Request Standard Message cannot be empty")
        
        # flow_standard_message不可以为空
        if str_tools.str_is_empty(flow_task.flow_standard_message):
            raise ValueError("Flow Standard Message cannot be empty")

        create_common_fields(flow_task)
        session.add(flow_task)
        session.commit()
        session.refresh(flow_task)
        
        # 创建流程任务日志
        flow_task_log = FlowTaskLog()
        flow_task_log.task_id = flow_task.id
        flow_task_log.log_type = LogTypeEnum.TXT.value[1]
        flow_task_log.message = "流程任务创建成功"
        FlowTaskLogDBManager.create_flow_task_log(flow_task_log)

        return flow_task

    @db_session
    def update_flow_task(session, data:FlowTask):
        # id不可以为空
        if not data.id:
            raise ValueError("Flow task ID cannot be empty")

        flow_task = session.query(FlowTask).filter(FlowTask.id == data.id).first()
        if flow_task:
            # site_id不为空则可以更新
            if data.site_id:
                flow_task.site_id = data.site_id

            # flow_id不为空则可以更新
            if data.flow_id:
                flow_task.flow_id = data.flow_id

            # flow_config_id不为空则更新
            if data.flow_config_id:
                flow_task.flow_config_id = data.flow_config_id

            # biz_no不为空则可以更新
            if data.biz_no:
                flow_task.biz_no = data.biz_no

            # sub_source不为空则可以更新
            if data.sub_source:
                flow_task.sub_source = data.sub_source

            # status不为空则可以更新
            if data.status:
                flow_task.status = data.status

            # result_code不为空则可以更新
            if data.result_code:
                flow_task.result_code = data.result_code
            
            # result_message不为空则可以更新
            if data.result_message:
                flow_task.result_message = data.result_message

            # result_data不为空则可以更新
            if data.result_data:
                flow_task.result_data = data.result_data

            # retry_number不为空则可以更新
            if data.retry_number:
                flow_task.retry_number = data.retry_number

            # screenshot_base64不为空则可以更新
            if data.screenshot_base64:
                flow_task.screenshot_base64 = data.screenshot_base64

            # request_standard_message不为空则可以更新
            if data.request_standard_message:
                flow_task.request_standard_message = data.request_standard_message

            # flow_standard_message不为空则可以更新
            if data.flow_standard_message:
                flow_task.flow_standard_message = data.flow_standard_message

            # task_result_message不为空则可以更新
            if data.task_result_message:
                flow_task.task_result_message = data.task_result_message

            # flow_result_handle_message不为空则可以更新
            if data.flow_result_handle_message:
                flow_task.flow_result_handle_message = data.flow_result_handle_message

            update_common_fields(flow_task)
            session.commit()
            session.refresh(flow_task)
            return flow_task
        return None

    @db_session
    def delete_flow_task(session, id):
        flow_task = session.query(FlowTask).filter(FlowTask.id == id).first()
        if flow_task:
            session.delete(flow_task)
            session.commit()
            return True
        return False
    
    @db_session
    def get_flow_task_by_ids(session, ids: list[int]) ->list[FlowTask]:
        if not ids:
            return []
        return session.query(FlowTask).filter(FlowTask.id.in_(ids)).all()

    @db_session
    def select_page_list(session,do:FlowTask,page: int,page_size: int,sorts: dict) -> list[FlowTask]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(FlowTask, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(FlowTask, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(FlowTask, key).desc())

        # 执行查询
        query = session.query(FlowTask).filter(
            FlowTask.id == do.id if do.id is not None else True,
            FlowTask.site_id == do.site_id if do.site_id is not None else True,
            FlowTask.flow_id == do.flow_id if do.flow_id is not None else True,
            FlowTask.biz_no.contains(do.biz_no) if do.biz_no is not None else True,
            FlowTask.sub_source == do.sub_source if do.sub_source is not None else True,
            FlowTask.status == do.status if do.status is not None else True,
            FlowTask.result_code == do.result_code if do.result_code is not None else True,
            FlowTask.result_message.contains(do.result_message) if do.result_message is not None else True,
            FlowTask.result_data.contains(do.result_data) if do.result_data is not None else True,
            FlowTask.created_id == do.created_id if do.created_id is not None else True,
            FlowTask.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowTask.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:FlowTask) -> int:
        query = session.query(FlowTask).filter(
            FlowTask.id == do.id if do.id is not None else True,
            FlowTask.site_id == do.site_id if do.site_id is not None else True,
            FlowTask.flow_id == do.flow_id if do.flow_id is not None else True,
            FlowTask.biz_no.contains(do.biz_no) if do.biz_no is not None else True,
            FlowTask.sub_source == do.sub_source if do.sub_source is not None else True,
            FlowTask.status == do.status if do.status is not None else True,
            FlowTask.result_code == do.result_code if do.result_code is not None else True,
            FlowTask.result_message.contains(do.result_message) if do.result_message is not None else True,
            FlowTask.result_data.contains(do.result_data) if do.result_data is not None else True,
            FlowTask.created_id == do.created_id if do.created_id is not None else True,
            FlowTask.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowTask.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    