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