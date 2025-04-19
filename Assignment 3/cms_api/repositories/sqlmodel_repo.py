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