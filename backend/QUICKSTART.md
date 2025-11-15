# Quick Start Guide - Backend

## ✅ Setup Complete!

Your Django backend has been successfully set up and configured!

## 🚀 Running the Server

**Option 1: Using Virtual Environment (Recommended)**
```bash
cd backend
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Linux/Mac
python manage.py runserver
```

**Option 2: Direct Run**
```bash
cd backend
.\venv\Scripts\python.exe manage.py runserver
```

## 🌐 Access Points

Once the server is running, access:

- **API Root**: http://localhost:8000/api/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/api/health/

## 📝 Create Admin User (Optional)

```bash
cd backend
.\venv\Scripts\python.exe manage.py createsuperuser
```

Then access admin at: http://localhost:8000/admin/

## 🧪 Test the API

### 1. Health Check
Open browser: http://localhost:8000/api/health/

Should return:
```json
{
    "status": "healthy",
    "message": "Chemical Equipment Visualizer API is running",
    "version": "1.0.0",
    "total_equipment": 0
}
```

### 2. Upload Sample CSV

**Using curl (if available):**
```bash
curl -X POST http://localhost:8000/api/uploads/ \
  -F "file=@../sample_data/sample_equipment_data.csv"
```

**Or use Swagger UI:**
1. Go to http://localhost:8000/swagger/
2. Find `/api/uploads/` POST endpoint
3. Click "Try it out"
4. Upload the CSV file from `sample_data/sample_equipment_data.csv`
5. Click "Execute"

### 3. View Equipment Data

Open browser: http://localhost:8000/api/equipment/

### 4. View Dashboard Summary

Open browser: http://localhost:8000/api/dashboard/summary/

## 📊 API Endpoints Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/equipment/` | GET | List all equipment |
| `/api/equipment/` | POST | Create equipment |
| `/api/equipment/{id}/` | GET | Get equipment details |
| `/api/uploads/` | POST | Upload CSV file |
| `/api/dashboard/summary/` | GET | Dashboard summary |
| `/api/dashboard/flowrate-chart/` | GET | Flowrate chart data |
| `/api/dashboard/type-distribution/` | GET | Type distribution |
| `/api/reports/generate/` | POST | Generate PDF report |

## 🔧 Common Commands

**Check migrations:**
```bash
.\venv\Scripts\python.exe manage.py showmigrations
```

**Create new migrations (after model changes):**
```bash
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

**Run tests:**
```bash
.\venv\Scripts\python.exe manage.py test api
```

**Clear all data:**
```bash
# Using API endpoint
curl -X DELETE http://localhost:8000/api/clear/
```

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 8000 is in use
- Try different port: `python manage.py runserver 8001`

**Import errors:**
- Make sure virtual environment is activated
- Reinstall packages: `pip install -r requirements.txt`

**Database errors:**
- Delete `db.sqlite3` and run migrations again

## ✨ Next Steps

1. ✅ Backend is running
2. Test API endpoints using Swagger UI
3. Upload sample CSV data
4. Build frontend (React)
5. Build desktop app (PyQt5)

## 📚 Documentation

Full documentation: See `README.md`

API Documentation: http://localhost:8000/swagger/

---

**Status**: ✅ Backend is ready to use!

