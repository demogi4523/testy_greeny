from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
)


def get_launches(metadata):
    launches = Table(
        "launches",
        metadata,
        Column("id", String, primary_key=True),
        Column("details", String),
        Column("launch_date_utc", DateTime(timezone='UTC')),
        Column("launch_success", Boolean, nullable=True),
        Column("upcoming", Boolean),
    )
    return launches


def get_rockets(metadata):
    rockets = Table(
        "rockets",
        metadata,
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("first_flight", Date),
        Column("diameter_unit", String, server_default='feet'),
        Column("diameter", Integer),
        Column("launch_payload_mass_unit", String, server_default='lb'),
        Column("launch_payload_mass", Integer),
    )
    return rockets


def get_missions(metadata):
    missions = Table(
        "missions",
        metadata,
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("website", String),
        Column("manufactures", String),
        Column("payloads", String),
    )
    return missions
