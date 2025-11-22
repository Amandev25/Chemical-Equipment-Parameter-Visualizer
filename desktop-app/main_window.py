"""
Main window for the desktop application.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton,
    QHBoxLayout, QLabel, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from api_client import APIClient
from auth_dialog import AuthDialog
from dashboard_tab import DashboardTab
from upload_tab import UploadTab
from visualization_tab import VisualizationTab


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_user = None
        self.setup_ui()
        self.show_auth_dialog()
    
    def setup_ui(self):
        """Setup the UI components."""
        self.setWindowTitle("Chemical Equipment Visualizer - Desktop Application")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top bar with gradient effect
        top_bar = QWidget()
        top_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0F172A, stop:1 #1E293B);
                padding: 10px 20px;
                border-bottom: 2px solid #334155;
            }
        """)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(25, 15, 25, 15)
        
        title = QLabel("⚗️ Chemical Equipment Visualizer")
        title.setStyleSheet("""
            color: white; 
            font-size: 20px; 
            font-weight: bold;
            padding: 5px;
        """)
        top_bar_layout.addWidget(title)
        
        top_bar_layout.addStretch()
        
        self.user_label = QLabel("Not logged in")
        self.user_label.setStyleSheet("""
            color: #CBD5E1; 
            font-size: 13px;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 6px 12px;
            border-radius: 6px;
        """)
        top_bar_layout.addWidget(self.user_label)
        
        top_bar_layout.addSpacing(10)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4F46E5, stop:1 #6366F1);
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6366F1, stop:1 #818CF8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4338CA, stop:1 #4F46E5);
            }
        """)
        refresh_btn.clicked.connect(self.refresh_all)
        top_bar_layout.addWidget(refresh_btn)
        
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #EF4444, stop:1 #F87171);
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F87171, stop:1 #FCA5A5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #DC2626, stop:1 #EF4444);
            }
        """)
        logout_btn.clicked.connect(self.logout)
        top_bar_layout.addWidget(logout_btn)
        
        layout.addWidget(top_bar)
        
        # Tab widget with enhanced styling
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E2E8F0;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAFC, stop:1 #F1F5F9);
                border-radius: 0px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E2E8F0, stop:1 #CBD5E1);
                color: #475569;
                padding: 12px 30px;
                min-width: 120px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8FAFC);
                color: #0F172A;
                font-weight: bold;
                border-bottom: 3px solid #4F46E5;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F1F5F9, stop:1 #E2E8F0);
            }
        """)
        
        # Create tabs
        self.dashboard_tab = DashboardTab(self.api_client)
        self.upload_tab = UploadTab(self.api_client, self)
        self.visualization_tab = VisualizationTab(self.api_client, self)
        
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.upload_tab, "📤 Upload")
        self.tabs.addTab(self.visualization_tab, "📈 Visualization")
        
        layout.addWidget(self.tabs)
    
    def show_auth_dialog(self):
        """Show authentication dialog."""
        dialog = AuthDialog(self.api_client, self)
        if dialog.exec_() == QDialog.Accepted:
            if dialog.is_authenticated:
                # Get current user info
                user_result = self.api_client.get_current_user()
                if user_result['success']:
                    self.current_user = user_result['data']
                    username = self.current_user.get('username', 'User')
                    self.user_label.setText(f"👤 {username}")
                    self.user_label.setStyleSheet("""
                        color: #10B981; 
                        font-size: 13px;
                        background-color: rgba(16, 185, 129, 0.15);
                        padding: 6px 12px;
                        border-radius: 6px;
                        font-weight: bold;
                    """)
                else:
                    self.user_label.setText("✅ Logged in")
                    self.user_label.setStyleSheet("""
                        color: #10B981; 
                        font-size: 13px;
                        background-color: rgba(16, 185, 129, 0.15);
                        padding: 6px 12px;
                        border-radius: 6px;
                    """)
                # Load data in all tabs after successful authentication
                self.dashboard_tab.load_data()
                self.visualization_tab.refresh()
            else:
                QMessageBox.warning(self, "Authentication Failed", "Please login to continue.")
                self.close()
        else:
            self.close()
    
    def logout(self):
        """Logout current user."""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.current_user = None
            self.user_label.setText("Not logged in")
            self.user_label.setStyleSheet("""
                color: #CBD5E1; 
                font-size: 13px;
                background-color: rgba(255, 255, 255, 0.1);
                padding: 6px 12px;
                border-radius: 6px;
            """)
            self.show_auth_dialog()
    
    def refresh_all(self):
        """Refresh all tabs."""
        self.dashboard_tab.refresh()
        self.visualization_tab.refresh()
        QMessageBox.information(self, "Refresh", "Data refreshed successfully!")

