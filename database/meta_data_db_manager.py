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
        if session.query(MetaData).filter(MetaData.name == meta.name).first():
            raise ValueError("Name already exists")
        if session.query(MetaData).filter(MetaData.code == meta.code).first():
            raise ValueError("Code already exists")

        create_common_fields(meta)
        session.add(meta)
        session.commit()
        session.refresh(meta)
        return meta

    @db_session
    def delete_meta_data(session, id:int):
        if number_tool.num_is_empty(id):
            raise ValueError("Meta Data ID cannot be empty")
        # select by id
        meta = session.query(MetaData).filter(MetaData.id == id).first()
        if meta is None:
            raise ValueError("Meta Data not found")

        session.delete(meta)
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
        
        if meta.is_active is not None:
            existing_meta.is_active = meta.is_active
        
        update_common_fields(existing_meta)
        session.commit()
        session.refresh(existing_meta)
        return existing_meta

    @db_session
    def get_meta_data_by_code(session, code:str):
        if str_tools.str_is_empty(code):
            raise ValueError("Meta Data Code cannot be empty")
        return session.query(MetaData).filter(MetaData.code == code).first()
    
    @db_session
    def get_meta_data_by_id(session, id:int) -> MetaData:
        if number_tool.num_is_empty(id):
            raise ValueError("Meta Data ID cannot be empty")
        return session.query(MetaData).filter(MetaData.id == id).first()
    
    @db_session
    def select_page_list(session,do:MetaData,page: int,page_size: int,sorts: dict) -> list[MetaData]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(MetaData, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(MetaData, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(MetaData, key).desc())

        # 执行查询
        query = session.query(MetaData).filter(
            MetaData.id == do.id if do.id is not None else True,
            MetaData.name.contains(do.name) if do.name is not None else True,
            MetaData.code.contains(do.code) if do.code is not None else True,
            MetaData.description.contains(do.description) if do.description is not None else True,
            MetaData.created_id == do.created_id if do.created_id is not None else True,
            MetaData.modify_id == do.modify_id if do.modify_id is not None else True,
            MetaData.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:MetaData) -> int:
        query = session.query(MetaData).filter(
            MetaData.id == do.id if do.id is not None else True,
            MetaData.name.contains(do.name) if do.name is not None else True,
            MetaData.code.contains(do.code) if do.code is not None else True,
            MetaData.description.contains(do.description) if do.description is not None else True,
            MetaData.created_id == do.created_id if do.created_id is not None else True,
            MetaData.modify_id == do.modify_id if do.modify_id is not None else True,
            MetaData.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def get_meta_datas_by_codes(session, codes:list[str]) -> list[MetaData]:
        if codes is None or len(codes) <= 0:
            raise ValueError("Meta Data Codes cannot be empty")
        return session.query(MetaData).filter(MetaData.code.in_(codes)).all()
