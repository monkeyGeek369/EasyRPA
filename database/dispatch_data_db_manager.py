from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchData
from easyrpa.tools import str_tools,number_tool


class DispatchDataDBManager:

    @db_session
    def get_all_dispatch_data(session):
        return session.query(DispatchData).all()

    @db_session
    def get_dispatch_data_by_id(session, id):
        if number_tool.num_is_empty(id):
            return None
        return session.query(DispatchData).filter(DispatchData.id == id).first()

    @db_session
    def create_dispatch_data(session, dispatch_data:DispatchData):
        # job_id不可以为空
        if number_tool.num_is_empty(dispatch_data.job_id):
            raise ValueError("Job ID cannot be empty")
        
        # data_json不可以为空
        if str_tools.str_is_empty(dispatch_data.data_json):
            raise ValueError("Data JSON cannot be empty")
        
        create_common_fields(dispatch_data)
        session.add(dispatch_data)
        session.commit()
        session.refresh(dispatch_data)
        return dispatch_data

    @db_session
    def update_dispatch_data(session, data:DispatchData):
        if number_tool.num_is_empty(data.id):
            raise ValueError("Dispatch Data ID cannot be empty")

        dispatch_data = session.query(DispatchData).filter(DispatchData.id == data.id).first()

        if dispatch_data:
            # job_id不为空则可更新
            if number_tool.num_is_not_empty(data.job_id):
                dispatch_data.job_id = data.job_id

            # data_business_no不为空则可更新
            if str_tools.str_is_not_empty(data.data_business_no):
                dispatch_data.data_business_no = data.data_business_no

            # data_json不为空则可更新
            if str_tools.str_is_not_empty(data.data_json):
                dispatch_data.data_json = data.data_json

            update_common_fields(dispatch_data)
            session.commit()
            session.refresh(dispatch_data)
            return dispatch_data
        return None

    @db_session
    def delete_dispatch_data(session, id):
        dispatch_datum = session.query(DispatchData).filter(DispatchData.id == id).first()
        if dispatch_datum:
            session.delete(dispatch_datum)
            session.commit()
            return True
        return False
    
    @db_session
    def get_first_sort_asc_by_id(session,job_id:int) -> DispatchData:
        if number_tool.num_is_empty(job_id):
            raise ValueError("Job ID cannot be empty")

        dispatch_data = session.query(DispatchData).filter(DispatchData.job_id == job_id).order_by(DispatchData.id.asc()).first()

        if dispatch_data:
            return dispatch_data

        return None
    
    @db_session
    def get_next_sort_asc_by_id(session,id:int,job_id:int) -> DispatchData:
        if number_tool.num_is_empty(id):
            raise ValueError("Dispatch Data ID cannot be empty")
        if number_tool.num_is_empty(job_id):
            raise ValueError("Job ID cannot be empty")

        dispatch_data = session.query(DispatchData).filter(DispatchData.job_id == job_id).filter(DispatchData.id > id).order_by(DispatchData.id.asc()).first()

        if dispatch_data:
            return dispatch_data

        return None
    
    @db_session
    def search_by_job_id_and_data_business_no(session,job_id:int,data_business_no:str) -> DispatchData:
        if number_tool.num_is_empty(job_id) or str_tools.str_is_empty(data_business_no):
            raise ValueError("Job ID or Data Business No cannot be empty")

        return session.query(DispatchData).filter(DispatchData.job_id == job_id,DispatchData.data_business_no == data_business_no).first()

    @db_session
    def select_page_list(session,do:DispatchData,page: int,page_size: int,sorts: dict) -> list[DispatchData]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(DispatchData, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(DispatchData, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(DispatchData, key).desc())

        # 执行查询
        query = session.query(DispatchData).filter(
            DispatchData.id == do.id if do.id is not None else True,
            DispatchData.job_id == do.job_id if do.job_id is not None else True,
            DispatchData.data_business_no.contains(do.data_business_no) if do.data_business_no is not None else True,
            DispatchData.data_json.contains(do.data_json) if do.data_json is not None else True,
            DispatchData.created_id == do.created_id if do.created_id is not None else True,
            DispatchData.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchData.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:DispatchData) -> int:
        query = session.query(DispatchData).filter(
            DispatchData.id == do.id if do.id is not None else True,
            DispatchData.job_id == do.job_id if do.job_id is not None else True,
            DispatchData.data_business_no.contains(do.data_business_no) if do.data_business_no is not None else True,
            DispatchData.data_json.contains(do.data_json) if do.data_json is not None else True,
            DispatchData.created_id == do.created_id if do.created_id is not None else True,
            DispatchData.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchData.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def get_count(session,job_id:int) -> int:
        if number_tool.num_is_empty(job_id):
            raise ValueError("Job ID cannot be empty")

        return session.query(DispatchData).filter(DispatchData.job_id == job_id).count()
