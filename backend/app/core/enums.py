from enum import Enum

class RoadType(str, Enum):
    motorway = "motorway"
    trunk = "trunk"
    primary = "primary"
    secondary = "secondary"
    tertiary = "tertiary"
    residential = "residential"
    unclassified = "unclassified"
    # Link types (ramps, connectors)
    motorway_link = "motorway_link"
    trunk_link = "trunk_link"
    primary_link = "primary_link"
    secondary_link = "secondary_link"
    tertiary_link = "tertiary_link"
    living_street = "living_street"
    service = "service"
    track = "track"
    road = "road"
    unknown = "unknown"

class IncidentType(str, Enum):
    blocked = "blocked"
    landslide = "landslide"
    flood = "flood"
    bridge_damage = "bridge_damage"
    other = "other"

class IncidentSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class CargoType(str, Enum):
    medicine = "medicine"
    food = "food"
    emergency = "emergency"
    commercial = "commercial"

class ShipmentPriority(str, Enum):
    critical = "critical"
    high = "high"
    normal = "normal"

class ShipmentStatus(str, Enum):
    pending = "pending"
    route_generated = "route_generated"
    in_transit = "in_transit"
    needs_reroute = "needs_reroute"
    completed = "completed"
    cancelled = "cancelled"

class RiskState(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"