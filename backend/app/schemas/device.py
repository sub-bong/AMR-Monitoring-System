from pydantic import BaseModel
from typing import Optional


class DeviceCreate(BaseModel):
    '''
    - name: string
    - map_id: str, default 값=None
    '''
    name: str
    map_id: Optional[str] = None


class DeviceOut(BaseModel):
    '''
    - id: int
    - name: str
    - is_active: bool
    '''
    id: int
    name: str
    is_active: bool


class DeviceKeyOut(BaseModel):
    '''
    - device_id: int
    - device_key: str
    '''
    device_id: int
    device_key: str
