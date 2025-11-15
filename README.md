# 🧪 ChemViz Pro - Chemical Equipment Visualizer

A comprehensive full-stack web application for managing, visualizing, and analyzing chemical equipment data from CSV files. Built with Django REST Framework and React.js.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.3.1-blue.svg)

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Usage Guide](#-usage-guide)
- [CSV File Format](#-csv-file-format)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## ⚡ Quick Start

### Backend (5 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (3 minutes)

```bash
cd web-frontend
npm install
npm run dev
```

### First Use

1. Open `http://localhost:3000`
2. Register a new account
3. Upload `sample_equipment_data.csv`
4. Explore the dashboard!

**That's it!** 🎉

---

## ✨ Features

### Core Functionality
- 📤 **CSV File Upload**: Upload and process chemical equipment data from CSV files
- 📊 **Data Visualization**: Interactive charts and graphs for equipment analysis
- 📈 **Dashboard Analytics**: Real-time summary statistics and insights
- 📋 **Data Management**: View, search, and filter equipment records
- 📄 **PDF Report Generation**: Generate detailed equipment reports
- 🔐 **User Authentication**: Secure user-based authentication and data isolation
- 🎨 **Modern UI**: Beautiful, responsive design with dark mode support

### Advanced Features
- 🔄 **Dynamic Columns**: Support for custom CSV columns (humidity, vibration, etc.)
- 📁 **File History**: Track and manage uploaded CSV files
- 🔍 **Advanced Filtering**: Filter by equipment type, status, and CSV upload
- 📊 **Multiple Chart Types**: Flowrate charts, type distribution, and more
- 💾 **Data Retention**: Automatic cleanup (keeps last 5 CSV uploads per user)
- 🌐 **RESTful API**: Comprehensive API with Swagger documentation

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Data Processing**: Pandas 2.1.3
- **PDF Generation**: ReportLab 4.0.7
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Server**: Gunicorn (production)

### Frontend
- **Framework**: React 18.3.1
- **Build Tool**: Vite 5.3.1
- **Styling**: Tailwind CSS 3.4.4
- **Charts**: Recharts 2.15.2
- **Icons**: Lucide React
- **HTTP Client**: Axios 1.7.2
- **Routing**: React Router DOM 6.26.0

### Development Tools
- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node.js)
- **Environment Variables**: python-decouple

---

## 🖼 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+View)

### Data Visualization
![Visualization](https://via.placeholder.com/800x400?text=Data+Visualization)

### CSV Upload
![Upload](https://via.placeholder.com/800x400?text=CSV+Upload)

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8 or higher
- **Node.js** 18.x or higher
- **npm** or **yarn**
- **Git**
- **Virtual Environment** (recommended for Python)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env

# Edit .env file with your settings
# At minimum, set:
# DEBUG=True
# SECRET_KEY=your-secret-key-here

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../web-frontend

# Install dependencies
npm install

# Create .env file
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env

# Edit .env file
# Set VITE_API_URL=http://localhost:8000/api
```

### Running the Application

#### Start Backend Server

```bash
# From backend directory
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

The backend API will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/swagger/`
- Admin Panel: `http://localhost:8000/admin/`

#### Start Frontend Development Server

```bash
# From web-frontend directory
cd web-frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
│
├── backend/                          # Django Backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile                      # For Heroku/Railway
│   ├── deploy.sh                     # Deployment script
│   ├── backend/                      # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── api/                          # Main API app
│       ├── models.py                 # Database models
│       ├── views.py                  # API views
│       ├── serializers.py            # Data serializers
│       ├── urls.py                   # API routes
│       ├── utils.py                  # Helper functions
│       └── migrations/               # Database migrations
│
├── web-frontend/                     # React Frontend
│   ├── src/
│   │   ├── api/                      # API client
│   │   │   └── client.js
│   │   ├── components/              # Reusable components
│   │   │   ├── Layout.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── StatsCard.jsx
│   │   ├── pages/                    # Page components
│   │   │   ├── LoginPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   └── VisualizationPage.jsx
│   │   ├── App.jsx                   # Main app component
│   │   └── main.jsx                  # Entry point
│   ├── public/                       # Static assets
│   ├── package.json
│   ├── vercel.json                   # Vercel config
│   └── netlify.toml                  # Netlify config
│
├── Docs/                             # Documentation
│   ├── Project_Requirement_Document.pdf
│   └── Chemical Equipment Dashboard UI/
│
├── sample_data/                      # Sample CSV files
│   └── sample_equipment_data.csv
│
├── DEPLOYMENT_PLAN.md                # Deployment guide
├── DEPLOYMENT_QUICK_START.md         # Quick deployment
└── README.md                         # This file
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "user123",
  "password": "password123",
  "password_confirm": "password123",
  "email": "user@example.com"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

#### Get Current User
```http
GET /api/auth/me/
```

#### Logout
```http
POST /api/auth/logout/
```

### Equipment Endpoints

#### List Equipment
```http
GET /api/equipment/
Query Parameters:
  - csv_upload: Filter by CSV upload ID
  - type: Filter by equipment type
  - status: Filter by status
  - search: Search by name or ID
```

#### Get Equipment by ID
```http
GET /api/equipment/{id}/
```

### CSV Upload Endpoints

#### Upload CSV File
```http
POST /api/uploads/
Content-Type: multipart/form-data

file: [CSV file]
```

#### List Uploads
```http
GET /api/uploads/
```

#### Get Upload Details
```http
GET /api/uploads/{id}/
```

### Dashboard Endpoints

#### Get Summary Statistics
```http
GET /api/dashboard/summary/
```

#### Get Flowrate Chart Data
```http
GET /api/dashboard/flowrate-chart/
Query Parameters:
  - csv_upload: Filter by CSV upload ID
```

#### Get Type Distribution Data
```http
GET /api/dashboard/type-distribution/
Query Parameters:
  - csv_upload: Filter by CSV upload ID
```

### Interactive API Documentation

Visit `http://localhost:8000/swagger/` for interactive Swagger UI documentation.

---

## 🔐 Authentication

The application uses **session-based authentication** with CSRF protection.

### How It Works

1. **Registration/Login**: Users register or log in through the frontend
2. **Session Creation**: Backend creates a session and sets a cookie
3. **Authenticated Requests**: Frontend includes session cookie in all requests
4. **CSRF Protection**: CSRF token is automatically included in POST requests

### User Data Isolation

- Each user can only see their own CSV uploads
- Equipment data is filtered by user
- Dashboard statistics are user-specific
- Automatic cleanup keeps last 5 uploads per user

---

## 📖 Usage Guide

### 1. First Time Setup

1. **Register an Account**
   - Navigate to the login page
   - Click "Don't have an account? Register"
   - Fill in username, password, and optional email
   - Click "Register"

2. **Login**
   - Enter your username and password
   - Click "Sign In"

### 2. Upload CSV File

1. Navigate to **Upload** page from sidebar
2. **Drag and drop** a CSV file or click to browse
3. **Supported CSV format**:
   - **Required columns**: Equipment Name, Type
   - **Optional columns**: Flowrate, Pressure, Temperature, and any custom columns (e.g., Humidity, Vibration)
   - **Example format**:
     ```csv
     Equipment Name,Type,Flowrate,Pressure,Temperature
     Pump-1,Pump,120,5.2,110
     Compressor-1,Compressor,95,8.4,95
     ```
   - See `sample_equipment_data.csv` for a complete example

4. Click **Upload CSV** button
5. Wait for processing to complete

### 3. View Dashboard

1. Navigate to **Dashboard** page
2. View summary statistics:
   - Total equipment count
   - Active/Inactive equipment
   - Average flowrate, pressure, temperature
3. View interactive charts:
   - Flowrate chart
   - Equipment type distribution

### 4. Visualize Data

1. Navigate to **Data Visualization** page
2. **Filter data**:
   - Search by equipment name or ID
   - Filter by CSV upload file
   - Filter by equipment type
3. **View table** with all equipment data
4. **Export data** as CSV (coming soon)

### 5. View History

1. Navigate to **History** page
2. View all uploaded CSV files
3. See upload details and statistics

---

## 🚀 Deployment

### 🆓 Free Deployment Options

**Option 1: Render (Free Tier)**
- See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for step-by-step guide
- Backend + Frontend on Render (free tier available)
- Note: Free tier spins down after 15 min inactivity

**Option 2: Render Backend + Vercel Frontend (Recommended)**
- Backend: [Render](https://render.com) (free tier)
- Frontend: [Vercel](https://vercel.com) (always free, faster)
- Best of both worlds!

**Option 3: Railway (Paid)**
- See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) if you have Railway credits

### 📖 Simple Deployment Guide

See [SIMPLE_DEPLOYMENT.md](SIMPLE_DEPLOYMENT.md) for detailed step-by-step instructions with multiple platform options.

### Advanced Deployment

- [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) - Quick deployment options
- [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md) - Comprehensive production guide

### Recommended Platforms

**Backend:**
- Railway (easiest)
- Render
- Heroku
- DigitalOcean (VPS)

**Frontend:**
- Vercel (recommended)
- Netlify
- AWS S3 + CloudFront

### Environment Variables

**Backend (.env):**
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=api.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chemviz_db
DB_USER=chemviz_user
DB_PASSWORD=secure-password
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production):**
```env
VITE_API_URL=https://api.yourdomain.com/api
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd web-frontend
npm test
```

### Manual Testing Checklist

- [ ] User registration
- [ ] User login/logout
- [ ] CSV file upload
- [ ] Data visualization
- [ ] Dashboard statistics
- [ ] Filtering and search
- [ ] PDF report generation
- [ ] Responsive design

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Follow ESLint rules
- **React**: Use functional components with hooks
- **Django**: Follow Django best practices

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Known Issues

- CSV files with very large datasets (>10MB) may take longer to process
- Some browsers may require manual CSRF token refresh on first load

---

## 🔮 Future Enhancements

- [ ] Real-time data updates
- [ ] Advanced analytics and predictions
- [ ] Mobile app support
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Data export in multiple formats
- [ ] Custom dashboard widgets
- [ ] API rate limiting
- [ ] WebSocket support for live updates

---

## 📄 CSV File Format

### Required Columns
- `Equipment Name` - Name of the equipment
- `Type` - Equipment type (Pump, Valve, Compressor, etc.)

### Optional Standard Columns
- `Flowrate` - Flow rate value
- `Pressure` - Pressure value
- `Temperature` - Temperature value
- `Location` - Equipment location
- `Status` - Equipment status (Active, Inactive, Maintenance, etc.)
- `Manufacturer` - Manufacturer name
- `Model Number` - Model number
- `Serial Number` - Serial number
- `Capacity` - Equipment capacity
- `Installation Date` - Installation date
- `Last Maintenance` - Last maintenance date
- `Notes` - Additional notes

### Dynamic Columns
You can include **any additional columns** in your CSV file. These will be stored as dynamic parameters and displayed in the visualization table. Examples:
- `Humidity`
- `Vibration`
- `Power Consumption`
- `Efficiency`
- Any other custom metric

### Sample CSV
See `sample_equipment_data.csv` in the root directory for a complete example.

---

## 📞 Support

### Documentation
- **API Docs**: `http://localhost:8000/swagger/`
- **Deployment Guide**: [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)
- **Quick Start**: [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md)

### Issues
If you encounter any issues, please:
1. Check existing [GitHub Issues](https://github.com/yourusername/chemical-equipment-visualizer/issues)
2. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

### Contact
- **Email**: support@chemvizpro.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Django REST Framework team
- React and Vite communities
- Tailwind CSS for the amazing styling framework
- Recharts for beautiful chart components
- All contributors and users

---

## 📊 Project Status

✅ **Active Development** - Version 1.0.0

- ✅ Core features implemented
- ✅ User authentication
- ✅ CSV upload and processing
- ✅ Data visualization
- ✅ Dashboard analytics
- ✅ PDF report generation
- 🔄 Performance optimization (ongoing)
- 🔄 Additional features (planned)

---

**Made with ❤️ for Chemical Equipment Management**

