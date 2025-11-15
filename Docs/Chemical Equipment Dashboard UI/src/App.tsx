import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './components/LoginPage';
import { Dashboard } from './components/Dashboard';
import { CSVUpload } from './components/CSVUpload';
import { DataVisualization } from './components/DataVisualization';
import { HistoryPage } from './components/HistoryPage';
import { PDFReportViewer } from './components/PDFReportViewer';
import { ThemeProvider } from './components/ThemeProvider';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route 
            path="/login" 
            element={
              isAuthenticated ? 
                <Navigate to="/dashboard" /> : 
                <LoginPage onLogin={() => setIsAuthenticated(true)} />
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              isAuthenticated ? 
                <Dashboard /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/upload" 
            element={
              isAuthenticated ? 
                <CSVUpload /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/visualization" 
            element={
              isAuthenticated ? 
                <DataVisualization /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/history" 
            element={
              isAuthenticated ? 
                <HistoryPage /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/report/:id" 
            element={
              isAuthenticated ? 
                <PDFReportViewer /> : 
                <Navigate to="/login" />
            } 
          />
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}