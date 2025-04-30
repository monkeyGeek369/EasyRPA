from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchHandlerData
from easyrpa.tools import str_tools,number_tool

class DispatchHandlerDataDBManager:

    @db_session
    def get_all_dispatch_handler_data(session):
        return session.query(DispatchHandlerData).all()
    
    @db_session
    def get_dispatch_handler_data_by_id(session, id) -> DispatchHandlerData:
        if number_tool.num_is_empty(id):
            return None
        return session.query(DispatchHandlerData).filter(DispatchHandlerData.id == id).first()
    
    @db_session
    def create_dispatch_handler_data(session, dispatch_handler_data:DispatchHandlerData) -> DispatchHandlerData:
        if number_tool.num_is_empty(dispatch_handler_data.job_id):
            raise ValueError("Job ID cannot be empty")
        if number_tool.num_is_empty(dispatch_handler_data.data_job_id):
            raise ValueError("Data Job ID cannot be empty")
        if number_tool.num_is_empty(dispatch_handler_data.data_id):
            raise ValueError("Data ID cannot be empty")
        if number_tool.num_is_empty(dispatch_handler_data.status):
            raise ValueError("Status cannot be empty")
        
        create_common_fields(dispatch_handler_data)
        session.add(dispatch_handler_data)
        session.commit()
        session.refresh(dispatch_handler_data)
        return dispatch_handler_data
    
    @db_session
    def update_dispatch_handler_data(session, data:DispatchHandlerData):
        if number_tool.num_is_empty(data.id):
            raise ValueError("id cannot be empty")
        
        dispatch_handler_data = session.query(DispatchHandlerData).filter(DispatchHandlerData.id == data.id).first()

        if dispatch_handler_data is not None:
            if number_tool.num_is_not_empty(data.job_id):
                dispatch_handler_data.job_id = data.job_id
            if number_tool.num_is_not_empty(data.data_job_id):
                dispatch_handler_data.data_job_id = data.data_job_id
            if number_tool.num_is_not_empty(data.data_id):
                dispatch_handler_data.data_id = data.data_id
            if number_tool.num_is_not_empty(data.status):
                dispatch_handler_data.status = data.status

            update_common_fields(dispatch_handler_data)
            session.commit()
            session.refresh(dispatch_handler_data)
            return dispatch_handler_data
        return None
    
    @db_session
    def delete_dispatch_handler_data(session, id):
        if number_tool.num_is_empty(id):
            raise ValueError("Dispatch Handler Data ID cannot be empty")

        dispatch_handler_data = session.query(DispatchHandlerData).filter(DispatchHandlerData.id == id).first()

        if dispatch_handler_data is not None:
            session.delete(dispatch_handler_data)
            session.commit()
            return True
        return False
    
    @db_session
    def delete_dispatch_handler_data_by_job_id(session, job_id):
        if number_tool.num_is_empty(job_id):
            raise ValueError("Job ID cannot be empty")

        session.query(DispatchHandlerData).filter(DispatchHandlerData.job_id == job_id).delete()
        session.commit()
    
    @db_session
    def select_page_list(session,do:DispatchHandlerData,page: int,page_size: int,sorts: dict) -> list[DispatchHandlerData]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(DispatchHandlerData, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(DispatchHandlerData, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(DispatchHandlerData, key).desc())

        # 执行查询
        query = session.query(DispatchHandlerData).filter(
            DispatchHandlerData.id == do.id if do.id != '' and do.id is not None and number_tool.num_is_not_empty(int(do.id)) else True,
            DispatchHandlerData.job_id == do.job_id if do.job_id != '' and do.job_id is not None and number_tool.num_is_not_empty(int(do.job_id)) else True,
            DispatchHandlerData.data_job_id == do.data_job_id if do.data_job_id != '' and do.data_job_id is not None and number_tool.num_is_not_empty(int(do.data_job_id)) else True,
            DispatchHandlerData.data_id == do.data_id if do.data_id != '' and do.data_id is not None and number_tool.num_is_not_empty(int(do.data_id)) else True,
            DispatchHandlerData.status == do.status if do.status != '' and do.status is not None and number_tool.num_is_not_empty(int(do.status)) else True,
            DispatchHandlerData.created_id == do.created_id if do.created_id != '' and do.created_id is not None and number_tool.num_is_not_empty(int(do.created_id)) else True,
            DispatchHandlerData.modify_id == do.modify_id if do.modify_id != '' and do.modify_id is not None and number_tool.num_is_not_empty(int(do.modify_id)) else True,
            DispatchHandlerData.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:DispatchHandlerData) -> int:
        query = session.query(DispatchHandlerData).filter(
            DispatchHandlerData.id == do.id if do.id != '' and do.id is not None and number_tool.num_is_not_empty(int(do.id)) else True,
            DispatchHandlerData.job_id == do.job_id if do.job_id != '' and do.job_id is not None and number_tool.num_is_not_empty(int(do.job_id)) else True,
            DispatchHandlerData.data_job_id == do.data_job_id if do.data_job_id != '' and do.data_job_id is not None and number_tool.num_is_not_empty(int(do.data_job_id)) else True,
            DispatchHandlerData.data_id == do.data_id if do.data_id != '' and do.data_id is not None and number_tool.num_is_not_empty(int(do.data_id)) else True,
            DispatchHandlerData.status == do.status if do.status != '' and do.status is not None and number_tool.num_is_not_empty(int(do.status)) else True,
            DispatchHandlerData.created_id == do.created_id if do.created_id != '' and do.created_id is not None and number_tool.num_is_not_empty(int(do.created_id)) else True,
            DispatchHandlerData.modify_id == do.modify_id if do.modify_id != '' and do.modify_id is not None and number_tool.num_is_not_empty(int(do.modify_id)) else True,
            DispatchHandlerData.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def select_dispatch_handler_datas_by_ids(session, ids: list[int]) -> list[DispatchHandlerData]:
        if ids is None or len(ids) == 0:
            return []
        return session.query(DispatchHandlerData).filter(DispatchHandlerData.id.in_(ids)).all()
    
    @db_session
    def get_all_by_status(session,job_id: int, status: int) -> list[DispatchHandlerData]:
        if status is None or job_id is None:
            return []
        return session.query(DispatchHandlerData).filter(DispatchHandlerData.job_id == job_id, DispatchHandlerData.status == status).all()
    
    @db_session
    def get_latest_job(session, job_id: int, status: list[int]) -> DispatchHandlerData:
        if status is None or job_id is None:
            return None
        return session.query(DispatchHandlerData).filter(DispatchHandlerData.job_id == job_id, DispatchHandlerData.status.in_(status)).order_by(DispatchHandlerData.id.desc()).first()
    

    