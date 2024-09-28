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