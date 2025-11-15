# Chemical Equipment Visualizer - Backend

Django REST API for managing and visualizing chemical equipment data from CSV files.

## Features

- **CSV Upload & Processing**: Upload CSV files containing equipment data
- **Equipment Management**: CRUD operations for equipment records
- **Data Visualization**: API endpoints for charts and graphs
- **PDF Report Generation**: Generate detailed equipment reports
- **Dashboard Analytics**: Summary statistics and insights
- **RESTful API**: Comprehensive API with Swagger documentation

## Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Data Processing**: Pandas
- **PDF Generation**: ReportLab
- **API Documentation**: drf-yasg (Swagger/OpenAPI)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (if not exists):
   ```bash
   # Copy the example below or use provided .env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at: `http://localhost:8000/`

## API Endpoints

### Equipment Endpoints

- `GET /api/equipment/` - List all equipment
- `POST /api/equipment/` - Create new equipment
- `GET /api/equipment/{id}/` - Retrieve specific equipment
- `PUT /api/equipment/{id}/` - Update equipment
- `DELETE /api/equipment/{id}/` - Delete equipment
- `GET /api/equipment/types/` - Get unique equipment types
- `GET /api/equipment/statuses/` - Get equipment statuses

### CSV Upload Endpoints

- `GET /api/uploads/` - List all CSV uploads
- `POST /api/uploads/` - Upload and process CSV file
- `GET /api/uploads/{id}/` - Retrieve upload details
- `GET /api/uploads/{id}/equipment/` - Get equipment from specific upload
- `GET /api/uploads/{id}/summary/` - Get summary statistics

### Dashboard Endpoints

- `GET /api/dashboard/summary/` - Get dashboard summary cards
- `GET /api/dashboard/flowrate-chart/` - Get flowrate chart data
- `GET /api/dashboard/type-distribution/` - Get type distribution data

### Report Endpoints

- `POST /api/reports/generate/` - Generate PDF report

### Utility Endpoints

- `GET /api/health/` - API health check
- `DELETE /api/clear/` - Clear all data (development only)

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## CSV File Format

The CSV file should contain the following columns (flexible naming):

### Required Columns:
- `equipment_id` (or `id`, `equip_id`)
- `equipment_name` (or `name`, `equip_name`)
- `equipment_type` (or `type`, `equip_type`)

### Optional Columns:
- `manufacturer` (or `make`, `vendor`)
- `model_number` (or `model`)
- `serial_number` (or `serial`)
- `capacity`
- `flowrate` (or `flow_rate`, `flow`)
- `pressure`
- `temperature` (or `temp`)
- `location` (or `loc`)
- `status`
- `installation_date`
- `last_maintenance`
- `notes` (or `remarks`, `comments`)

### Sample CSV:
```csv
equipment_id,equipment_name,equipment_type,flowrate,pressure,status,location
PUMP-001,Main Circulation Pump,Pump,150.5,5.2,Active,Building A
VALVE-002,Control Valve,Valve,100.0,3.8,Active,Building A
TANK-003,Storage Tank,Tank,0.0,1.0,Inactive,Building B
```

## Query Parameters

### Equipment List Filtering:
- `?type=Pump` - Filter by equipment type
- `?status=Active` - Filter by status
- `?search=pump` - Search in name or ID

### Pagination:
- `?page=1` - Page number
- `?page_size=50` - Items per page (default: 100)

## Testing

Run tests with:
```bash
python manage.py test api
```

## Project Structure

```
backend/
├── backend/              # Project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── api/                 # Main API application
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # API URL routing
│   ├── utils.py         # Utility functions
│   ├── admin.py         # Django admin configuration
│   └── tests.py         # Unit tests
├── media/               # Uploaded files
│   └── uploads/         # CSV uploads
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Database Models

### Equipment
Stores individual equipment records with specifications and operational data.

### CSVUpload
Tracks uploaded CSV files and processing status.

### DataSummary
Stores aggregated statistics for each CSV upload.

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate a secure `SECRET_KEY`
3. Configure PostgreSQL database
4. Set up static file serving
5. Configure CORS for your frontend domain
6. Use gunicorn or uWSGI as WSGI server
7. Set up nginx as reverse proxy

## Admin Panel

Access Django admin at: `http://localhost:8000/admin/`

Use the superuser credentials created during setup.

## Troubleshooting

### Common Issues:

1. **Migration errors**: Delete `db.sqlite3` and `api/migrations/*.py` (except `__init__.py`), then run migrations again

2. **Port already in use**: Change port with `python manage.py runserver 8001`

3. **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in settings.py

4. **CSV upload fails**: Verify file format and check column names

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue in the repository.

## Author

Developed for Chemical Equipment Visualizer internship screening project.

