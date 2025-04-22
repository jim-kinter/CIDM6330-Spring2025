from rest_framework import serializers
from .models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'role']

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ['crew_id', 'name', 'project_id']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'name', 'start_date', 'end_date']

class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = ['metric_id', 'crew_id', 'date', 'productivity', 'tasks_completed', 'tasks_total', 'hours_worked']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity_id', 'project_id', 'description', 'constraint', 'start_date', 'end_date']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['shipment_id', 'project_id', 'location', 'contents', 'status', 'arrival_date', 'customs_date', 'laydown_date', 'available_date']

class ScheduleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleStatus
        fields = ['status_id', 'project_id', 'phase', 'status', 'last_updated']

class TimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeReport
        fields = ['report_id', 'crew_id', 'user_id', 'date', 'member_name', 'task', 'hours', 'effort_percentage']