from django.db import models

class Role(models.TextChoices):
    FOREMAN = 'Foreman', 'Foreman'
    GENERAL_FOREMAN = 'GeneralForeman', 'GeneralForeman'
    SUPERINTENDENT = 'Superintendent', 'Superintendent'
    WORKPLACE_PLANNER = 'WorkplacePlanner', 'WorkplacePlanner'
    MATERIAL_PLANNER = 'MaterialPlanner', 'MaterialPlanner'
    CONSTRUCTION_MANAGER = 'ConstructionManager', 'ConstructionManager'

class ShipmentStatus(models.TextChoices):
    IN_TRANSIT = 'InTransit', 'InTransit'
    AT_PORT = 'AtPort', 'AtPort'
    CUSTOMS = 'Customs', 'Customs'
    LAYDOWN = 'Laydown', 'Laydown'
    AVAILABLE = 'Available', 'Available'

class ScheduleStatusEnum(models.TextChoices):
    AHEAD = 'Ahead', 'Ahead'
    ON_SCHEDULE = 'OnSchedule', 'OnSchedule'
    BEHIND = 'Behind', 'Behind'

class User(models.Model):
    user_id = models.CharField(max_length=36, primary_key=True)
    username = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        db_table = 'user'

class Project(models.Model):
    project_id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'project'

class Crew(models.Model):
    crew_id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')

    class Meta:
        db_table = 'crew'

class PerformanceMetric(models.Model):
    metric_id = models.CharField(max_length=36, primary_key=True)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, db_column='crew_id')
    date = models.DateField()
    productivity = models.FloatField()
    tasks_completed = models.IntegerField()
    tasks_total = models.IntegerField()
    hours_worked = models.FloatField()

    class Meta:
        db_table = 'performance_metric'

class Activity(models.Model):
    activity_id = models.CharField(max_length=36, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    description = models.TextField()
    constraint = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'activity'

class Shipment(models.Model):
    shipment_id = models.CharField(max_length=36, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    location = models.CharField(max_length=255)
    contents = models.TextField()
    status = models.CharField(max_length=20, choices=ShipmentStatus.choices)
    arrival_date = models.DateField()
    customs_date = models.DateField()
    laydown_date = models.DateField()
    available_date = models.DateField()

    class Meta:
        db_table = 'shipment'

class ScheduleStatus(models.Model):
    status_id = models.CharField(max_length=36, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    phase = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ScheduleStatusEnum.choices)
    last_updated = models.DateField()

    class Meta:
        db_table = 'schedule_status'

class TimeReport(models.Model):
    report_id = models.CharField(max_length=36, primary_key=True)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, db_column='crew_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    date = models.DateField()
    member_name = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    hours = models.FloatField()
    effort_percentage = models.FloatField()

    class Meta:
        db_table = 'time_report'