from dataclasses import dataclass

@dataclass
class MetaDataItemAddReqModel():
    meta_id:int
    business_code:str
    name_en:str
    name_cn:str