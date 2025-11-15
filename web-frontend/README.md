# Chemical Equipment Visualizer - Web Frontend

React.js frontend application for visualizing chemical equipment data.

## Features

- **Dashboard**: Overview with summary cards and charts
- **CSV Upload**: Drag-and-drop CSV file upload
- **Data Visualization**: Interactive charts and data tables
- **History**: View upload history
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on all screen sizes

## Tech Stack

- **React 18.3.1** - UI library
- **Vite 5.3.1** - Build tool
- **React Router 6.26.0** - Routing
- **Axios 1.7.2** - HTTP client
- **Recharts 2.15.2** - Chart library
- **Tailwind CSS 3.4.4** - Styling
- **Lucide React** - Icons

## Installation

### Prerequisites

- Node.js 16+ and npm/yarn
- Backend server running on http://localhost:8000

### Setup Steps

1. **Navigate to web-frontend directory**:
   ```bash
   cd web-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

The application will be available at: **http://localhost:3000**

## Project Structure

```
web-frontend/
├── src/
│   ├── api/
│   │   └── client.js          # API client with axios
│   ├── components/
│   │   ├── Layout.jsx         # Main layout wrapper
│   │   ├── Sidebar.jsx        # Navigation sidebar
│   │   ├── TopNav.jsx         # Top navigation bar
│   │   └── StatsCard.jsx      # Dashboard stat cards
│   ├── pages/
│   │   ├── LoginPage.jsx      # Login page
│   │   ├── DashboardPage.jsx  # Main dashboard
│   │   ├── UploadPage.jsx     # CSV upload page
│   │   ├── VisualizationPage.jsx  # Data visualization
│   │   └── HistoryPage.jsx    # Upload history
│   ├── App.jsx                # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── public/                    # Static assets
├── index.html                 # HTML template
├── package.json               # Dependencies
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind configuration
└── README.md                  # This file
```

## API Integration

The frontend connects to the Django backend API at `http://localhost:8000/api/`.

### API Endpoints Used

- `GET /api/health/` - Health check
- `GET /api/equipment/` - List equipment
- `POST /api/uploads/` - Upload CSV
- `GET /api/uploads/` - List uploads
- `GET /api/dashboard/summary/` - Dashboard summary
- `GET /api/dashboard/flowrate-chart/` - Flowrate chart data
- `GET /api/dashboard/type-distribution/` - Type distribution
- `POST /api/reports/generate/` - Generate PDF report

## Features

### Dashboard Page
- Summary statistics cards (Total Equipment, Avg Flowrate, Avg Pressure, Avg Temperature)
- Equipment type distribution chart
- Flowrate trends chart

### Upload Page
- Drag-and-drop CSV file upload
- Upload progress indicator
- Success/error messages
- CSV format requirements guide

### Visualization Page
- Searchable and filterable equipment table
- Equipment type distribution chart
- Flowrate trends chart
- Export to CSV
- Generate PDF report

### History Page
- List of all CSV uploads
- Upload status and timestamps
- Record counts

## Environment Variables

Create a `.env` file (optional):

```env
VITE_API_URL=http://localhost:8000/api
```

## Development

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Authentication

Currently uses simple localStorage-based authentication. In production, implement proper JWT token authentication.

## Styling

- **Tailwind CSS** for utility-first styling
- **Dark mode** support via class-based toggling
- **Responsive design** with mobile-first approach

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

**CORS Errors:**
- Ensure backend CORS is configured for `http://localhost:3000`
- Check backend is running on port 8000

**API Connection Issues:**
- Verify backend server is running
- Check API URL in `src/api/client.js`
- Check browser console for errors

**Build Errors:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## License

MIT License

