from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import FlowConfiguration

class FlowConfigurationDBManager:

    @db_session
    def get_all_flow_configuration(session):
        return session.query(FlowConfiguration).all()

    @db_session
    def get_flow_configuration_by_id(session, id):
        return session.query(FlowConfiguration).filter(FlowConfiguration.id == id).first()

    @db_session
    def create_flow_configuration(session, flow_configuration:FlowConfiguration):
        # flow_id不可以为空
        if not flow_configuration.flow_id:
            raise ValueError("Flow ID cannot be empty")
        
        # config_name不可以为空且要唯一
        if not flow_configuration.config_name:
            raise ValueError("Config name cannot be empty")

        if session.query(FlowConfiguration).filter(FlowConfiguration.config_name == flow_configuration.config_name).first():
            raise ValueError("Config name already exists")
        
        # config_description不可以为空
        if not flow_configuration.config_description:
            raise ValueError("Config description cannot be empty")
        
        # config_json不可以为空
        if not flow_configuration.config_json:
            raise ValueError("Config json cannot be empty")
        
        create_common_fields(flow_configuration)
        session.add(flow_configuration)
        session.commit()
        session.refresh(flow_configuration)
        return flow_configuration

    @db_session
    def update_flow_configuration(session, data:FlowConfiguration):
        flow_configuration = session.query(FlowConfiguration).filter(FlowConfiguration.id == data.id).first()
        if flow_configuration:
            # flow_id不为空则可更新
            if data.flow_id:
                flow_configuration.flow_id = data.flow_id

            # config_name不为空且不自己不同且新值唯一则可更新
            if data.config_name:
                if flow_configuration.config_name != data.config_name:
                    if session.query(FlowConfiguration).filter(FlowConfiguration.config_name == data.config_name).first():
                        raise ValueError("Config name already exists")
                flow_configuration.config_name = data.config_name

            # config_description不为空则可更新
            if data.config_description:
                flow_configuration.config_description = data.config_description

            # config_json不为空则可更新
            if data.config_json:
                flow_configuration.config_json = data.config_json

            # is_active不为空则可更新
            if data.is_active is not None:
                flow_configuration.is_active = data.is_active

            update_common_fields(flow_configuration)
            session.commit()
            session.refresh(flow_configuration)
            return flow_configuration
        return None

    @db_session
    def delete_flow_configuration(session, id):
        flow_configuration = session.query(FlowConfiguration).filter(FlowConfiguration.id == id).first()
        if flow_configuration:
            session.delete(flow_configuration)
            session.commit()
            return True
        return False
    
    @db_session
    def select_page_list(session,do:FlowConfiguration,page: int,page_size: int,sorts: dict) -> list[FlowConfiguration]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(FlowConfiguration, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(FlowConfiguration, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(FlowConfiguration, key).desc())

        # 执行查询
        query = session.query(FlowConfiguration).filter(
            FlowConfiguration.id == do.id if do.id is not None else True,
            FlowConfiguration.flow_id == do.flow_id if do.flow_id is not None else True,
            FlowConfiguration.config_name.contains(do.config_name) if do.config_name is not None else True,
            FlowConfiguration.config_description.contains(do.config_description) if do.config_description is not None else True,
            FlowConfiguration.created_id == do.created_id if do.created_id is not None else True,
            FlowConfiguration.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowConfiguration.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:FlowConfiguration) -> int:
        query = session.query(FlowConfiguration).filter(
            FlowConfiguration.id == do.id if do.id is not None else True,
            FlowConfiguration.flow_id == do.flow_id if do.flow_id is not None else True,
            FlowConfiguration.config_name.contains(do.config_name) if do.config_name is not None else True,
            FlowConfiguration.config_description.contains(do.config_description) if do.config_description is not None else True,
            FlowConfiguration.created_id == do.created_id if do.created_id is not None else True,
            FlowConfiguration.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowConfiguration.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def search_config_by_ids(session,ids: list[int]) -> list[FlowConfiguration]:
        if ids is None or len(ids) == 0:
            return []
        
        return session.query(FlowConfiguration).filter(FlowConfiguration.id.in_(ids)).all()
    
    @db_session
    def search_config_by_name(session,name:str) -> list[FlowConfiguration]:
        if not name:
            return []
        
        return session.query(FlowConfiguration).filter(FlowConfiguration.config_name.contains(name)).all()
    