from dataclasses import dataclass

@dataclass
class MetaDataUpdateReqModel():
    id:int
    name:str
    code:str
    description:str
    is_active:bool