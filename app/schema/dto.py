from datetime import date, datetime

from pydantic import BaseModel
from pydantic.schema import Optional


class Launch(BaseModel):
    id: str
    details: Optional[str]
    launch_date_utc: datetime
    launch_date_success: Optional[bool]
    upcoming: bool

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


class Mission(BaseModel):
    id: str
    name: str
    website: str
    manufactures: str
    payloads: str
