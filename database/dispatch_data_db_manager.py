from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchData


class DispatchDatumDBManager:

    @db_session
    def get_all_dispatch_data(session):
        return session.query(DispatchData).all()

    @db_session
    def get_dispatch_data_by_id(session, id):
        return session.query(DispatchData).filter(DispatchData.id == id).first()

    @db_session
    def create_dispatch_data(session, dispatch_data:DispatchData):
        # job_id不可以为空
        if not dispatch_data.job_id:
            raise ValueError("Job ID cannot be empty")
        
        # data_json不可以为空
        if not dispatch_data.data_json:
            raise ValueError("Data JSON cannot be empty")
        
        # is_data_push不可以为空
        if not dispatch_data.is_data_push:
            raise ValueError("Is data push cannot be empty")

        create_common_fields(dispatch_data)
        session.add(dispatch_data)
        session.commit()
        return dispatch_data

    @db_session
    def update_dispatch_data(session, data:DispatchData):
        dispatch_data = session.query(DispatchData).filter(DispatchData.id == data.id).first()
        if dispatch_data:
            # job_id不为空则可更新
            if data.job_id:
                dispatch_data.job_id = data.job_id

            # data_json不为空则可更新
            if data.data_json:
                dispatch_data.data_json = data.data_json

            # is_data_push不为空则可更新
            if data.is_data_push:
                dispatch_data.is_data_push = data.is_data_push
            
            update_common_fields(dispatch_data)
            session.commit()
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