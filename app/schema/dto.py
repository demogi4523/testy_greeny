from datetime import date, datetime

from pydantic import BaseModel
from pydantic.schema import Optional


class Launch(BaseModel):
    id: str
    details: Optional[str]
    launch_date_utc: datetime
    launch_date_success: Optional[bool]
    upcoming: bool
    mission_id: Optional[str]
    # rocket_name: Optional[str]
    # rocket_type: Optional[str]
    rocket_id : str

    class Config:
        orm_mode = True


class Rocket(BaseModel):
    id: str
    name: str
    first_flight: date
    diameter: int
    diameter_unit: str
    launch_payload_mass: int
    launch_payload_mass_unit: str

    class Config:
        orm_mode = True


class Mission(BaseModel):
    id: str
    name: str
    website: str
    manufactures: str
    payloads: str

    class Config:
        orm_mode = True
