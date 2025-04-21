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