1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepo)
8 [requirements.txt](#requirementstxt)

#### `main.py`
```
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport, Role
from repositories.base import UserRepository, CrewRepository, ProjectRepository, PerformanceMetricRepository, ActivityRepository, ShipmentRepository, ScheduleStatusRepository, TimeReportRepository
from repositories.sqlmodel_repo import SQLModelUserRepository, SQLModelCrewRepository, SQLModelProjectRepository, SQLModelPerformanceMetricRepository, SQLModelActivityRepository, SQLModelShipmentRepository, SQLModelScheduleStatusRepository, SQLModelTimeReportRepository
from repositories.csv_repo import CSVUserRepository, CSVCrewRepository, CSVProjectRepository, CSVPerformanceMetricRepository, CSVActivityRepository, CSVShipmentRepository, CSVScheduleStatusRepository, CSVTimeReportRepository
from repositories.in_memory_repo import InMemoryUserRepository, InMemoryCrewRepository, InMemoryProjectRepository, InMemoryPerformanceMetricRepository, InMemoryActivityRepository, InMemoryShipmentRepository, InMemoryScheduleStatusRepository, InMemoryTimeReportRepository
from database import get_db

app = FastAPI(title="Construction Management System API")
repotype =  "SQL"                #"SQL" "CSV" or "MEM"

# Dependencies for repositories
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    match repotype:
        case "SQL":
            return SQLModelUserRepository(db)  
        case "CSV":
            return CSVUserRepository() 
        case "MEM":
            return InMemoryUserRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_crew_repository(db: Session = Depends(get_db)) -> CrewRepository:
    match repotype:
        case "SQL":
            return SQLModelCrewRepository(db)  
        case "CSV":
            return CSVCrewRepository() 
        case "MEM":
            return InMemoryCrewRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    match repotype:
        case "SQL":
            return SQLModelProjectRepository(db)  
        case "CSV":
            return CSVProjectRepository() 
        case "MEM":
            return InMemoryProjectRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_metric_repository(db: Session = Depends(get_db)) -> PerformanceMetricRepository:
    match repotype:
        case "SQL":
            return SQLModelPerformanceMetricRepository(db)  
        case "CSV":
            return CSVPerformanceMetricRepository() 
        case "MEM":
            return InMemoryPerformanceMetricRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")


def get_activity_repository(db: Session = Depends(get_db)) -> ActivityRepository:
    match repotype:
        case "SQL":
            return SQLModelActivityRepository(db)  
        case "CSV":
            return CSVActivityRepository() 
        case "MEM":
            return InMemoryActivityRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_shipment_repository(db: Session = Depends(get_db)) -> ShipmentRepository:
    match repotype:
        case "SQL":
            return SQLModelShipmentRepository(db)  
        case "CSV":
            return CSVShipmentRepository() 
        case "MEM":
            return InMemoryShipmentRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_status_repository(db: Session = Depends(get_db)) -> ScheduleStatusRepository:
    match repotype:
        case "SQL":
            return SQLModelScheduleStatusRepository(db)  
        case "CSV":
            return CSVScheduleStatusRepository() 
        case "MEM":
            return InMemoryScheduleStatusRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

def get_report_repository(db: Session = Depends(get_db)) -> TimeReportRepository:
    match repotype:
        case "SQL":
            return SQLModelTimeReportRepository(db)  
        case "CSV":
            return CSVTimeReportRepository() 
        case "MEM":
            return InMemoryTimeReportRepository()
        case _:
            raise ValueError("Invalid repotype. Use 'SQL', 'CSV', or 'MEM'.")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "API is running"}

# CRUD for User
@app.post("/users/", response_model=User)
async def create_user(user: User, repo: UserRepository = Depends(get_user_repository)):
    return repo.create(user)

@app.get("/users/", response_model=List[User])
async def read_users(repo: UserRepository = Depends(get_user_repository)):
    return repo.get_all()

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: UUID, repo: UserRepository = Depends(get_user_repository)):
    return repo.get_by_id(user_id)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, updated_user: User, repo: UserRepository = Depends(get_user_repository)):
    return repo.update(user_id, updated_user)

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, repo: UserRepository = Depends(get_user_repository)):
    repo.delete(user_id)
    return {"detail": "User deleted"}

# CRUD for Crew
@app.post("/crews/", response_model=Crew)
async def create_crew(crew: Crew, repo: CrewRepository = Depends(get_crew_repository)):
    return repo.create(crew)

@app.get("/crews/", response_model=List[Crew])
async def read_crews(project_id: UUID = None, repo: CrewRepository = Depends(get_crew_repository)):
    return repo.get_all(project_id)

@app.get("/crews/{crew_id}", response_model=Crew)
async def read_crew(crew_id: UUID, repo: CrewRepository = Depends(get_crew_repository)):
    return repo.get_by_id(crew_id)

@app.put("/crews/{crew_id}", response_model=Crew)
async def update_crew(crew_id: UUID, updated_crew: Crew, repo: CrewRepository = Depends(get_crew_repository)):
    return repo.update(crew_id, updated_crew)

@app.delete("/crews/{crew_id}")
async def delete_crew(crew_id: UUID, repo: CrewRepository = Depends(get_crew_repository)):
    repo.delete(crew_id)
    return {"detail": "Crew deleted"}

# CRUD for Project
@app.post("/projects/", response_model=Project)
async def create_project(project: Project, repo: ProjectRepository = Depends(get_project_repository)):
    return repo.create(project)

@app.get("/projects/", response_model=List[Project])
async def read_projects(repo: ProjectRepository = Depends(get_project_repository)):
    return repo.get_all()

@app.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: UUID, repo: ProjectRepository = Depends(get_project_repository)):
    return repo.get_by_id(project_id)

@app.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: UUID, updated_project: Project, repo: ProjectRepository = Depends(get_project_repository)):
    return repo.update(project_id, updated_project)

@app.delete("/projects/{project_id}")
async def delete_project(project_id: UUID, repo: ProjectRepository = Depends(get_project_repository)):
    repo.delete(project_id)
    return {"detail": "Project deleted"}

# CRUD for PerformanceMetric
@app.post("/metrics/", response_model=PerformanceMetric)
async def create_metric(metric: PerformanceMetric, repo: PerformanceMetricRepository = Depends(get_metric_repository)):
    return repo.create(metric)

@app.get("/metrics/", response_model=List[PerformanceMetric])
async def read_metrics(crew_id: UUID, repo: PerformanceMetricRepository = Depends(get_metric_repository)):
    return repo.get_all(crew_id)

@app.get("/metrics/{metric_id}", response_model=PerformanceMetric)
async def read_metric(metric_id: UUID, repo: PerformanceMetricRepository = Depends(get_metric_repository)):
    return repo.get_by_id(metric_id)

@app.put("/metrics/{metric_id}", response_model=PerformanceMetric)
async def update_metric(metric_id: UUID, updated_metric: PerformanceMetric, repo: PerformanceMetricRepository = Depends(get_metric_repository)):
    return repo.update(metric_id, updated_metric)

@app.delete("/metrics/{metric_id}")
async def delete_metric(metric_id: UUID, repo: PerformanceMetricRepository = Depends(get_metric_repository)):
    repo.delete(metric_id)
    return {"detail": "Metric deleted"}

# CRUD for Activity
@app.post("/activities/", response_model=Activity)
async def create_activity(activity: Activity, repo: ActivityRepository = Depends(get_activity_repository)):
    return repo.create(activity)

@app.get("/activities/", response_model=List[Activity])
async def read_activities(project_id: UUID, repo: ActivityRepository = Depends(get_activity_repository)):
    return repo.get_all(project_id)

@app.get("/activities/{activity_id}", response_model=Activity)
async def read_activity(activity_id: UUID, repo: ActivityRepository = Depends(get_activity_repository)):
    return repo.get_by_id(activity_id)

@app.put("/activities/{activity_id}", response_model=Activity)
async def update_activity(activity_id: UUID, updated_activity: Activity, repo: ActivityRepository = Depends(get_activity_repository)):
    return repo.update(activity_id, updated_activity)

@app.delete("/activities/{activity_id}")
async def delete_activity(activity_id: UUID, repo: ActivityRepository = Depends(get_activity_repository)):
    repo.delete(activity_id)
    return {"detail": "Activity deleted"}

# CRUD for Shipment
@app.post("/shipments/", response_model=Shipment)
async def create_shipment(shipment: Shipment, repo: ShipmentRepository = Depends(get_shipment_repository)):
    return repo.create(shipment)

@app.get("/shipments/", response_model=List[Shipment])
async def read_shipments(project_id: UUID, repo: ShipmentRepository = Depends(get_shipment_repository)):
    return repo.get_all(project_id)

@app.get("/shipments/{shipment_id}", response_model=Shipment)
async def read_shipment(shipment_id: UUID, repo: ShipmentRepository = Depends(get_shipment_repository)):
    return repo.get_by_id(shipment_id)

@app.put("/shipments/{shipment_id}", response_model=Shipment)
async def update_shipment(shipment_id: UUID, updated_shipment: Shipment, repo: ShipmentRepository = Depends(get_shipment_repository)):
    return repo.update(shipment_id, updated_shipment)

@app.delete("/shipments/{shipment_id}")
async def delete_shipment(shipment_id: UUID, repo: ShipmentRepository = Depends(get_shipment_repository)):
    repo.delete(shipment_id)
    return {"detail": "Shipment deleted"}

# CRUD for ScheduleStatus
@app.post("/statuses/", response_model=ScheduleStatus)
async def create_status(status: ScheduleStatus, repo: ScheduleStatusRepository = Depends(get_status_repository)):
    return repo.create(status)

@app.get("/statuses/", response_model=List[ScheduleStatus])
async def read_statuses(project_id: UUID, repo: ScheduleStatusRepository = Depends(get_status_repository)):
    return repo.get_all(project_id)

@app.get("/statuses/{status_id}", response_model=ScheduleStatus)
async def read_status(status_id: UUID, repo: ScheduleStatusRepository = Depends(get_status_repository)):
    return repo.get_by_id(status_id)

@app.put("/statuses/{status_id}", response_model=ScheduleStatus)
async def update_status(status_id: UUID, updated_status: ScheduleStatus, repo: ScheduleStatusRepository = Depends(get_status_repository)):
    return repo.update(status_id, updated_status)

@app.delete("/statuses/{status_id}")
async def delete_status(status_id: UUID, repo: ScheduleStatusRepository = Depends(get_status_repository)):
    repo.delete(status_id)
    return {"detail": "Status deleted"}

# CRUD for TimeReport
@app.post("/reports/", response_model=TimeReport)
async def create_report(report: TimeReport, user_id: UUID, repo: TimeReportRepository = Depends(get_report_repository)):
    return repo.create(report, user_id)

@app.get("/reports/", response_model=List[TimeReport])
async def read_reports(crew_id: UUID, repo: TimeReportRepository = Depends(get_report_repository)):
    return repo.get_all(crew_id)

@app.get("/reports/{report_id}", response_model=TimeReport)
async def read_report(report_id: UUID, repo: TimeReportRepository = Depends(get_report_repository)):
    return repo.get_by_id(report_id)

@app.put("/reports/{report_id}", response_model=TimeReport)
async def update_report(report_id: UUID, updated_report: TimeReport, user_id: UUID, repo: TimeReportRepository = Depends(get_report_repository)):
    return repo.update(report_id, updated_report, user_id)

@app.delete("/reports/{report_id}")
async def delete_report(report_id: UUID, repo: TimeReportRepository = Depends(get_report_repository)):
    repo.delete(report_id)
    return {"detail": "Report deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepo)
8 [requirements.txt](#requirementstxt)

#### `models.py`
```
from pydantic import BaseModel
from uuid import UUID
from datetime import date
from enum import Enum

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
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepo)
8 [requirements.txt](#requirementstxt)

#### `database.py`
```
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
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepo)
8 [requirements.txt](#requirementstxt)

#### `base.py`
```
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User:
        pass
    @abstractmethod
    def update(self, user_id: UUID, updated_user: User) -> User:
        pass
    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass

class CrewRepository(ABC):
    @abstractmethod
    def create(self, crew: Crew) -> Crew:
        pass
    @abstractmethod
    def get_all(self, project_id: UUID = None) -> List[Crew]:
        pass
    @abstractmethod
    def get_by_id(self, crew_id: UUID) -> Crew:
        pass
    @abstractmethod
    def update(self, crew_id: UUID, updated_crew: Crew) -> Crew:
        pass
    @abstractmethod
    def delete(self, crew_id: UUID) -> None:
        pass

class ProjectRepository(ABC):
    @abstractmethod
    def create(self, project: Project) -> Project:
        pass
    @abstractmethod
    def get_all(self) -> List[Project]:
        pass
    @abstractmethod
    def get_by_id(self, project_id: UUID) -> Project:
        pass
    @abstractmethod
    def update(self, project_id: UUID, updated_project: Project) -> Project:
        pass
    @abstractmethod
    def delete(self, project_id: UUID) -> None:
        pass

class PerformanceMetricRepository(ABC):
    @abstractmethod
    def create(self, metric: PerformanceMetric) -> PerformanceMetric:
        pass
    @abstractmethod
    def get_all(self, crew_id: UUID) -> List[PerformanceMetric]:
        pass
    @abstractmethod
    def get_by_id(self, metric_id: UUID) -> PerformanceMetric:
        pass
    @abstractmethod
    def update(self, metric_id: UUID, updated_metric: PerformanceMetric) -> PerformanceMetric:
        pass
    @abstractmethod
    def delete(self, metric_id: UUID) -> None:
        pass

class ActivityRepository(ABC):
    @abstractmethod
    def create(self, activity: Activity) -> Activity:
        pass
    @abstractmethod
    def get_all(self, project_id: UUID) -> List[Activity]:
        pass
    @abstractmethod
    def get_by_id(self, activity_id: UUID) -> Activity:
        pass
    @abstractmethod
    def update(self, activity_id: UUID, updated_activity: Activity) -> Activity:
        pass
    @abstractmethod
    def delete(self, activity_id: UUID) -> None:
        pass

class ShipmentRepository(ABC):
    @abstractmethod
    def create(self, shipment: Shipment) -> Shipment:
        pass
    @abstractmethod
    def get_all(self, project_id: UUID) -> List[Shipment]:
        pass
    @abstractmethod
    def get_by_id(self, shipment_id: UUID) -> Shipment:
        pass
    @abstractmethod
    def update(self, shipment_id: UUID, updated_shipment: Shipment) -> Shipment:
        pass
    @abstractmethod
    def delete(self, shipment_id: UUID) -> None:
        pass

class ScheduleStatusRepository(ABC):
    @abstractmethod
    def create(self, status: ScheduleStatus) -> ScheduleStatus:
        pass
    @abstractmethod
    def get_all(self, project_id: UUID) -> List[ScheduleStatus]:
        pass
    @abstractmethod
    def get_by_id(self, status_id: UUID) -> ScheduleStatus:
        pass
    @abstractmethod
    def update(self, status_id: UUID, updated_status: ScheduleStatus) -> ScheduleStatus:
        pass
    @abstractmethod
    def delete(self, status_id: UUID) -> None:
        pass

class TimeReportRepository(ABC):
    @abstractmethod
    def create(self, report: TimeReport, user_id: UUID) -> TimeReport:
        pass
    @abstractmethod
    def get_all(self, crew_id: UUID) -> List[TimeReport]:
        pass
    @abstractmethod
    def get_by_id(self, report_id: UUID) -> TimeReport:
        pass
    @abstractmethod
    def update(self, report_id: UUID, updated_report: TimeReport, user_id: UUID) -> TimeReport:
        pass
    @abstractmethod
    def delete(self, report_id: UUID) -> None:
        pass
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepo)
8 [requirements.txt](#requirementstxt)

#### `csv_repo.py`
```
from datetime import date
import pandas as pd
from uuid import UUID
from typing import List
from models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport, Role, ShipmentStatus, ScheduleStatusEnum
from .base import UserRepository, CrewRepository, ProjectRepository, PerformanceMetricRepository, ActivityRepository, ShipmentRepository, ScheduleStatusRepository, TimeReportRepository
from fastapi import HTTPException
import os

class CSVUserRepository(UserRepository):
    def __init__(self, file_path: str = "data/users.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["user_id", "username", "role"]).to_csv(self.file_path, index=False)

    def create(self, user: User) -> User:
        df = pd.read_csv(self.file_path)
        new_row = {
            "user_id": str(user.user_id),
            "username": user.username,
            "role": user.role.value
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return user

    def get_all(self) -> List[User]:
        df = pd.read_csv(self.file_path)
        return [User(user_id=UUID(row.user_id), username=row.username, role=Role(row.role)) for _, row in df.iterrows()]

    def get_by_id(self, user_id: UUID) -> User:
        df = pd.read_csv(self.file_path)
        user_row = df[df["user_id"] == str(user_id)]
        if user_row.empty:
            raise HTTPException(status_code=404, detail="User not found")
        row = user_row.iloc[0]
        return User(user_id=UUID(row.user_id), username=row.username, role=Role(row.role))

    def update(self, user_id: UUID, updated_user: User) -> User:
        df = pd.read_csv(self.file_path)
        if str(user_id) not in df["user_id"].values:
            raise HTTPException(status_code=404, detail="User not found")
        df.loc[df["user_id"] == str(user_id), ["user_id", "username", "role"]] = [
            str(updated_user.user_id), updated_user.username, updated_user.role.value
        ]
        df.to_csv(self.file_path, index=False)
        return updated_user

    def delete(self, user_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(user_id) not in df["user_id"].values:
            raise HTTPException(status_code=404, detail="User not found")
        df = df[df["user_id"] != str(user_id)]
        df.to_csv(self.file_path, index=False)

class CSVCrewRepository(CrewRepository):
    def __init__(self, file_path: str = "data/crews.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["crew_id", "name", "project_id"]).to_csv(self.file_path, index=False)

    def create(self, crew: Crew) -> Crew:
        df = pd.read_csv(self.file_path)
        new_row = {
            "crew_id": str(crew.crew_id),
            "name": crew.name,
            "project_id": str(crew.project_id)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return crew

    def get_all(self, project_id: UUID = None) -> List[Crew]:
        df = pd.read_csv(self.file_path)
        if project_id:
            df = df[df["project_id"] == str(project_id)]
        return [Crew(crew_id=UUID(row.crew_id), name=row.name, project_id=UUID(row.project_id)) for _, row in df.iterrows()]

    def get_by_id(self, crew_id: UUID) -> Crew:
        df = pd.read_csv(self.file_path)
        crew_row = df[df["crew_id"] == str(crew_id)]
        if crew_row.empty:
            raise HTTPException(status_code=404, detail="Crew not found")
        row = crew_row.iloc[0]
        return Crew(crew_id=UUID(row.crew_id), name=row.name, project_id=UUID(row.project_id))

    def update(self, crew_id: UUID, updated_crew: Crew) -> Crew:
        df = pd.read_csv(self.file_path)
        if str(crew_id) not in df["crew_id"].values:
            raise HTTPException(status_code=404, detail="Crew not found")
        df.loc[df["crew_id"] == str(crew_id), ["crew_id", "name", "project_id"]] = [
            str(updated_crew.crew_id), updated_crew.name, str(updated_crew.project_id)
        ]
        df.to_csv(self.file_path, index=False)
        return updated_crew

    def delete(self, crew_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(crew_id) not in df["crew_id"].values:
            raise HTTPException(status_code=404, detail="Crew not found")
        df = df[df["crew_id"] != str(crew_id)]
        df.to_csv(self.file_path, index=False)

class CSVProjectRepository(ProjectRepository):
    def __init__(self, file_path: str = "data/projects.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["project_id", "name", "start_date", "end_date"]).to_csv(self.file_path, index=False)

    def create(self, project: Project) -> Project:
        df = pd.read_csv(self.file_path)
        new_row = {
            "project_id": str(project.project_id),
            "name": project.name,
            "start_date": project.start_date.isoformat(),
            "end_date": project.end_date.isoformat()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return project

    def get_all(self) -> List[Project]:
        df = pd.read_csv(self.file_path)
        return [Project(
            project_id=UUID(row.project_id),
            name=row.name,
            start_date=date.fromisoformat(row.start_date),
            end_date=date.fromisoformat(row.end_date)
        ) for _, row in df.iterrows()]

    def get_by_id(self, project_id: UUID) -> Project:
        df = pd.read_csv(self.file_path)
        project_row = df[df["project_id"] == str(project_id)]
        if project_row.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        row = project_row.iloc[0]
        return Project(
            project_id=UUID(row.project_id),
            name=row.name,
            start_date=date.fromisoformat(row.start_date),
            end_date=date.fromisoformat(row.end_date)
        )

    def update(self, project_id: UUID, updated_project: Project) -> Project:
        df = pd.read_csv(self.file_path)
        if str(project_id) not in df["project_id"].values:
            raise HTTPException(status_code=404, detail="Project not found")
        df.loc[df["project_id"] == str(project_id), ["project_id", "name", "start_date", "end_date"]] = [
            str(updated_project.project_id),
            updated_project.name,
            updated_project.start_date.isoformat(),
            updated_project.end_date.isoformat()
        ]
        df.to_csv(self.file_path, index=False)
        return updated_project

    def delete(self, project_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(project_id) not in df["project_id"].values:
            raise HTTPException(status_code=404, detail="Project not found")
        df = df[df["project_id"] != str(project_id)]
        df.to_csv(self.file_path, index=False)

class CSVPerformanceMetricRepository(PerformanceMetricRepository):
    def __init__(self, file_path: str = "data/metrics.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["metric_id", "crew_id", "date", "productivity", "tasks_completed", "tasks_total", "hours_worked"]).to_csv(self.file_path, index=False)

    def create(self, metric: PerformanceMetric) -> PerformanceMetric:
        df = pd.read_csv(self.file_path)
        new_row = {
            "metric_id": str(metric.metric_id),
            "crew_id": str(metric.crew_id),
            "date": metric.date.isoformat(),
            "productivity": metric.productivity,
            "tasks_completed": metric.tasks_completed,
            "tasks_total": metric.tasks_total,
            "hours_worked": metric.hours_worked
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return metric

    def get_all(self, crew_id: UUID) -> List[PerformanceMetric]:
        df = pd.read_csv(self.file_path)
        df = df[df["crew_id"] == str(crew_id)]
        return [PerformanceMetric(
            metric_id=UUID(row.metric_id),
            crew_id=UUID(row.crew_id),
            date=date.fromisoformat(row.date),
            productivity=row.productivity,
            tasks_completed=row.tasks_completed,
            tasks_total=row.tasks_total,
            hours_worked=row.hours_worked
        ) for _, row in df.iterrows()]

    def get_by_id(self, metric_id: UUID) -> PerformanceMetric:
        df = pd.read_csv(self.file_path)
        metric_row = df[df["metric_id"] == str(metric_id)]
        if metric_row.empty:
            raise HTTPException(status_code=404, detail="Metric not found")
        row = metric_row.iloc[0]
        return PerformanceMetric(
            metric_id=UUID(row.metric_id),
            crew_id=UUID(row.crew_id),
            date=date.fromisoformat(row.date),
            productivity=row.productivity,
            tasks_completed=row.tasks_completed,
            tasks_total=row.tasks_total,
            hours_worked=row.hours_worked
        )

    def update(self, metric_id: UUID, updated_metric: PerformanceMetric) -> PerformanceMetric:
        df = pd.read_csv(self.file_path)
        if str(metric_id) not in df["metric_id"].values:
            raise HTTPException(status_code=404, detail="Metric not found")
        df.loc[df["metric_id"] == str(metric_id), ["metric_id", "crew_id", "date", "productivity", "tasks_completed", "tasks_total", "hours_worked"]] = [
            str(updated_metric.metric_id),
            str(updated_metric.crew_id),
            updated_metric.date.isoformat(),
            updated_metric.productivity,
            updated_metric.tasks_completed,
            updated_metric.tasks_total,
            updated_metric.hours_worked
        ]
        df.to_csv(self.file_path, index=False)
        return updated_metric

    def delete(self, metric_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(metric_id) not in df["metric_id"].values:
            raise HTTPException(status_code=404, detail="Metric not found")
        df = df[df["metric_id"] != str(metric_id)]
        df.to_csv(self.file_path, index=False)

class CSVActivityRepository(ActivityRepository):
    def __init__(self, file_path: str = "data/activities.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["activity_id", "project_id", "description", "constraint", "start_date", "end_date"]).to_csv(self.file_path, index=False)

    def create(self, activity: Activity) -> Activity:
        df = pd.read_csv(self.file_path)
        new_row = {
            "activity_id": str(activity.activity_id),
            "project_id": str(activity.project_id),
            "description": activity.description,
            "constraint": activity.constraint,
            "start_date": activity.start_date.isoformat(),
            "end_date": activity.end_date.isoformat()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return activity

    def get_all(self, project_id: UUID) -> List[Activity]:
        df = pd.read_csv(self.file_path)
        df = df[df["project_id"] == str(project_id)]
        return [Activity(
            activity_id=UUID(row.activity_id),
            project_id=UUID(row.project_id),
            description=row.description,
            constraint=row.constraint,
            start_date=date.fromisoformat(row.start_date),
            end_date=date.fromisoformat(row.end_date)
        ) for _, row in df.iterrows()]

    def get_by_id(self, activity_id: UUID) -> Activity:
        df = pd.read_csv(self.file_path)
        activity_row = df[df["activity_id"] == str(activity_id)]
        if activity_row.empty:
            raise HTTPException(status_code=404, detail="Activity not found")
        row = activity_row.iloc[0]
        return Activity(
            activity_id=UUID(row.activity_id),
            project_id=UUID(row.project_id),
            description=row.description,
            constraint=row.constraint,
            start_date=date.fromisoformat(row.start_date),
            end_date=date.fromisoformat(row.end_date)
        )

    def update(self, activity_id: UUID, updated_activity: Activity) -> Activity:
        df = pd.read_csv(self.file_path)
        if str(activity_id) not in df["activity_id"].values:
            raise HTTPException(status_code=404, detail="Activity not found")
        df.loc[df["activity_id"] == str(activity_id), ["activity_id", "project_id", "description", "constraint", "start_date", "end_date"]] = [
            str(updated_activity.activity_id),
            str(updated_activity.project_id),
            updated_activity.description,
            updated_activity.constraint,
            updated_activity.start_date.isoformat(),
            updated_activity.end_date.isoformat()
        ]
        df.to_csv(self.file_path, index=False)
        return updated_activity

    def delete(self, activity_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(activity_id) not in df["activity_id"].values:
            raise HTTPException(status_code=404, detail="Activity not found")
        df = df[df["activity_id"] != str(activity_id)]
        df.to_csv(self.file_path, index=False)

class CSVShipmentRepository(ShipmentRepository):
    def __init__(self, file_path: str = "data/shipments.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["shipment_id", "project_id", "location", "contents", "status", "arrival_date", "customs_date", "laydown_date", "available_date"]).to_csv(self.file_path, index=False)

    def create(self, shipment: Shipment) -> Shipment:
        df = pd.read_csv(self.file_path)
        new_row = {
            "shipment_id": str(shipment.shipment_id),
            "project_id": str(shipment.project_id),
            "location": shipment.location,
            "contents": shipment.contents,
            "status": shipment.status.value,
            "arrival_date": shipment.arrival_date.isoformat(),
            "customs_date": shipment.customs_date.isoformat(),
            "laydown_date": shipment.laydown_date.isoformat(),
            "available_date": shipment.available_date.isoformat()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return shipment

    def get_all(self, project_id: UUID) -> List[Shipment]:
        df = pd.read_csv(self.file_path)
        df = df[df["project_id"] == str(project_id)]
        return [Shipment(
            shipment_id=UUID(row.shipment_id),
            project_id=UUID(row.project_id),
            location=row.location,
            contents=row.contents,
            status=ShipmentStatus(row.status),
            arrival_date=date.fromisoformat(row.arrival_date),
            customs_date=date.fromisoformat(row.customs_date),
            laydown_date=date.fromisoformat(row.laydown_date),
            available_date=date.fromisoformat(row.available_date)
        ) for _, row in df.iterrows()]

    def get_by_id(self, shipment_id: UUID) -> Shipment:
        df = pd.read_csv(self.file_path)
        shipment_row = df[df["shipment_id"] == str(shipment_id)]
        if shipment_row.empty:
            raise HTTPException(status_code=404, detail="Shipment not found")
        row = shipment_row.iloc[0]
        return Shipment(
            shipment_id=UUID(row.shipment_id),
            project_id=UUID(row.project_id),
            location=row.location,
            contents=row.contents,
            status=ShipmentStatus(row.status),
            arrival_date=date.fromisoformat(row.arrival_date),
            customs_date=date.fromisoformat(row.customs_date),
            laydown_date=date.fromisoformat(row.laydown_date),
            available_date=date.fromisoformat(row.available_date)
        )

    def update(self, shipment_id: UUID, updated_shipment: Shipment) -> Shipment:
        df = pd.read_csv(self.file_path)
        if str(shipment_id) not in df["shipment_id"].values:
            raise HTTPException(status_code=404, detail="Shipment not found")
        df.loc[df["shipment_id"] == str(shipment_id), ["shipment_id", "project_id", "location", "contents", "status", "arrival_date", "customs_date", "laydown_date", "available_date"]] = [
            str(updated_shipment.shipment_id),
            str(updated_shipment.project_id),
            updated_shipment.location,
            updated_shipment.contents,
            updated_shipment.status.value,
            updated_shipment.arrival_date.isoformat(),
            updated_shipment.customs_date.isoformat(),
            updated_shipment.laydown_date.isoformat(),
            updated_shipment.available_date.isoformat()
        ]
        df.to_csv(self.file_path, index=False)
        return updated_shipment

    def delete(self, shipment_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(shipment_id) not in df["shipment_id"].values:
            raise HTTPException(status_code=404, detail="Shipment not found")
        df = df[df["shipment_id"] != str(shipment_id)]
        df.to_csv(self.file_path, index=False)

class CSVScheduleStatusRepository(ScheduleStatusRepository):
    def __init__(self, file_path: str = "data/statuses.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["status_id", "project_id", "phase", "status", "last_updated"]).to_csv(self.file_path, index=False)

    def create(self, status: ScheduleStatus) -> ScheduleStatus:
        df = pd.read_csv(self.file_path)
        new_row = {
            "status_id": str(status.status_id),
            "project_id": str(status.project_id),
            "phase": status.phase,
            "status": status.status.value,
            "last_updated": status.last_updated.isoformat()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return status

    def get_all(self, project_id: UUID) -> List[ScheduleStatus]:
        df = pd.read_csv(self.file_path)
        df = df[df["project_id"] == str(project_id)]
        return [ScheduleStatus(
            status_id=UUID(row.status_id),
            project_id=UUID(row.project_id),
            phase=row.phase,
            status=ScheduleStatusEnum(row.status),
            last_updated=date.fromisoformat(row.last_updated)
        ) for _, row in df.iterrows()]

    def get_by_id(self, status_id: UUID) -> ScheduleStatus:
        df = pd.read_csv(self.file_path)
        status_row = df[df["status_id"] == str(status_id)]
        if status_row.empty:
            raise HTTPException(status_code=404, detail="Status not found")
        row = status_row.iloc[0]
        return ScheduleStatus(
            status_id=UUID(row.status_id),
            project_id=UUID(row.project_id),
            phase=row.phase,
            status=ScheduleStatusEnum(row.status),
            last_updated=date.fromisoformat(row.last_updated)
        )

    def update(self, status_id: UUID, updated_status: ScheduleStatus) -> ScheduleStatus:
        df = pd.read_csv(self.file_path)
        if str(status_id) not in df["status_id"].values:
            raise HTTPException(status_code=404, detail="Status not found")
        df.loc[df["status_id"] == str(status_id), ["status_id", "project_id", "phase", "status", "last_updated"]] = [
            str(updated_status.status_id),
            str(updated_status.project_id),
            updated_status.phase,
            updated_status.status.value,
            updated_status.last_updated.isoformat()
        ]
        df.to_csv(self.file_path, index=False)
        return updated_status

    def delete(self, status_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(status_id) not in df["status_id"].values:
            raise HTTPException(status_code=404, detail="Status not found")
        df = df[df["status_id"] != str(status_id)]
        df.to_csv(self.file_path, index=False)

class CSVTimeReportRepository(TimeReportRepository):
    def __init__(self, file_path: str = "data/reports.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=["report_id", "crew_id", "user_id", "date", "member_name", "task", "hours", "effort_percentage"]).to_csv(self.file_path, index=False)

    def create(self, report: TimeReport, user_id: UUID) -> TimeReport:
        # Foreman check requires UserRepository; assume external validation
        df = pd.read_csv(self.file_path)
        new_row = {
            "report_id": str(report.report_id),
            "crew_id": str(report.crew_id),
            "user_id": str(report.user_id),
            "date": report.date.isoformat(),
            "member_name": report.member_name,
            "task": report.task,
            "hours": report.hours,
            "effort_percentage": report.effort_percentage
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        return report

    def get_all(self, crew_id: UUID) -> List[TimeReport]:
        df = pd.read_csv(self.file_path)
        df = df[df["crew_id"] == str(crew_id)]
        return [TimeReport(
            report_id=UUID(row.report_id),
            crew_id=UUID(row.crew_id),
            user_id=UUID(row.user_id),
            date=date.fromisoformat(row.date),
            member_name=row.member_name,
            task=row.task,
            hours=row.hours,
            effort_percentage=row.effort_percentage
        ) for _, row in df.iterrows()]

    def get_by_id(self, report_id: UUID) -> TimeReport:
        df = pd.read_csv(self.file_path)
        report_row = df[df["report_id"] == str(report_id)]
        if report_row.empty:
            raise HTTPException(status_code=404, detail="Report not found")
        row = report_row.iloc[0]
        return TimeReport(
            report_id=UUID(row.report_id),
            crew_id=UUID(row.crew_id),
            user_id=UUID(row.user_id),
            date=date.fromisoformat(row.date),
            member_name=row.member_name,
            task=row.task,
            hours=row.hours,
            effort_percentage=row.effort_percentage
        )

    def update(self, report_id: UUID, updated_report: TimeReport, user_id: UUID) -> TimeReport:
        # Foreman check requires UserRepository; assume external validation
        df = pd.read_csv(self.file_path)
        if str(report_id) not in df["report_id"].values:
            raise HTTPException(status_code=404, detail="Report not found")
        df.loc[df["report_id"] == str(report_id), ["report_id", "crew_id", "user_id", "date", "member_name", "task", "hours", "effort_percentage"]] = [
            str(updated_report.report_id),
            str(updated_report.crew_id),
            str(updated_report.user_id),
            updated_report.date.isoformat(),
            updated_report.member_name,
            updated_report.task,
            updated_report.hours,
            updated_report.effort_percentage
        ]
        df.to_csv(self.file_path, index=False)
        return updated_report

    def delete(self, report_id: UUID) -> None:
        df = pd.read_csv(self.file_path)
        if str(report_id) not in df["report_id"].values:
            raise HTTPException(status_code=404, detail="Report not found")
        df = df[df["report_id"] != str(report_id)]
        df.to_csv(self.file_path, index=False)
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepopy)
8 [requirements.txt](#requirementstxt)

#### `in_memory_repo.py`
```
from uuid import UUID
from typing import List
from models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport, Role
from .base import UserRepository, CrewRepository, ProjectRepository, PerformanceMetricRepository, ActivityRepository, ShipmentRepository, ScheduleStatusRepository, TimeReportRepository
from fastapi import HTTPException

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def create(self, user: User) -> User:
        self.users[str(user.user_id)] = user
        return user

    def get_all(self) -> List[User]:
        return list(self.users.values())

    def get_by_id(self, user_id: UUID) -> User:
        user = self.users.get(str(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update(self, user_id: UUID, updated_user: User) -> User:
        if str(user_id) not in self.users:
            raise HTTPException(status_code=404, detail="User not found")
        self.users[str(user_id)] = updated_user
        return updated_user

    def delete(self, user_id: UUID) -> None:
        if str(user_id) not in self.users:
            raise HTTPException(status_code=404, detail="User not found")
        del self.users[str(user_id)]

class InMemoryCrewRepository(CrewRepository):
    def __init__(self):
        self.crews = {}

    def create(self, crew: Crew) -> Crew:
        self.crews[str(crew.crew_id)] = crew
        return crew

    def get_all(self, project_id: UUID = None) -> List[Crew]:
        if project_id:
            return [crew for crew in self.crews.values() if crew.project_id == project_id]
        return list(self.crews.values())

    def get_by_id(self, crew_id: UUID) -> Crew:
        crew = self.crews.get(str(crew_id))
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found")
        return crew

    def update(self, crew_id: UUID, updated_crew: Crew) -> Crew:
        if str(crew_id) not in self.crews:
            raise HTTPException(status_code=404, detail="Crew not found")
        self.crews[str(crew_id)] = updated_crew
        return updated_crew

    def delete(self, crew_id: UUID) -> None:
        if str(crew_id) not in self.crews:
            raise HTTPException(status_code=404, detail="Crew not found")
        del self.crews[str(crew_id)]

class InMemoryProjectRepository(ProjectRepository):
    def __init__(self):
        self.projects = {}

    def create(self, project: Project) -> Project:
        self.projects[str(project.project_id)] = project
        return project

    def get_all(self) -> List[Project]:
        return list(self.projects.values())

    def get_by_id(self, project_id: UUID) -> Project:
        project = self.projects.get(str(project_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def update(self, project_id: UUID, updated_project: Project) -> Project:
        if str(project_id) not in self.projects:
            raise HTTPException(status_code=404, detail="Project not found")
        self.projects[str(project_id)] = updated_project
        return updated_project

    def delete(self, project_id: UUID) -> None:
        if str(project_id) not in self.projects:
            raise HTTPException(status_code=404, detail="Project not found")
        del self.projects[str(project_id)]

class InMemoryPerformanceMetricRepository(PerformanceMetricRepository):
    def __init__(self):
        self.metrics = {}

    def create(self, metric: PerformanceMetric) -> PerformanceMetric:
        self.metrics[str(metric.metric_id)] = metric
        return metric

    def get_all(self, crew_id: UUID) -> List[PerformanceMetric]:
        return [metric for metric in self.metrics.values() if metric.crew_id == crew_id]

    def get_by_id(self, metric_id: UUID) -> PerformanceMetric:
        metric = self.metrics.get(str(metric_id))
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        return metric

    def update(self, metric_id: UUID, updated_metric: PerformanceMetric) -> PerformanceMetric:
        if str(metric_id) not in self.metrics:
            raise HTTPException(status_code=404, detail="Metric not found")
        self.metrics[str(metric_id)] = updated_metric
        return updated_metric

    def delete(self, metric_id: UUID) -> None:
        if str(metric_id) not in self.metrics:
            raise HTTPException(status_code=404, detail="Metric not found")
        del self.metrics[str(metric_id)]

class InMemoryActivityRepository(ActivityRepository):
    def __init__(self):
        self.activities = {}

    def create(self, activity: Activity) -> Activity:
        self.activities[str(activity.activity_id)] = activity
        return activity

    def get_all(self, project_id: UUID) -> List[Activity]:
        return [activity for activity in self.activities.values() if activity.project_id == project_id]

    def get_by_id(self, activity_id: UUID) -> Activity:
        activity = self.activities.get(str(activity_id))
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity

    def update(self, activity_id: UUID, updated_activity: Activity) -> Activity:
        if str(activity_id) not in self.activities:
            raise HTTPException(status_code=404, detail="Activity not found")
        self.activities[str(activity_id)] = updated_activity
        return updated_activity

    def delete(self, activity_id: UUID) -> None:
        if str(activity_id) not in self.activities:
            raise HTTPException(status_code=404, detail="Activity not found")
        del self.activities[str(activity_id)]

class InMemoryShipmentRepository(ShipmentRepository):
    def __init__(self):
        self.shipments = {}

    def create(self, shipment: Shipment) -> Shipment:
        self.shipments[str(shipment.shipment_id)] = shipment
        return shipment

    def get_all(self, project_id: UUID) -> List[Shipment]:
        return [shipment for shipment in self.shipments.values() if shipment.project_id == project_id]

    def get_by_id(self, shipment_id: UUID) -> Shipment:
        shipment = self.shipments.get(str(shipment_id))
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment

    def update(self, shipment_id: UUID, updated_shipment: Shipment) -> Shipment:
        if str(shipment_id) not in self.shipments:
            raise HTTPException(status_code=404, detail="Shipment not found")
        self.shipments[str(shipment_id)] = updated_shipment
        return updated_shipment

    def delete(self, shipment_id: UUID) -> None:
        if str(shipment_id) not in self.shipments:
            raise HTTPException(status_code=404, detail="Shipment not found")
        del self.shipments[str(shipment_id)]

class InMemoryScheduleStatusRepository(ScheduleStatusRepository):
    def __init__(self):
        self.statuses = {}

    def create(self, status: ScheduleStatus) -> ScheduleStatus:
        self.statuses[str(status.status_id)] = status
        return status

    def get_all(self, project_id: UUID) -> List[ScheduleStatus]:
        return [status for status in self.statuses.values() if status.project_id == project_id]

    def get_by_id(self, status_id: UUID) -> ScheduleStatus:
        status = self.statuses.get(str(status_id))
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
        return status

    def update(self, status_id: UUID, updated_status: ScheduleStatus) -> ScheduleStatus:
        if str(status_id) not in self.statuses:
            raise HTTPException(status_code=404, detail="Status not found")
        self.statuses[str(status_id)] = updated_status
        return updated_status

    def delete(self, status_id: UUID) -> None:
        if str(status_id) not in self.statuses:
            raise HTTPException(status_code=404, detail="Status not found")
        del self.statuses[str(status_id)]

class InMemoryTimeReportRepository(TimeReportRepository):
    def __init__(self):
        self.reports = {}

    def create(self, report: TimeReport, user_id: UUID) -> TimeReport:
        # Foreman check requires UserRepository; assume external validation
        self.reports[str(report.report_id)] = report
        return report

    def get_all(self, crew_id: UUID) -> List[TimeReport]:
        return [report for report in self.reports.values() if report.crew_id == crew_id]

    def get_by_id(self, report_id: UUID) -> TimeReport:
        report = self.reports.get(str(report_id))
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

    def update(self, report_id: UUID, updated_report: TimeReport, user_id: UUID) -> TimeReport:
        # Foreman check requires UserRepository; assume external validation
        if str(report_id) not in self.reports:
            raise HTTPException(status_code=404, detail="Report not found")
        self.reports[str(report_id)] = updated_report
        return updated_report

    def delete(self, report_id: UUID) -> None:
        if str(report_id) not in self.reports:
            raise HTTPException(status_code=404, detail="Report not found")
        del self.reports[str(report_id)]
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepopy)
8 [requirements.txt](#requirementstxt)

#### `sqlmodel_repo.py`
```
from sqlmodel import Session, select
from fastapi import HTTPException
from models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport, Role
from database import User as UserModel, Crew as CrewModel, Project as ProjectModel, PerformanceMetric as MetricModel, Activity as ActivityModel, Shipment as ShipmentModel, ScheduleStatus as StatusModel, TimeReport as ReportModel
from .base import UserRepository, CrewRepository, ProjectRepository, PerformanceMetricRepository, ActivityRepository, ShipmentRepository, ScheduleStatusRepository, TimeReportRepository
from uuid import UUID
from typing import List

class SQLModelUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserModel(user_id=str(user.user_id), username=user.username, role=user.role.value)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return user

    def get_all(self) -> List[User]:
        return self.db.exec(select(UserModel)).all()

    def get_by_id(self, user_id: UUID) -> User:
        user = self.db.exec(select(UserModel).where(UserModel.user_id == str(user_id))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update(self, user_id: UUID, updated_user: User) -> User:
        user = self.db.exec(select(UserModel).where(UserModel.user_id == str(user_id))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.user_id = str(updated_user.user_id)
        user.username = updated_user.username
        user.role = updated_user.role.value
        self.db.commit()
        self.db.refresh(user)
        return updated_user

    def delete(self, user_id: UUID) -> None:
        user = self.db.exec(select(UserModel).where(UserModel.user_id == str(user_id))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()

class SQLModelCrewRepository(CrewRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, crew: Crew) -> Crew:
        db_crew = CrewModel(crew_id=str(crew.crew_id), name=crew.name, project_id=str(crew.project_id))
        self.db.add(db_crew)
        self.db.commit()
        self.db.refresh(db_crew)
        return crew

    def get_all(self, project_id: UUID = None) -> List[Crew]:
        query = select(CrewModel)
        if project_id:
            query = query.where(CrewModel.project_id == str(project_id))
        return self.db.exec(query).all()

    def get_by_id(self, crew_id: UUID) -> Crew:
        crew = self.db.exec(select(CrewModel).where(CrewModel.crew_id == str(crew_id))).first()
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found")
        return crew

    def update(self, crew_id: UUID, updated_crew: Crew) -> Crew:
        crew = self.db.exec(select(CrewModel).where(CrewModel.crew_id == str(crew_id))).first()
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found")
        crew.crew_id = str(updated_crew.crew_id)
        crew.name = updated_crew.name
        crew.project_id = str(updated_crew.project_id)
        self.db.commit()
        self.db.refresh(crew)
        return updated_crew

    def delete(self, crew_id: UUID) -> None:
        crew = self.db.exec(select(CrewModel).where(CrewModel.crew_id == str(crew_id))).first()
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found")
        self.db.delete(crew)
        self.db.commit()

class SQLModelProjectRepository(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        db_project = ProjectModel(project_id=str(project.project_id), name=project.name, start_date=project.start_date, end_date=project.end_date)
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return project

    def get_all(self) -> List[Project]:
        return self.db.exec(select(ProjectModel)).all()

    def get_by_id(self, project_id: UUID) -> Project:
        project = self.db.exec(select(ProjectModel).where(ProjectModel.project_id == str(project_id))).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def update(self, project_id: UUID, updated_project: Project) -> Project:
        project = self.db.exec(select(ProjectModel).where(ProjectModel.project_id == str(project_id))).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        project.project_id = str(updated_project.project_id)
        project.name = updated_project.name
        project.start_date = updated_project.start_date
        project.end_date = updated_project.end_date
        self.db.commit()
        self.db.refresh(project)
        return updated_project

    def delete(self, project_id: UUID) -> None:
        project = self.db.exec(select(ProjectModel).where(ProjectModel.project_id == str(project_id))).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        self.db.delete(project)
        self.db.commit()

class SQLModelPerformanceMetricRepository(PerformanceMetricRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, metric: PerformanceMetric) -> PerformanceMetric:
        db_metric = MetricModel(
            metric_id=str(metric.metric_id), crew_id=str(metric.crew_id), date=metric.date,
            productivity=metric.productivity, tasks_completed=metric.tasks_completed,
            tasks_total=metric.tasks_total, hours_worked=metric.hours_worked
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return metric

    def get_all(self, crew_id: UUID) -> List[PerformanceMetric]:
        return self.db.exec(select(MetricModel).where(MetricModel.crew_id == str(crew_id))).all()

    def get_by_id(self, metric_id: UUID) -> PerformanceMetric:
        metric = self.db.exec(select(MetricModel).where(MetricModel.metric_id == str(metric_id))).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        return metric

    def update(self, metric_id: UUID, updated_metric: PerformanceMetric) -> PerformanceMetric:
        metric = self.db.exec(select(MetricModel).where(MetricModel.metric_id == str(metric_id))).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        metric.metric_id = str(updated_metric.metric_id)
        metric.crew_id = str(updated_metric.crew_id)
        metric.date = updated_metric.date
        metric.productivity = updated_metric.productivity
        metric.tasks_completed = updated_metric.tasks_completed
        metric.tasks_total = updated_metric.tasks_total
        metric.hours_worked = updated_metric.hours_worked
        self.db.commit()
        self.db.refresh(metric)
        return updated_metric

    def delete(self, metric_id: UUID) -> None:
        metric = self.db.exec(select(MetricModel).where(MetricModel.metric_id == str(metric_id))).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        self.db.delete(metric)
        self.db.commit()

class SQLModelActivityRepository(ActivityRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, activity: Activity) -> Activity:
        db_activity = ActivityModel(
            activity_id=str(activity.activity_id), project_id=str(activity.project_id),
            description=activity.description, constraint=activity.constraint,
            start_date=activity.start_date, end_date=activity.end_date
        )
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return activity

    def get_all(self, project_id: UUID) -> List[Activity]:
        return self.db.exec(select(ActivityModel).where(ActivityModel.project_id == str(project_id))).all()

    def get_by_id(self, activity_id: UUID) -> Activity:
        activity = self.db.exec(select(ActivityModel).where(ActivityModel.activity_id == str(activity_id))).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity

    def update(self, activity_id: UUID, updated_activity: Activity) -> Activity:
        activity = self.db.exec(select(ActivityModel).where(ActivityModel.activity_id == str(activity_id))).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        activity.activity_id = str(updated_activity.activity_id)
        activity.project_id = str(updated_activity.project_id)
        activity.description = updated_activity.description
        activity.constraint = updated_activity.constraint
        activity.start_date = updated_activity.start_date
        activity.end_date = updated_activity.end_date
        self.db.commit()
        self.db.refresh(activity)
        return updated_activity

    def delete(self, activity_id: UUID) -> None:
        activity = self.db.exec(select(ActivityModel).where(ActivityModel.activity_id == str(activity_id))).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        self.db.delete(activity)
        self.db.commit()

class SQLModelShipmentRepository(ShipmentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, shipment: Shipment) -> Shipment:
        db_shipment = ShipmentModel(
            shipment_id=str(shipment.shipment_id), project_id=str(shipment.project_id),
            location=shipment.location, contents=shipment.contents, status=shipment.status.value,
            arrival_date=shipment.arrival_date, customs_date=shipment.customs_date,
            laydown_date=shipment.laydown_date, available_date=shipment.available_date
        )
        self.db.add(db_shipment)
        self.db.commit()
        self.db.refresh(db_shipment)
        return shipment

    def get_all(self, project_id: UUID) -> List[Shipment]:
        return self.db.exec(select(ShipmentModel).where(ShipmentModel.project_id == str(project_id))).all()

    def get_by_id(self, shipment_id: UUID) -> Shipment:
        shipment = self.db.exec(select(ShipmentModel).where(ShipmentModel.shipment_id == str(shipment_id))).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment

    def update(self, shipment_id: UUID, updated_shipment: Shipment) -> Shipment:
        shipment = self.db.exec(select(ShipmentModel).where(ShipmentModel.shipment_id == str(shipment_id))).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        shipment.shipment_id = str(updated_shipment.shipment_id)
        shipment.project_id = str(updated_shipment.project_id)
        shipment.location = updated_shipment.location
        shipment.contents = updated_shipment.contents
        shipment.status = updated_shipment.status.value
        shipment.arrival_date = updated_shipment.arrival_date
        shipment.customs_date = updated_shipment.customs_date
        shipment.laydown_date = updated_shipment.laydown_date
        shipment.available_date = updated_shipment.available_date
        self.db.commit()
        self.db.refresh(shipment)
        return updated_shipment

    def delete(self, shipment_id: UUID) -> None:
        shipment = self.db.exec(select(ShipmentModel).where(ShipmentModel.shipment_id == str(shipment_id))).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        self.db.delete(shipment)
        self.db.commit()

class SQLModelScheduleStatusRepository(ScheduleStatusRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, status: ScheduleStatus) -> ScheduleStatus:
        db_status = StatusModel(
            status_id=str(status.status_id), project_id=str(status.project_id),
            phase=status.phase, status=status.status.value, last_updated=status.last_updated
        )
        self.db.add(db_status)
        self.db.commit()
        self.db.refresh(db_status)
        return status

    def get_all(self, project_id: UUID) -> List[ScheduleStatus]:
        return self.db.exec(select(StatusModel).where(StatusModel.project_id == str(project_id))).all()

    def get_by_id(self, status_id: UUID) -> ScheduleStatus:
        status = self.db.exec(select(StatusModel).where(StatusModel.status_id == str(status_id))).first()
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
        return status

    def update(self, status_id: UUID, updated_status: ScheduleStatus) -> ScheduleStatus:
        status = self.db.exec(select(StatusModel).where(StatusModel.status_id == str(status_id))).first()
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
        status.status_id = str(updated_status.status_id)
        status.project_id = str(updated_status.project_id)
        status.phase = updated_status.phase
        status.status = updated_status.status.value
        status.last_updated = updated_status.last_updated
        self.db.commit()
        self.db.refresh(status)
        return updated_status

    def delete(self, status_id: UUID) -> None:
        status = self.db.exec(select(StatusModel).where(StatusModel.status_id == str(status_id))).first()
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
        self.db.delete(status)
        self.db.commit()

class SQLModelTimeReportRepository(TimeReportRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, report: TimeReport, user_id: UUID) -> TimeReport:
        user = self.db.exec(select(UserModel).where(UserModel.user_id == str(user_id))).first()
        if not user or user.role != Role.FOREMAN.value:
            raise HTTPException(status_code=403, detail="Only Foremen can submit time reports")
        db_report = ReportModel(
            report_id=str(report.report_id), crew_id=str(report.crew_id), user_id=str(report.user_id),
            date=report.date, member_name=report.member_name, task=report.task,
            hours=report.hours, effort_percentage=report.effort_percentage
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return report

    def get_all(self, crew_id: UUID) -> List[TimeReport]:
        return self.db.exec(select(ReportModel).where(ReportModel.crew_id == str(crew_id))).all()

    def get_by_id(self, report_id: UUID) -> TimeReport:
        report = self.db.exec(select(ReportModel).where(ReportModel.report_id == str(report_id))).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

    def update(self, report_id: UUID, updated_report: TimeReport, user_id: UUID) -> TimeReport:
        report = self.db.exec(select(ReportModel).where(ReportModel.report_id == str(report_id))).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        user = self.db.exec(select(UserModel).where(UserModel.user_id == str(user_id))).first()
        if not user or user.role != Role.FOREMAN.value:
            raise HTTPException(status_code=403, detail="Only Foremen can update time reports")
        report.report_id = str(updated_report.report_id)
        report.crew_id = str(updated_report.crew_id)
        report.user_id = str(updated_report.user_id)
        report.date = updated_report.date
        report.member_name = updated_report.member_name
        report.task = updated_report.task
        report.hours = updated_report.hours
        report.effort_percentage = updated_report.effort_percentage
        self.db.commit()
        self.db.refresh(report)
        return updated_report

    def delete(self, report_id: UUID) -> None:
        report = self.db.exec(select(ReportModel).where(ReportModel.report_id == str(report_id))).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        self.db.delete(report)
        self.db.commit()
```

1 [main.py](#mainpy)
2 [model.py](#modelspy)
3 [database.py](#databasepy)
4 [base.py](#basepy)
5 [csv_repo.py](#csvrepopy)
6 [in_memory_repo.py](#inmemoryrepopy)
7 [sqlmodel_repo.py](#sqlmodelrepopy)
8 [requirements.txt](#requirementstxt)

#### `requirements.txt`
```
annotated-types==0.7.0
anyio==4.9.0
click==8.1.8
colorama==0.4.6
fastapi==0.115.12
greenlet==3.2.0
h11==0.14.0
idna==3.10
numpy==2.2.4
pandas==2.2.3
pydantic==2.11.3
pydantic_core==2.33.1
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.40
sqlmodel==0.0.24
starlette==0.46.2
typing-inspection==0.4.0
typing_extensions==4.13.2
tzdata==2025.2
uvicorn==0.34.1
```
