import csv
from django.apps import apps
from django.db import transaction
from datetime import datetime
import os

def load_csv_data():
    models = {
        'user': ('users.csv', ['user_id', 'username', 'role']),
        'project': ('projects.csv', ['project_id', 'name', 'start_date', 'end_date']),
        'crew': ('crews.csv', ['crew_id', 'name', 'project_id']),
        'performancemetric': ('metrics.csv', ['metric_id', 'crew_id', 'date', 'productivity', 'tasks_completed', 'tasks_total', 'hours_worked']),
        'activity': ('activities.csv', ['activity_id', 'project_id', 'description', 'constraint', 'start_date', 'end_date']),
        'shipment': ('shipments.csv', ['shipment_id', 'project_id', 'location', 'contents', 'status', 'arrival_date', 'customs_date', 'laydown_date', 'available_date']),
        'schedulestatus': ('statuses.csv', ['status_id', 'project_id', 'phase', 'status', 'last_updated']),
        'timereport': ('reports.csv', ['report_id', 'crew_id', 'user_id', 'date', 'member_name', 'task', 'hours', 'effort_percentage']),
    }
    with transaction.atomic():
        for model_name, (csv_file, fields) in models.items():
            Model = apps.get_model('apps', model_name)
            csv_path = os.path.join('data', csv_file)
            if not os.path.exists(csv_path):
                print(f"Warning: {csv_path} not found, skipping.")
                continue
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Prepare data with correct fields
                    data = {}
                    for field in fields:
                        if field in row:
                            if field.endswith('date') or field == 'last_updated':
                                if row[field]:
                                    data[field] = datetime.strptime(row[field], '%Y-%m-%d').date()
                                else:
                                    data[field] = None
                            else:
                                data[field] = row[field]
                    # Convert numeric fields
                    if model_name == 'performancemetric':
                        data['productivity'] = float(data['productivity'])
                        data['tasks_completed'] = int(data['tasks_completed'])
                        data['tasks_total'] = int(data['tasks_total'])
                        data['hours_worked'] = float(data['hours_worked'])
                    if model_name == 'timereport':
                        data['hours'] = float(data['hours'])
                        data['effort_percentage'] = float(data['effort_percentage'])
                    # Use get_or_create to avoid duplicates
                    try:
                        Model.objects.get_or_create(**data)
                    except Exception as e:
                        print(f"Error loading {model_name} with data {data}: {e}")