# Generated by Django 5.0.9 on 2025-04-25 00:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Inspected', 'Inspected'), ('Stored', 'Stored'), ('Issued', 'Issued'), ('Shipped', 'Shipped')], default='Received', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('maint_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('condition', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.material')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryRecord',
            fields=[
                ('inv_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('last_checked', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.material')),
            ],
        ),
        migrations.CreateModel(
            name='InstallationRequirement',
            fields=[
                ('inst_req_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('fab_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.material')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('req_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('delivery_date', models.DateField()),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Feedback', 'Feedback'), ('Finalized', 'Finalized')], default='Draft', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.material')),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('widget_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Fabricated', 'Fabricated'), ('Inspected', 'Inspected'), ('Shipped', 'Shipped')], default='Fabricated', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.material')),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('shipment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tracking_id', models.CharField(max_length=50)),
                ('customer_id', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Prepared', 'Prepared'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Prepared', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.material')),
                ('widget_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.widget')),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('inspection_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('result', models.CharField(choices=[('Pass', 'Pass'), ('Fail', 'Fail')], max_length=50)),
                ('defects', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.material')),
                ('widget_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.widget')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_id', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.material')),
                ('widget_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.widget')),
            ],
        ),
    ]
