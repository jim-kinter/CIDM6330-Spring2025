from pydantic import BaseModel
from uuid import UUID
from datetime import date
from enum import Enum
from typing import Optional

class Role(str, Enum):
    FOREMAN = "Foreman"
    GENERAL_FOREMAN = "GeneralForeman"
    SUPERINTENDENT = "Superintendent"
    WORKPLACE_PLANNER = "WorkplacePlanner"
    MATERIAL_PLANNER = "MaterialPlanner"
    CONSTRUCTION_MANAGER = "ConstructionManager"

class ShipmentStatus(str, Enum):
    IN_TRANSIT = "InTransit"
    AT_PORT = "AtPort"
    CUSTOMS = "Customs"
    LAYDOWN = "Laydown"
    AVAILABLE = "Available"

class ScheduleStatusEnum(str, Enum):
    AHEAD = "Ahead"
    ON_SCHEDULE = "OnSchedule"
    BEHIND = "Behind"

class User(BaseModel):
    user_id: UUID
    username: str
    role: Role

class Crew(BaseModel):
    crew_id: UUID
    name: str
    project_id: UUID

class Project(BaseModel):
    project_id: UUID
    name: str
    start_date: date
    end_date: date

class PerformanceMetric(BaseModel):
    metric_id: UUID
    crew_id: UUID
    date: date
    productivity: float
    tasks_completed: int
    tasks_total: int
    hours_worked: float

class Activity(BaseModel):
    activity_id: UUID
    project_id: UUID
    description: str
    constraint: str
    start_date: date
    end_date: date

class Shipment(BaseModel):
    shipment_id: UUID
    project_id: UUID
    location: str
    contents: str
    status: ShipmentStatus
    arrival_date: date
    customs_date: date
    laydown_date: date
    available_date: date

class ScheduleStatus(BaseModel):
    status_id: UUID
    project_id: UUID
    phase: str
    status: ScheduleStatusEnum
    last_updated: date

class TimeReport(BaseModel):
    report_id: UUID
    crew_id: UUID
    user_id: UUID
    date: date
    member_name: str
    task: str
    hours: float
    effort_percentage: float