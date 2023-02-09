from enum import Enum


class LaunchOrderEnum(str, Enum):
    id = "id"
    launch_date_utc = "launch_date_utc"


class RocketOrderEnum(str, Enum):
    id = "id"
    name = "name"
    first_flight = "first_flight"
    # TODO: for realization need compare values in different units
    # diameter = "diameter"
    # launch_payload_mass = "launch_payload_mass"


class MissionOrderEnum(str, Enum):
    id = "id"
    name = "name"
    manufactures = "manufactures"
    payloads = "payloads"
