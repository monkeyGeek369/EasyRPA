from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchJob
from easyrpa.tools import str_tools,number_tool
from database.dispatch_record_db_manager import DispatchRecordDBManager

class DispatchJobDBManager:
    @db_session
    def get_all_dispatch_job(session):
        return session.query(DispatchJob).all()
    
    @db_session
    def get_all_active_dispatch_job(session):
        return session.query(DispatchJob).filter(DispatchJob.is_active == True).all()

    @db_session
    def get_dispatch_job_by_id(session, id) -> DispatchJob:
        if number_tool.num_is_empty(id):
            return None
        return session.query(DispatchJob).filter(DispatchJob.id == id).first()

    @db_session
    def create_dispatch_job(session, dispatch_job:DispatchJob):
        # job_name不可以为空
        if str_tools.str_is_empty(dispatch_job.job_name):
            raise ValueError("Job name cannot be empty")
        
        # job_name要唯一
        if session.query(DispatchJob).filter(DispatchJob.job_name == dispatch_job.job_name).first():
            raise ValueError("Job name already exists")
        
        # cron不可以为空
        if str_tools.str_is_empty(dispatch_job.cron):
            raise ValueError("Cron cannot be empty")
        
        # flow_code不可以为空
        if str_tools.str_is_empty(dispatch_job.flow_code):
            raise ValueError("Flow code cannot be empty")
        
        # job_type不可以为空
        if number_tool.num_is_empty(dispatch_job.job_type):
            raise ValueError("Job type cannot be empty")
        
        create_common_fields(dispatch_job)
        session.add(dispatch_job)
        session.commit()
        session.refresh(dispatch_job)
        return dispatch_job

    @db_session
    def update_dispatch_job(session, data:DispatchJob):
        if number_tool.num_is_empty(data.id):
            raise ValueError("Id cannot be empty")

        dispatch_job = session.query(DispatchJob).filter(DispatchJob.id == data.id).first()

        if dispatch_job is not None:
            # job_name只能更新为除自身外的唯一值
            if str_tools.str_is_not_empty(data.job_name) and dispatch_job.job_name != data.job_name:
                if session.query(DispatchJob).filter(DispatchJob.job_name == data.job_name).first():
                    raise ValueError("Job name already exists")
                dispatch_job.job_name = data.job_name

            # cron只能更新
            if str_tools.str_is_not_empty(data.cron) and dispatch_job.cron != data.cron:
                dispatch_job.cron = data.cron

            # flow_code只能更新
            if str_tools.str_is_not_empty(data.flow_code) and dispatch_job.flow_code != data.flow_code:
                dispatch_job.flow_code = data.flow_code

            # flow_config_id只能更新
            if number_tool.num_is_not_empty(data.flow_config_id) and dispatch_job.flow_config_id != data.flow_config_id:
                dispatch_job.flow_config_id = data.flow_config_id

            # job_type只能更新
            if number_tool.num_is_not_empty(data.job_type) and dispatch_job.job_type != data.job_type:
                dispatch_job.job_type = data.job_type

            # parent_job只能更新
            if data.parent_job == data.id:
                raise ValueError("Parent job cannot be self") 
            if number_tool.num_is_not_empty(data.parent_job) and dispatch_job.parent_job != data.parent_job:
                dispatch_job.parent_job = data.parent_job

            # current_data_id只能更新
            if number_tool.num_is_not_empty(data.current_data_id) and dispatch_job.current_data_id != data.current_data_id:
                dispatch_job.current_data_id = data.current_data_id

            # last_record_id只能更新
            if number_tool.num_is_not_empty(data.last_record_id) and dispatch_job.last_record_id != data.last_record_id:
                dispatch_job.last_record_id = data.last_record_id

            # is_active只能更新
            if data.is_active is not None:
                dispatch_job.is_active = data.is_active

            update_common_fields(dispatch_job)
            session.commit()
            session.refresh(dispatch_job)
            return dispatch_job
        return None

    @db_session
    def delete_dispatch_job(session, id):
        dispatch_job = session.query(DispatchJob).filter(DispatchJob.id == id).first()
        if dispatch_job:
            session.delete(dispatch_job)
            session.commit()
            return True
        return False
    
    @db_session
    def get_job_by_record_id(session, record_id:int) -> DispatchJob:
        if number_tool.num_is_empty(record_id):
            return None
        
        # search job record
        record = DispatchRecordDBManager.get_dispatch_record_by_id(id=record_id)
        if record is None or number_tool.num_is_empty(record.job_id):
            return None

        job = session.query(DispatchJob).filter(DispatchJob.id == record.job_id).first()
        
        if job is None:
            return None
        return job
    
    @db_session
    def select_page_list(session,do:DispatchJob,page: int,page_size: int,sorts: dict) -> list[DispatchJob]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(DispatchJob, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(DispatchJob, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(DispatchJob, key).desc())

        # 执行查询
        query = session.query(DispatchJob).filter(
            DispatchJob.id == do.id if do.id is not None else True,
            DispatchJob.job_name.contains(do.job_name) if do.job_name is not None else True,
            DispatchJob.flow_code == do.flow_code if do.flow_code is not None else True,
            DispatchJob.flow_config_id == do.flow_config_id if do.flow_config_id is not None else True,
            DispatchJob.job_type == do.job_type if do.job_type is not None else True,
            DispatchJob.parent_job == do.parent_job if do.parent_job is not None else True,
            DispatchJob.created_id == do.created_id if do.created_id is not None else True,
            DispatchJob.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchJob.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:DispatchJob) -> int:
        query = session.query(DispatchJob).filter(
            DispatchJob.id == do.id if do.id is not None else True,
            DispatchJob.job_name.contains(do.job_name) if do.job_name is not None else True,
            DispatchJob.flow_code == do.flow_code if do.flow_code is not None else True,
            DispatchJob.flow_config_id == do.flow_config_id if do.flow_config_id is not None else True,
            DispatchJob.job_type == do.job_type if do.job_type is not None else True,
            DispatchJob.parent_job == do.parent_job if do.parent_job is not None else True,
            DispatchJob.created_id == do.created_id if do.created_id is not None else True,
            DispatchJob.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchJob.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def search_job_by_ids(session, ids: list[int]) -> list[DispatchJob]:
        if ids is None or len(ids) == 0:
            return []
        
        return session.query(DispatchJob).filter(DispatchJob.id.in_(ids)).all()
    
    @db_session
    def search_job_by_name(session, name: str) -> list[DispatchJob]:
        if str_tools.str_is_empty(name):
            return []
        return session.query(DispatchJob).filter(DispatchJob.job_name.contains(name)).all()
    