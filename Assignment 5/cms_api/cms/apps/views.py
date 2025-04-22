from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, TimeReport, Role
from .serializers import UserSerializer, CrewSerializer, ProjectSerializer, PerformanceMetricSerializer, ActivitySerializer, ShipmentSerializer, ScheduleStatusSerializer, TimeReportSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .tasks import generate_performance_report_task, send_notification_task
from datetime import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    lookup_field = 'crew_id'

    @action(detail=False, methods=['get'], url_path='by-project/(?P<project_id>[^/.]+)')
    def by_project(self, request, project_id=None):
        crews = self.queryset.filter(project_id=project_id)
        serializer = self.get_serializer(crews, many=True)
        return Response(serializer.data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    @action(detail=True, methods=['get'], url_path='progress')
    def calculate_progress(self, request, project_id=None):
        project = get_object_or_404(Project, project_id=project_id)
        statuses = ScheduleStatus.objects.filter(project_id=project_id)
        activities = Activity.objects.filter(project_id=project_id)
        total_phases = statuses.count()
        completed_phases = statuses.filter(status='OnSchedule').count() + statuses.filter(status='Ahead').count()
        progress = (completed_phases / total_phases * 100) if total_phases > 0 else 0
        return Response({
            'project_id': project_id,
            'progress_percentage': progress,
            'total_phases': total_phases,
            'completed_phases': completed_phases,
            'activity_count': activities.count()
        })

class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    lookup_field = 'metric_id'

    def get_queryset(self):
        crew_id = self.request.query_params.get('crew_id')
        if crew_id:
            return self.queryset.filter(crew_id=crew_id)
        return self.queryset

    @action(detail=False, methods=['post'], url_path='report')
    def generate_report(self, request):
        crew_id = request.data.get('crew_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if not all([crew_id, start_date, end_date]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        task = generate_performance_report_task.delay(crew_id, start_date, end_date)
        return Response({'task_id': task.id, 'status': 'Report generation started'})

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_field = 'activity_id'

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = 'shipment_id'

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset

class ScheduleStatusViewSet(viewsets.ModelViewSet):
    queryset = ScheduleStatus.objects.all()
    serializer_class = ScheduleStatusSerializer
    lookup_field = 'status_id'

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_id = request.data.get('user_id')
        if user_id:
            message = f"Schedule status updated for project {request.data.get('project_id')}: {request.data.get('phase')} is {request.data.get('status')}"
            send_notification_task.delay(user_id, message)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user_id = request.data.get('user_id')
        if user_id:
            message = f"Schedule status updated for project {request.data.get('project_id')}: {request.data.get('phase')} is {request.data.get('status')}"
            send_notification_task.delay(user_id, message)
        return response

class TimeReportViewSet(viewsets.ModelViewSet):
    queryset = TimeReport.objects.all()
    serializer_class = TimeReportSerializer
    lookup_field = 'report_id'

    def get_queryset(self):
        crew_id = self.request.query_params.get('crew_id')
        if crew_id:
            return self.queryset.filter(crew_id=crew_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        if user.role != Role.FOREMAN:
            raise PermissionDenied("Only Foremen can submit time reports")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        if user.role != Role.FOREMAN:
            raise PermissionDenied("Only Foremen can update time reports")
        return super().update(request, *args, **kwargs)