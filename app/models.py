from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
)

from database import Base


class Launch(Base):
    __tablename__ = "launches"
    id = Column(String, primary_key=True)
    details = Column(String)
    launch_date_utc = Column(DateTime(timezone='UTC'))
    launch_success = Column(Boolean, nullable=True)
    upcoming = Column(Boolean)


class Rocket(Base):
    __tablename__ = "rockets",
    id = Column(String, primary_key=True)
    name = Column(String)
    first_flight = Column(Date)
    diameter_unit = Column(String, server_default='feet')
    diameter = Column(Integer)
    launch_payload_mass_unit = Column(String, server_default='lb')
    launch_payload_mass = Column(Integer)


class Mission(Base):
    __tablename__ = "missions",
    id = Column(String, primary_key=True)
    name = Column(String)
    website = Column(String)
    manufactures = Column(String)
    payloads = Column(String)
