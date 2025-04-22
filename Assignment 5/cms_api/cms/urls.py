from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from cms.apps.views import UserViewSet, CrewViewSet, ProjectViewSet, PerformanceMetricViewSet, ActivityViewSet, ShipmentViewSet, ScheduleStatusViewSet, TimeReportViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'crews', CrewViewSet, basename='crew')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'metrics', PerformanceMetricViewSet, basename='metric')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'shipments', ShipmentViewSet, basename='shipment')
router.register(r'statuses', ScheduleStatusViewSet, basename='status')
router.register(r'reports', TimeReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('health/', lambda request: {'status': 'OK', 'message': 'API is running'}, name='health'),
]