# Generated by Django 5.2 on 2025-04-21 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('crew_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'crew',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('Foreman', 'Foreman'), ('GeneralForeman', 'GeneralForeman'), ('Superintendent', 'Superintendent'), ('WorkplacePlanner', 'WorkplacePlanner'), ('MaterialPlanner', 'MaterialPlanner'), ('ConstructionManager', 'ConstructionManager')], max_length=20)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='PerformanceMetric',
            fields=[
                ('metric_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('productivity', models.FloatField()),
                ('tasks_completed', models.IntegerField()),
                ('tasks_total', models.IntegerField()),
                ('hours_worked', models.FloatField()),
                ('crew', models.ForeignKey(db_column='crew_id', on_delete=django.db.models.deletion.CASCADE, to='apps.crew')),
            ],
            options={
                'db_table': 'performance_metric',
            },
        ),
        migrations.AddField(
            model_name='crew',
            name='project',
            field=models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, to='apps.project'),
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('constraint', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, to='apps.project')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='ScheduleStatus',
            fields=[
                ('status_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('phase', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Ahead', 'Ahead'), ('OnSchedule', 'OnSchedule'), ('Behind', 'Behind')], max_length=20)),
                ('last_updated', models.DateField()),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, to='apps.project')),
            ],
            options={
                'db_table': 'schedule_status',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('shipment_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('contents', models.TextField()),
                ('status', models.CharField(choices=[('InTransit', 'InTransit'), ('AtPort', 'AtPort'), ('Customs', 'Customs'), ('Laydown', 'Laydown'), ('Available', 'Available')], max_length=20)),
                ('arrival_date', models.DateField()),
                ('customs_date', models.DateField()),
                ('laydown_date', models.DateField()),
                ('available_date', models.DateField()),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, to='apps.project')),
            ],
            options={
                'db_table': 'shipment',
            },
        ),
        migrations.CreateModel(
            name='TimeReport',
            fields=[
                ('report_id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('member_name', models.CharField(max_length=255)),
                ('task', models.CharField(max_length=255)),
                ('hours', models.FloatField()),
                ('effort_percentage', models.FloatField()),
                ('crew', models.ForeignKey(db_column='crew_id', on_delete=django.db.models.deletion.CASCADE, to='apps.crew')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='apps.user')),
            ],
            options={
                'db_table': 'time_report',
            },
        ),
    ]
