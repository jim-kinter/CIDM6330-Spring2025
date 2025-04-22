from django.contrib import admin
from .models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'role')
    search_fields = ('username', 'role')

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('crew_id', 'name', 'project_id')
    search_fields = ('name',)
    list_filter = ('project_id',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_id', 'crew_id', 'date', 'productivity', 'tasks_completed', 'tasks_total', 'hours_worked')
    search_fields = ('crew_id',)
    list_filter = ('date',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 'project_id', 'description', 'constraint', 'start_date', 'end_date')
    search_fields = ('description', 'constraint')
    list_filter = ('project_id', 'start_date', 'end_date')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('shipment_id', 'project_id', 'location', 'contents', 'status', 'arrival_date')
    search_fields = ('location', 'contents')
    list_filter = ('project_id', 'status', 'arrival_date')

@admin.register(ScheduleStatus)
class ScheduleStatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'project_id', 'phase', 'status', 'last_updated')
    search_fields = ('phase',)
    list_filter = ('project_id', 'status', 'last_updated')

@admin.register(TimeReport)
class TimeReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'crew_id', 'user_id', 'date', 'member_name', 'task', 'hours', 'effort_percentage')
    search_fields = ('member_name', 'task')
    list_filter = ('crew_id', 'user_id', 'date')