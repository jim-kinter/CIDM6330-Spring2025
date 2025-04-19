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