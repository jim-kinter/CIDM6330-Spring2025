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