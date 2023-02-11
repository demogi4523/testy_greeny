from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
)
from sqlalchemy.orm import relationship

from database import Base

class Rocket(Base):
    __tablename__ = "rockets"

    id = Column(String, primary_key=True)
    name = Column(String)
    first_flight = Column(Date)
    diameter_unit = Column(String, server_default='feet')
    diameter = Column(Integer)
    launch_payload_mass_unit = Column(String, server_default='lb')
    launch_payload_mass = Column(Integer)

    # launches = relationship("Launch",
    #     back_populates="rocket",
    #     # cascade="all, delete-orphan",
    # )

class Launch(Base):
    __tablename__ = "launches"

    id = Column(String, primary_key=True)
    details = Column(String)
    launch_date_utc = Column(DateTime(timezone='UTC'))
    launch_success = Column(Boolean, nullable=True)
    upcoming = Column(Boolean)

    rocket_id = Column(String)
    # rocket_id = Column(String,
    #     ForeignKey('rockets.id'),
    #     nullable=True,
    # )
    # rocket = relationship("Rocket", back_populates="launches")

    mission_id = Column(String)
    # mission = relationship("Rocket", back_populates="launches")


class Mission(Base):
    __tablename__ = "missions",
    id = Column(String, primary_key=True)
    name = Column(String)
    website = Column(String)
    manufactures = Column(String)
    payloads = Column(String)
