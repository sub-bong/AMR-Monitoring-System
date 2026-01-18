from pydantic import BaseModel
from typing import Optional, Literal


class Pose(BaseModel):
    frame: Literal["map"] = "map"
    x: float
    y: float
    yaw: float


class GPS(BaseModel):
    lat: float
    lon: float
    accuracy_m: Optional[float] = None


class State(BaseModel):
    battery_pct: Optional[int] = None
    mode: Optional[str] = None
    health: Optional[str] = None
    speed_mps: Optional[float] = None


class TelemetryIn(BaseModel):
    type: Literal["telemetry"] = "telemetry"
    map_id: str
    amr_id: str
    ts: Optional[int] = None
    pose: Pose
    gps: Optional[GPS] = None
    state: Optional[State] = None
