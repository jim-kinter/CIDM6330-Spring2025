from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Crew, Project, PerformanceMetric, ScheduleStatus
from .tasks import generate_performance_report_task, send_notification_task
from datetime import datetime
from django.urls import reverse

class CMSTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            user_id='111e2222-3333-4444-5555-666677778888',
            username='john_doe',
            role='Foreman'
        )
        self.project = Project.objects.create(
            project_id='777e8888-9999-0000-1111-222233334444',
            name='highway_expansion',
            start_date='2025-01-01',
            end_date='2025-12-31'
        )
        self.crew = Crew.objects.create(
            crew_id='444e5555-6666-7777-8888-999900001111',
            name='welding_team',
            project=self.project
        )
        self.metric = PerformanceMetric.objects.create(
            metric_id='999e0000-1111-2222-3333-444455556666',
            crew=self.crew,
            date='2025-04-01',
            productivity=0.85,
            tasks_completed=10,
            tasks_total=12,
            hours_worked=8.0
        )
        self.status = ScheduleStatus.objects.create(
            status_id='555e6666-7777-8888-9999-000011112222',
            project=self.project,
            phase='foundation',
            status='OnSchedule',
            last_updated='2025-04-01'
        )

    def test_generate_performance_report(self):
        result = generate_performance_report_task(self.crew.crew_id, '2025-04-01', '2025-04-01')
        self.assertEqual(result['crew_id'], self.crew.crew_id)
        self.assertAlmostEqual(result['avg_productivity'], 0.85)
        self.assertEqual(result['total_tasks_completed'], 10)
        self.assertEqual(result['total_hours_worked'], 8.0)

    def test_send_notification(self):
        result = send_notification_task(self.user.user_id, 'Test notification')
        self.assertEqual(result['user_id'], self.user.user_id)
        self.assertEqual(result['message'], 'Test notification')

    def test_calculate_project_progress(self):
        response = self.client.get(
            reverse('project-calculate-progress', kwargs={'project_id': self.project.project_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['project_id'], self.project.project_id)
        self.assertGreaterEqual(response.data['progress_percentage'], 0)

    def test_generate_report_endpoint(self):
        data = {
            'crew_id': self.crew.crew_id,
            'start_date': '2025-04-01',
            'end_date': '2025-04-01'
        }
        response = self.client.post(
            reverse('performancemetric-generate-report'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('task_id', response.data)

    def test_schedule_status_notification(self):
        data = {
            'status_id': '666e7777-8888-9999-0000-111122223333',
            'project_id': self.project.project_id,
            'phase': 'framing',
            'status': 'Ahead',
            'last_updated': '2025-04-02',
            'user_id': self.user.user_id
        }
        response = self.client.post(
            reverse('schedulestatus-list'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)