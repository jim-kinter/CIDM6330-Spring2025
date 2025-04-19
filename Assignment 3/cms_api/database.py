from datetime import date
from sqlmodel import SQLModel, create_engine, Session, Field, Enum
from enum import Enum as PyEnum
from typing import Optional

# SQLite database
DATABASE_URL = "sqlite:///cms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Enums
class Role(PyEnum):
    FOREMAN = "Foreman"
    GENERAL_FOREMAN = "GeneralForeman"
    SUPERINTENDENT = "Superintendent"
    WORKPLACE_PLANNER = "WorkplacePlanner"
    MATERIAL_PLANNER = "MaterialPlanner"
    CONSTRUCTION_MANAGER = "ConstructionManager"

class ShipmentStatus(PyEnum):
    IN_TRANSIT = "InTransit"
    AT_PORT = "AtPort"
    CUSTOMS = "Customs"
    LAYDOWN = "Laydown"
    AVAILABLE = "Available"

class ScheduleStatusEnum(PyEnum):
    AHEAD = "Ahead"
    ON_SCHEDULE = "OnSchedule"
    BEHIND = "Behind"

# SQLModel Classes
class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    username: str
    role: Role = Field(sa_type=Enum(Role, values_callable=lambda x: [e.value for e in x]))

class Crew(SQLModel, table=True):
    crew_id: str = Field(primary_key=True)
    name: str
    project_id: str = Field(foreign_key="project.project_id")

class Project(SQLModel, table=True):
    project_id: str = Field(primary_key=True)
    name: str
    start_date: date
    end_date: date

class PerformanceMetric(SQLModel, table=True):
    metric_id: str = Field(primary_key=True)
    crew_id: str = Field(foreign_key="crew.crew_id")
    date: date
    productivity: float
    tasks_completed: int
    tasks_total: int
    hours_worked: float

class Activity(SQLModel, table=True):
    activity_id: str = Field(primary_key=True)
    project_id: str = Field(foreign_key="project.project_id")
    description: str
    constraint: str
    start_date: date
    end_date: date

class Shipment(SQLModel, table=True):
    shipment_id: str = Field(primary_key=True)
    project_id: str = Field(foreign_key="project.project_id")
    location: str
    contents: str
    status: ShipmentStatus = Field(sa_type=Enum(ShipmentStatus, values_callable=lambda x: [e.value for e in x]))
    arrival_date: date
    customs_date: date
    laydown_date: date
    available_date: date

class ScheduleStatus(SQLModel, table=True):
    status_id: str = Field(primary_key=True)
    project_id: str = Field(foreign_key="project.project_id")
    phase: str
    status: ScheduleStatusEnum = Field(sa_type=Enum(ScheduleStatusEnum, values_callable=lambda x: [e.value for e in x]))
    last_updated: date

class TimeReport(SQLModel, table=True):
    report_id: str = Field(primary_key=True)
    crew_id: str = Field(foreign_key="crew.crew_id")
    user_id: str = Field(foreign_key="user.user_id")
    date: date
    member_name: str
    task: str
    hours: float
    effort_percentage: float

# Create tables
SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session