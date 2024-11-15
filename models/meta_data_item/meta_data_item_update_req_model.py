from dataclasses import dataclass

@dataclass
class MetaDataItemUpdateReqModel():
    id:int
    meta_id:int
    business_code:str
    name_en:str
    name_cn:str
    is_active:bool