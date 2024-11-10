from dataclasses import dataclass

@dataclass
class SiteUpdateReqModel():
    site_id:int
    site_name:str
    site_description:str
    is_active:bool