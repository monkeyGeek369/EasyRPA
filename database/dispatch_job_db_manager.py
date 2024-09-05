from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchJob

class DispatchJobDBManager:
    @db_session
    def get_all_dispatch_job(session):
        return session.query(DispatchJob).all()

    @db_session
    def get_dispatch_job_by_id(session, id):
        return session.query(DispatchJob).filter(DispatchJob.id == id).first()

    @db_session
    def create_dispatch_job(session, dispatch_job:DispatchJob):
        # job_name不可以为空且唯一
        if not dispatch_job.job_name or session.query(DispatchJob).filter(DispatchJob.job_name == dispatch_job.job_name).first():
            raise ValueError("Job name cannot be empty")
        
        # cron不可以为空
        if not dispatch_job.cron:
            raise ValueError("Cron cannot be empty")
        
        # flow_code不可以为空
        if not dispatch_job.flow_code:
            raise ValueError("Flow code cannot be empty")
        
        # job_type不可以为空
        if not dispatch_job.job_type:
            raise ValueError("Job type cannot be empty")
        
        create_common_fields(dispatch_job)
        session.add(dispatch_job)
        session.commit()
        return dispatch_job

    @db_session
    def update_dispatch_job(session, data:DispatchJob):
        dispatch_job = session.query(DispatchJob).filter(DispatchJob.id == data.id).first()
        if dispatch_job:

            # job_name只能更新为除自身外的唯一值
            if data.job_name and dispatch_job.job_name != data.job_name:
                if session.query(DispatchJob).filter(DispatchJob.job_name == data.job_name).first():
                    raise ValueError("Job name already exists")
                dispatch_job.job_name = data.job_name

            # cron只能更新
            if data.cron and dispatch_job.cron != data.cron:
                dispatch_job.cron = data.cron

            # flow_code只能更新
            if data.flow_code and dispatch_job.flow_code != data.flow_code:
                dispatch_job.flow_code = data.flow_code

            # flow_config只能更新
            if data.flow_config and dispatch_job.flow_config != data.flow_config:
                dispatch_job.flow_config = data.flow_config

            # job_type只能更新
            if data.job_type and dispatch_job.job_type != data.job_type:
                dispatch_job.job_type = data.job_type

            # parent_job只能更新
            if data.parent_job and dispatch_job.parent_job != data.parent_job:
                dispatch_job.parent_job = data.parent_job

            update_common_fields(dispatch_job)
            session.commit()
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