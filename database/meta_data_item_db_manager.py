from database.models import MetaDataItem
from database.db_session import db_session,update_common_fields,create_common_fields
from easyrpa.tools import str_tools,number_tool

class MetaDataItemDbManager:

    @db_session
    def create_meta_data_item(session, item: MetaDataItem):
        # base check 
        if number_tool.num_is_empty(item.meta_id):
            raise ValueError("Meta ID cannot be empty")
        if str_tools.str_is_empty(item.business_code):
            raise ValueError("Business Code cannot be empty")
        if str_tools.str_is_empty(item.name_en):
            raise ValueError("Name En cannot be empty")
        if str_tools.str_is_empty(item.name_cn):
            raise ValueError("Name Cn cannot be empty")
        
        # 相同meta_id下business_code允许相同
        if session.query(MetaDataItem).filter(MetaDataItem.meta_id == item.meta_id, MetaDataItem.business_code == item.business_code).first():
            raise ValueError("Business Code already exists")

        create_common_fields(item)
        session.add(item)
        session.commit()
        return item
    
    @db_session
    def delete_meta_data_item(session, item: MetaDataItem):
        if number_tool.num_is_empty(item.id):
            raise ValueError("Meta Data Item ID cannot be empty")
        session.delete(item.id)
        session.commit()

    @db_session
    def update_meta_data_item(session, item: MetaDataItem):
        if number_tool.num_is_empty(item.id):
            raise ValueError("Meta Data Item ID cannot be empty")
        
        # 根据id查询
        existing_item = session.query(MetaDataItem).filter(MetaDataItem.id == item.id).first()
        if existing_item is None:
            raise ValueError("Meta Data Item not found")
        
        if number_tool.num_is_not_empty(item.meta_id) and existing_item.meta_id != item.meta_id:
            existing_item.meta_id = item.meta_id
        
        if str_tools.str_is_not_empty(item.business_code) and existing_item.business_code != item.business_code:
            existing_item.business_code = item.business_code
        
        # 相同meta_id下除了自己外，business_code不允许相同
        if session.query(MetaDataItem).filter(MetaDataItem.meta_id == item.meta_id, MetaDataItem.business_code == item.business_code).filter(MetaDataItem.id != item.id).first():
            raise ValueError("Business Code already exists")
        
        if str_tools.str_is_not_empty(item.name_en) and existing_item.name_en != item.name_en:
            existing_item.name_en = item.name_en
        
        if str_tools.str_is_not_empty(item.name_cn) and existing_item.name_cn != item.name_cn:
            existing_item.name_cn = item.name_cn
        
        update_common_fields(existing_item)
        session.commit()
        return existing_item
    
    @db_session
    def get_all_meta_data_items_by_meta_id(session, meta_id:int):
        return session.query(MetaDataItem).filter(MetaDataItem.meta_id == meta_id)
    
    @db_session
    def get_meta_data_item_by_meta_id_and_business_code(session, meta_id:int, business_code:str):
        if number_tool.num_is_empty(meta_id):
            raise ValueError("Meta ID cannot be empty")
        if str_tools.str_is_empty(business_code):
            raise ValueError("Business Code cannot be empty")
        return session.query(MetaDataItem).filter(MetaDataItem.meta_id == meta_id, MetaDataItem.business_code == business_code).first()