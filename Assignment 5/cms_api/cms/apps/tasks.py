from celery import shared_task
from django.db.models import Avg, Sum
from .models import PerformanceMetric, User, ScheduleStatus
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_performance_report_task(crew_id, start_date, end_date):
    metrics = PerformanceMetric.objects.filter(
        crew_id=crew_id,
        date__range=[start_date, end_date]
    )
    report = {
        'crew_id': crew_id,
        'start_date': start_date,
        'end_date': end_date,
        'avg_productivity': metrics.aggregate(Avg('productivity'))['productivity__avg'] or 0,
        'total_tasks_completed': metrics.aggregate(Sum('tasks_completed'))['tasks_completed__sum'] or 0,
        'total_hours_worked': metrics.aggregate(Sum('hours_worked'))['hours_worked__sum'] or 0
    }
    logger.info(f"Generated report: {report}")
    return report

@shared_task
def send_notification_task(user_id, message):
    logger.info(f"Notification sent to user {user_id}: {message}")
    return {"user_id": user_id, "message": message}