from sqlalchemy import create_engine, Column, String, Float, Integer, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

# SQLite database
DATABASE_URL = "sqlite:///cms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class Role(enum.Enum):
    FOREMAN = "Foreman"
    GENERAL_FOREMAN = "GeneralForeman"
    SUPERINTENDENT = "Superintendent"
    WORKPLACE_PLANNER = "WorkplacePlanner"
    MATERIAL_PLANNER = "MaterialPlanner"
    CONSTRUCTION_MANAGER = "ConstructionManager"

class ShipmentStatus(enum.Enum):
    IN_TRANSIT = "InTransit"
    AT_PORT = "AtPort"
    CUSTOMS = "Customs"
    LAYDOWN = "Laydown"
    AVAILABLE = "Available"

class ScheduleStatusEnum(enum.Enum):
    AHEAD = "Ahead"
    ON_SCHEDULE = "OnSchedule"
    BEHIND = "Behind"

# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)  # Store UUID as string
    username = Column(String, nullable=False)
    role = Column(Enum(Role, values_callable=lambda x: [e.value for e in x]), nullable=False)

class Crew(Base):
    __tablename__ = "crews"
    crew_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=False)

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

class PerformanceMetric(Base):
    __tablename__ = "metrics"
    metric_id = Column(String, primary_key=True)
    crew_id = Column(String, ForeignKey("crews.crew_id"), nullable=False)
    date = Column(Date, nullable=False)
    productivity = Column(Float, nullable=False)
    tasks_completed = Column(Integer, nullable=False)
    tasks_total = Column(Integer, nullable=False)
    hours_worked = Column(Float, nullable=False)

class Activity(Base):
    __tablename__ = "activities"
    activity_id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=False)
    description = Column(String, nullable=False)
    constraint = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

class Shipment(Base):
    __tablename__ = "shipments"
    shipment_id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=False)
    location = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    status = Column(Enum(ShipmentStatus, values_callable=lambda x: [e.value for e in x]), nullable=False)
    arrival_date = Column(Date, nullable=False)
    customs_date = Column(Date, nullable=False)
    laydown_date = Column(Date, nullable=False)
    available_date = Column(Date, nullable=False)

class ScheduleStatus(Base):
    __tablename__ = "statuses"
    status_id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=False)
    phase = Column(String, nullable=False)
    status = Column(Enum(ScheduleStatusEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    last_updated = Column(Date, nullable=False)

class TimeReport(Base):
    __tablename__ = "reports"
    report_id = Column(String, primary_key=True)
    crew_id = Column(String, ForeignKey("crews.crew_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    date = Column(Date, nullable=False)
    member_name = Column(String, nullable=False)
    task = Column(String, nullable=False)
    hours = Column(Float, nullable=False)
    effort_percentage = Column(Float, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()