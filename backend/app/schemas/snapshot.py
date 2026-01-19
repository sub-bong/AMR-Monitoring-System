from typing import Optional
from pydantic import BaseModel


class SnapshotCreate(BaseModel):
    '''
    - map_id: string
    - image_url: string
    - pose: dict
    - intrinsics: dict
    - meta: dict, default 값=None
    '''
    map_id: str
    image_url: str
    pose: dict
    intrinsics: dict
    meta: Optional[dict] = None


class SnapshotOut(BaseModel):
    '''
    - id: int
    - map_id: string
    - image_url: string
    - pose: dict
    - intrinsics: dict
    - meta: dict, default 값=None
    '''
    id: int
    map_id: str
    image_url: str
    pose: dict
    intrinsics: dict
    meta: Optional[dict] = None
