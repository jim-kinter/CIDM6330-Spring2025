![ERD](./artifacts/CMS_ERD.png)
[VIEW ERD FILE](./artifacts/CMS_ERD.pdf)

```
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from models import (
    User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport,
    Role, ShipmentStatus, ScheduleStatusEnum
)
from database import (
    User as UserModel, Crew as CrewModel, Project as ProjectModel, PerformanceMetric as MetricModel,
    Activity as ActivityModel, Shipment as ShipmentModel, ScheduleStatus as StatusModel,
    TimeReport as ReportModel, get_db
)

import database

app = FastAPI(title="Construction Management System API", description="API for managing construction project data")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "API is running"}

# CRUD for User
@app.post("/users/", response_model=User)
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(user_id=str(user.user_id), username=user.username, role=user.role.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

@app.get("/users/", response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, updated_user: User, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.user_id = str(updated_user.user_id)
    user.username = updated_user.username
    user.role = updated_user.role.value
    db.commit()
    db.refresh(user)
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# CRUD for Crew
@app.post("/crews/", response_model=Crew)
async def create_crew(crew: Crew, db: Session = Depends(get_db)):
    db_crew = CrewModel(crew_id=str(crew.crew_id), name=crew.name, project_id=str(crew.project_id))
    db.add(db_crew)
    db.commit()
    db.refresh(db_crew)
    return crew

@app.get("/crews/", response_model=List[Crew])
async def read_crews(project_id: UUID = None, db: Session = Depends(get_db)):
    query = db.query(CrewModel)
    if project_id:
        query = query.filter(CrewModel.project_id == str(project_id))
    return query.all()

@app.get("/crews/{crew_id}", response_model=Crew)
async def read_crew(crew_id: UUID, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.crew_id == str(crew_id)).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    return crew

@app.put("/crews/{crew_id}", response_model=Crew)
async def update_crew(crew_id: UUID, updated_crew: Crew, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.crew_id == str(crew_id)).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    crew.crew_id = str(updated_crew.crew_id)
    crew.name = updated_crew.name
    crew.project_id = str(updated_crew.project_id)
    db.commit()
    db.refresh(crew)
    return updated_crew

@app.delete("/crews/{crew_id}")
async def delete_crew(crew_id: UUID, db: Session = Depends(get_db)):
    crew = db.query(CrewModel).filter(CrewModel.crew_id == str(crew_id)).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    db.delete(crew)
    db.commit()
    return {"detail": "Crew deleted"}

# CRUD for Project
@app.post("/projects/", response_model=Project)
async def create_project(project: Project, db: Session = Depends(get_db)):
    db_project = ProjectModel(project_id=str(project.project_id), name=project.name, start_date=project.start_date, end_date=project.end_date)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return project

@app.get("/projects/", response_model=List[Project])
async def read_projects(db: Session = Depends(get_db)):
    return db.query(ProjectModel).all()

@app.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.project_id == str(project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: UUID, updated_project: Project, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.project_id == str(project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.project_id = str(updated_project.project_id)
    project.name = updated_project.name
    project.start_date = updated_project.start_date
    project.end_date = updated_project.end_date
    db.commit()
    db.refresh(project)
    return updated_project

@app.delete("/projects/{project_id}")
async def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.project_id == str(project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted"}

# CRUD for PerformanceMetric
@app.post("/metrics/", response_model=PerformanceMetric)
async def create_metric(metric: PerformanceMetric, db: Session = Depends(get_db)):
    db_metric = MetricModel(
        metric_id=str(metric.metric_id), crew_id=str(metric.crew_id), date=metric.date,
        productivity=metric.productivity, tasks_completed=metric.tasks_completed,
        tasks_total=metric.tasks_total, hours_worked=metric.hours_worked
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return metric

@app.get("/metrics/", response_model=List[PerformanceMetric])
async def read_metrics(crew_id: UUID, db: Session = Depends(get_db)):
    metrics = db.query(MetricModel).filter(MetricModel.crew_id == str(crew_id)).all()
    return metrics

@app.get("/metrics/{metric_id}", response_model=PerformanceMetric)
async def read_metric(metric_id: UUID, db: Session = Depends(get_db)):
    metric = db.query(MetricModel).filter(MetricModel.metric_id == str(metric_id)).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@app.put("/metrics/{metric_id}", response_model=PerformanceMetric)
async def update_metric(metric_id: UUID, updated_metric: PerformanceMetric, db: Session = Depends(get_db)):
    metric = db.query(MetricModel).filter(MetricModel.metric_id == str(metric_id)).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    metric.metric_id = str(updated_metric.metric_id)
    metric.crew_id = str(updated_metric.crew_id)
    metric.date = updated_metric.date
    metric.productivity = updated_metric.productivity
    metric.tasks_completed = updated_metric.tasks_completed
    metric.tasks_total = updated_metric.tasks_total
    metric.hours_worked = updated_metric.hours_worked
    db.commit()
    db.refresh(metric)
    return updated_metric

@app.delete("/metrics/{metric_id}")
async def delete_metric(metric_id: UUID, db: Session = Depends(get_db)):
    metric = db.query(MetricModel).filter(MetricModel.metric_id == str(metric_id)).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    return {"detail": "Metric deleted"}

# CRUD for Activity
@app.post("/activities/", response_model=Activity)
async def create_activity(activity: Activity, db: Session = Depends(get_db)):
    db_activity = ActivityModel(
        activity_id=str(activity.activity_id), project_id=str(activity.project_id),
        description=activity.description, constraint=activity.constraint,
        start_date=activity.start_date, end_date=activity.end_date
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return activity

@app.get("/activities/", response_model=List[Activity])
async def read_activities(project_id: UUID, db: Session = Depends(get_db)):
    activities = db.query(ActivityModel).filter(ActivityModel.project_id == str(project_id)).all()
    return activities

@app.get("/activities/{activity_id}", response_model=Activity)
async def read_activity(activity_id: UUID, db: Session = Depends(get_db)):
    activity = db.query(ActivityModel).filter(ActivityModel.activity_id == str(activity_id)).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.put("/activities/{activity_id}", response_model=Activity)
async def update_activity(activity_id: UUID, updated_activity: Activity, db: Session = Depends(get_db)):
    activity = db.query(ActivityModel).filter(ActivityModel.activity_id == str(activity_id)).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity.activity_id = str(updated_activity.activity_id)
    activity.project_id = str(updated_activity.project_id)
    activity.description = updated_activity.description
    activity.constraint = updated_activity.constraint
    activity.start_date = updated_activity.start_date
    activity.end_date = updated_activity.end_date
    db.commit()
    db.refresh(activity)
    return updated_activity

@app.delete("/activities/{activity_id}")
async def delete_activity(activity_id: UUID, db: Session = Depends(get_db)):
    activity = db.query(ActivityModel).filter(ActivityModel.activity_id == str(activity_id)).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"detail": "Activity deleted"}

# CRUD for Shipment
@app.post("/shipments/", response_model=Shipment)
async def create_shipment(shipment: Shipment, db: Session = Depends(get_db)):
    db_shipment = ShipmentModel(
        shipment_id=str(shipment.shipment_id), project_id=str(shipment.project_id),
        location=shipment.location, contents=shipment.contents, status=shipment.status.value,
        arrival_date=shipment.arrival_date, customs_date=shipment.customs_date,
        laydown_date=shipment.laydown_date, available_date=shipment.available_date
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return shipment

@app.get("/shipments/", response_model=List[Shipment])
async def read_shipments(project_id: UUID, db: Session = Depends(get_db)):
    shipments = db.query(ShipmentModel).filter(ShipmentModel.project_id == str(project_id)).all()
    return shipments

@app.get("/shipments/{shipment_id}", response_model=Shipment)
async def read_shipment(shipment_id: UUID, db: Session = Depends(get_db)):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.shipment_id == str(shipment_id)).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@app.put("/shipments/{shipment_id}", response_model=Shipment)
async def update_shipment(shipment_id: UUID, updated_shipment: Shipment, db: Session = Depends(get_db)):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.shipment_id == str(shipment_id)).first()
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
    db.commit()
    db.refresh(shipment)
    return updated_shipment

@app.delete("/shipments/{shipment_id}")
async def delete_shipment(shipment_id: UUID, db: Session = Depends(get_db)):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.shipment_id == str(shipment_id)).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(shipment)
    db.commit()
    return {"detail": "Shipment deleted"}

# CRUD for ScheduleStatus
@app.post("/statuses/", response_model=ScheduleStatus)
async def create_status(status: ScheduleStatus, db: Session = Depends(get_db)):
    db_status = StatusModel(
        status_id=str(status.status_id), project_id=str(status.project_id),
        phase=status.phase, status=status.status.value, last_updated=status.last_updated
    )
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return status

@app.get("/statuses/", response_model=List[ScheduleStatus])
async def read_statuses(project_id: UUID, db: Session = Depends(get_db)):
    statuses = db.query(StatusModel).filter(StatusModel.project_id == str(project_id)).all()
    return statuses

@app.get("/statuses/{status_id}", response_model=ScheduleStatus)
async def read_status(status_id: UUID, db: Session = Depends(get_db)):
    status = db.query(StatusModel).filter(StatusModel.status_id == str(status_id)).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

@app.put("/statuses/{status_id}", response_model=ScheduleStatus)
async def update_status(status_id: UUID, updated_status: ScheduleStatus, db: Session = Depends(get_db)):
    status = db.query(StatusModel).filter(StatusModel.status_id == str(status_id)).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    status.status_id = str(updated_status.status_id)
    status.project_id = str(updated_status.project_id)
    status.phase = updated_status.phase
    status.status = updated_status.status.value
    status.last_updated = updated_status.last_updated
    db.commit()
    db.refresh(status)
    return updated_status

@app.delete("/statuses/{status_id}")
async def delete_status(status_id: UUID, db: Session = Depends(get_db)):
    status = db.query(StatusModel).filter(StatusModel.status_id == str(status_id)).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(status)
    db.commit()
    return {"detail": "Status deleted"}

# CRUD for TimeReport
@app.post("/reports/", response_model=TimeReport)
async def create_report(report: TimeReport, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == str(report.user_id)).first()
    if not user or user.role != Role.FOREMAN.value:
        raise HTTPException(status_code=403, detail="Only Foremen can submit time reports")
    db_report = ReportModel(
        report_id=str(report.report_id), crew_id=str(report.crew_id), user_id=str(report.user_id),
        date=report.date, member_name=report.member_name, task=report.task,
        hours=report.hours, effort_percentage=report.effort_percentage
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return report

@app.get("/reports/", response_model=List[TimeReport])
async def read_reports(crew_id: UUID, db: Session = Depends(get_db)):
    reports = db.query(ReportModel).filter(ReportModel.crew_id == str(crew_id)).all()
    return reports

@app.get("/reports/{report_id}", response_model=TimeReport)
async def read_report(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(ReportModel).filter(ReportModel.report_id == str(report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.put("/reports/{report_id}", response_model=TimeReport)
async def update_report(report_id: UUID, updated_report: TimeReport, db: Session = Depends(get_db)):
    report = db.query(ReportModel).filter(ReportModel.report_id == str(report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    user = db.query(UserModel).filter(UserModel.user_id == str(updated_report.user_id)).first()
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
    db.commit()
    db.refresh(report)
    return updated_report

@app.delete("/reports/{report_id}")
async def delete_report(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(ReportModel).filter(ReportModel.report_id == str(report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"detail": "Report deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```