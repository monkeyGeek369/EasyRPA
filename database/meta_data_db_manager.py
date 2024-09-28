from database.models import MetaData
from database.db_session import db_session,update_common_fields,create_common_fields
from easyrpa.tools import str_tools,number_tool

class MetaDataDbManager:

    @db_session
    def create_meta_data(session, meta:MetaData):
        # base check
        if str_tools.str_is_empty(meta.name):
            raise ValueError("Name cannot be empty")
        if str_tools.str_is_empty(meta.code):
            raise ValueError("Code cannot be empty")
        if str_tools.str_is_empty(meta.description):
            raise ValueError("Description cannot be empty")
        
        # name或code不可以重复
        if session.query(MetaData).filter(MetaData.name == meta.name, MetaData.code == meta.code).first():
            raise ValueError("Name or Code already exists")

        create_common_fields(meta)
        session.add(meta)
        session.commit()
        session.refresh(meta)
        return meta

    @db_session
    def delete_meta_data(session, id:int):
        if number_tool.num_is_empty(id):
            raise ValueError("Meta Data ID cannot be empty")
        session.delete(id)
        session.commit()

    @db_session
    def update_meta_data(session, meta:MetaData):
        if number_tool.num_is_empty(meta.id):
            raise ValueError("Meta Data ID cannot be empty")

        # 根据id查询
        existing_meta = session.query(MetaData).filter(MetaData.id == meta.id).first()
        if existing_meta is None:
            raise ValueError("Meta Data not found")
        
        if str_tools.str_is_not_empty(meta.name) and existing_meta.name != meta.name:
            existing_meta.name = meta.name

        # 除了自己外，name不可以重复
        if session.query(MetaData).filter(MetaData.name == meta.name).filter(MetaData.id != meta.id).first():
            raise ValueError("Name already exists")
        
        if str_tools.str_is_not_empty(meta.code) and existing_meta.code != meta.code:
            existing_meta.code = meta.code
        
        # 除了自己外，code不可以重复
        if session.query(MetaData).filter(MetaData.code == meta.code).filter(MetaData.id != meta.id).first():
            raise ValueError("Code already exists")
        
        if str_tools.str_is_not_empty(meta.description) and existing_meta.description != meta.description:
            existing_meta.description = meta.description
        
        update_common_fields(existing_meta)
        session.commit()
        session.refresh(existing_meta)
        return existing_meta

    @db_session
    def get_meta_data_by_code(session, code:str):
        if str_tools.str_is_empty(code):
            raise ValueError("Meta Data Code cannot be empty")
        return session.query(MetaData).filter(MetaData.code == code).first()
