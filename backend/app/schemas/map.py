from typing import Any, List, Optional
from pydantic import BaseModel


class Point2D(BaseModel):
    '''
    - x: float
    - y: float
    '''
    x: float
    y: float


class MapCreate(BaseModel):
    '''
    - map_id: string
    - name: string
    - polygon: list[Point2D]
    - meta: dict[str, Any], default 값=None
    '''
    map_id: str
    name: str
    polygon: List[Point2D]
    meta: Optional[dict[str, Any]] = None


class MapOut(BaseModel):
    '''
    - map_id: string
    - name: string
    - polygon: list[Point2D]
    - meta: dict[str, Any], default 값=None
    '''
    map_id: str
    name: str
    polygon: List[Point2D]
    meta: Optional[dict[str, Any]] = None
