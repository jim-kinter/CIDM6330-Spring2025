# CMS API README

The Construction Management System (CMS) API was initially built using FastAPI with a custom repository pattern supporting SQLModel, CSV, and In-Memory storage for entities: User, Crew, Project, PerformanceMetric, Activity, Shipment, ScheduleStatus, and TimeReport based upon the original system requirements. 

I transitioned it to Django REST Framework (DRF) with Django ORM per the assignment, maintaining all CRUD endpoints and Foreman-only checks for TimeReport. The API now uses SQLite (`cms.db`) for data storage, replacing the repository pattern with Django ORM models defined in `cms/apps/models.py`. 

Sample data from CSV files (`data/users.csv`, `crews.csv`, etc.) was migrated to `cms.db` using a `load_csv.py` script, ensuring referential integrity. 

The Django admin UI at `http://localhost:8000/admin/` provides data management. The transition preserves functionality, with DRF endpoints tested at `http://localhost:8000/` and data verified via admin UI.