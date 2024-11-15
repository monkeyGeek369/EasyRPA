from models.meta_data.meta_data_detail_model import MetaDataDetailModel
from models.meta_data_item.meta_data_item_detail_model import MetaDataItemDetailModel
from database.models import MetaData,MetaDataItem
from copy import deepcopy

def metaData2MetaDataDetailModel(meta_data:MetaData) -> MetaDataDetailModel:
    # copy
    detail = MetaDataDetailModel(
        id=meta_data.id,
        name=meta_data.name,
        code=meta_data.code,
        description=meta_data.description,
        created_id=meta_data.created_id,
        created_time=meta_data.created_time,
        modify_id=meta_data.modify_id,
        modify_time=meta_data.modify_time,
        trace_id=meta_data.trace_id,
        is_active=meta_data.is_active
    )

    return detail

def metaData2MetaDataDetailModels(meta_datas:list[MetaData]) -> list[MetaDataDetailModel]:
    return [metaData2MetaDataDetailModel(item) for item in meta_datas]

def metaDataItem2MetaDataItemDetailModel(item:MetaDataItem) -> MetaDataItemDetailModel:
    # copy
    detail = MetaDataItemDetailModel(
        id=item.id,
        meta_id=item.meta_id,
        business_code=item.business_code,
        name_en=item.name_en,
        name_cn=item.name_cn,
        created_id=item.created_id,
        created_time=item.created_time,
        modify_id=item.modify_id,
        modify_time=item.modify_time,
        trace_id=item.trace_id,
        is_active=item.is_active
    )

    return detail

def metaDataItems2MetaDataItemDetailModels(items:list[MetaDataItem]) -> list[MetaDataItemDetailModel]:
    return [metaDataItem2MetaDataItemDetailModel(item) for item in items]