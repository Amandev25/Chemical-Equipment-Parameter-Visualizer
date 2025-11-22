# Chemical Equipment Visualizer - Desktop Application

Desktop application built with PyQt5 and matplotlib for visualizing chemical equipment data.

## Features

- **Dashboard**: Overview with statistics cards and charts
- **CSV Upload**: Upload and process CSV files with equipment data
- **Data Visualization**: View, filter, and export equipment data
- **Charts**: Interactive matplotlib charts for equipment distribution and flowrate trends
- **Export**: Export data to CSV or generate PDF reports

## Requirements

- Python 3.8+
- PyQt5
- matplotlib
- requests
- pandas

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure backend is running**:
   The desktop app connects to the Django backend API at `http://localhost:8000/api`
   Make sure the backend server is running (see backend README for instructions)

## Running the Application

```bash
python main.py
```

Or on Windows:
```bash
pythonw main.py
```

## Usage

1. **Login/Register**: When you start the application, you'll be prompted to login or register
2. **Dashboard**: View overview statistics and charts
3. **Upload**: Upload CSV files containing equipment data
4. **Visualization**: Browse, filter, and export equipment data

## CSV Format

The CSV file should have the following columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Additional columns will be stored as dynamic parameters.

## Project Structure

```
desktop-app/
├── main.py                 # Entry point
├── main_window.py          # Main window with tabs
├── auth_dialog.py          # Authentication dialog
├── dashboard_tab.py        # Dashboard tab with charts
├── upload_tab.py           # CSV upload tab
├── visualization_tab.py    # Data visualization tab
├── api_client.py           # API client for backend communication
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Notes

- The desktop app requires the backend API to be running
- Authentication is required to access the application
- Data is synchronized with the web application through the shared backend


