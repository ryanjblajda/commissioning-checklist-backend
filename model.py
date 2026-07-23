from pydantic import BaseModel

class NewDevicePayload(BaseModel):
    prefix_id:int
    manufacturer_id:int
    model:str
    capabilities:list[int]
    controls:list[int]

class NewItemPayload(BaseModel):
    id:int
    name:str
    description:str