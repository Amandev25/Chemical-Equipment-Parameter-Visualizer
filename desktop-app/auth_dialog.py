"""
Authentication dialog for login and registration.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AuthDialog(QDialog):
    """Dialog for user authentication (login/register)."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.is_authenticated = False
        self.setWindowTitle("Chemical Equipment Visualizer - Authentication")
        self.setMinimumWidth(480)
        self.setMinimumHeight(600)
        self.resize(500, 650)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Set dialog background
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAFC, stop:1 #F1F5F9);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Title with icon
        title = QLabel("⚗️ Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("""
            color: #0F172A;
            padding: 8px 0px;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Desktop Application")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 13px;
            padding-bottom: 5px;
        """)
        layout.addWidget(subtitle)
        
        layout.addSpacing(15)
        
        # Tab widget for Login/Register with enhanced styling
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E2E8F0;
                background-color: white;
                border-radius: 12px;
                padding: 5px;
            }
            QTabBar::tab {
                background-color: #F1F5F9;
                color: #475569;
                padding: 12px 40px;
                min-width: 140px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 3px;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #0F172A;
                font-weight: bold;
                border-bottom: 3px solid #4F46E5;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E2E8F0;
            }
        """)
        
        # Login Tab
        login_tab = QWidget()
        login_tab.setStyleSheet("background-color: white; border-radius: 10px;")
        login_layout = QVBoxLayout(login_tab)
        login_layout.setSpacing(15)
        login_layout.setContentsMargins(25, 25, 25, 25)
        
        username_label = QLabel("Username:")
        username_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        login_layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setMinimumHeight(40)
        self.login_username.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        login_layout.addWidget(self.login_username)
        
        login_layout.addSpacing(5)
        
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        login_layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setMinimumHeight(40)
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        login_layout.addWidget(self.login_password)
        
        login_layout.addSpacing(20)
        
        login_btn = QPushButton("🔐 Login")
        login_btn.setMinimumHeight(45)
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4F46E5, stop:1 #6366F1);
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
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
        login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(login_btn)
        
        login_layout.addStretch()
        
        tabs.addTab(login_tab, "🔐 Login")
        
        # Register Tab - Use scroll area to prevent overlapping
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #F1F5F9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #CBD5E1;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94A3B8;
            }
        """)
        
        register_tab = QWidget()
        register_tab.setStyleSheet("background-color: white; border-radius: 10px;")
        register_layout = QVBoxLayout(register_tab)
        register_layout.setSpacing(15)
        register_layout.setContentsMargins(25, 25, 25, 25)
        
        username_label = QLabel("Username:")
        username_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        register_layout.addWidget(username_label)
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        self.register_username.setMinimumHeight(40)
        self.register_username.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        register_layout.addWidget(self.register_username)
        
        register_layout.addSpacing(5)
        
        email_label = QLabel("Email (optional):")
        email_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        register_layout.addWidget(email_label)
        
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("your.email@example.com")
        self.register_email.setMinimumHeight(40)
        self.register_email.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        register_layout.addWidget(self.register_email)
        
        register_layout.addSpacing(5)
        
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        register_layout.addWidget(password_label)
        
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Create a password")
        self.register_password.setMinimumHeight(40)
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        register_layout.addWidget(self.register_password)
        
        register_layout.addSpacing(5)
        
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet("color: #334155; font-weight: 600; font-size: 13px; padding-bottom: 3px;")
        register_layout.addWidget(confirm_label)
        
        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setPlaceholderText("Re-enter your password")
        self.register_password_confirm.setMinimumHeight(40)
        self.register_password_confirm.setEchoMode(QLineEdit.Password)
        self.register_password_confirm.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                font-size: 14px;
                background-color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        register_layout.addWidget(self.register_password_confirm)
        
        register_layout.addSpacing(20)
        
        register_btn = QPushButton("✨ Register")
        register_btn.setMinimumHeight(45)
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06B6D4, stop:1 #0891B2);
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0891B2, stop:1 #0E7490);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0E7490, stop:1 #155E75);
            }
        """)
        register_btn.clicked.connect(self.handle_register)
        register_layout.addWidget(register_btn)
        
        register_layout.addStretch()
        
        scroll_area.setWidget(register_tab)
        
        tabs.addTab(scroll_area, "✨ Register")
        
        layout.addWidget(tabs)
        
        layout.addSpacing(10)
        
        # Status label with enhanced styling
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(50)
        self.status_label.setStyleSheet("""
            color: #EF4444;
            padding: 10px 12px;
            background-color: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            font-size: 13px;
        """)
        self.status_label.setWordWrap(True)
        self.status_label.setVisible(False)  # Hidden by default
        layout.addWidget(self.status_label)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            self.status_label.setText("⚠️ Please enter username and password")
            self.status_label.setStyleSheet("""
                color: #F59E0B;
                padding: 10px 12px;
                background-color: rgba(245, 158, 11, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
            return
        
        self.status_label.setText("⏳ Logging in...")
        self.status_label.setStyleSheet("""
            color: #4F46E5;
            padding: 10px 12px;
            background-color: rgba(79, 70, 229, 0.1);
            border-radius: 8px;
            font-size: 13px;
        """)
        self.status_label.setVisible(True)
        
        result = self.api_client.login(username, password)
        
        if result['success']:
            self.is_authenticated = True
            self.status_label.setText("✅ Login successful!")
            self.status_label.setStyleSheet("""
                color: #10B981;
                padding: 10px 12px;
                background-color: rgba(16, 185, 129, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
            self.accept()
        else:
            error_msg = result.get('error', 'Login failed')
            self.status_label.setText(f"❌ Login failed: {error_msg}")
            self.status_label.setStyleSheet("""
                color: #EF4444;
                padding: 10px 12px;
                background-color: rgba(239, 68, 68, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
    
    def handle_register(self):
        """Handle register button click."""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        
        if not username or not password:
            self.status_label.setText("⚠️ Please enter username and password")
            self.status_label.setStyleSheet("""
                color: #F59E0B;
                padding: 10px 12px;
                background-color: rgba(245, 158, 11, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
            return
        
        if password != password_confirm:
            self.status_label.setText("⚠️ Passwords do not match")
            self.status_label.setStyleSheet("""
                color: #F59E0B;
                padding: 10px 12px;
                background-color: rgba(245, 158, 11, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
            return
        
        self.status_label.setText("⏳ Registering...")
        self.status_label.setStyleSheet("""
            color: #06B6D4;
            padding: 10px 12px;
            background-color: rgba(6, 182, 212, 0.1);
            border-radius: 8px;
            font-size: 13px;
        """)
        self.status_label.setVisible(True)
        
        result = self.api_client.register(username, password, password_confirm, email)
        
        if result['success']:
            self.is_authenticated = True
            self.status_label.setText("✅ Registration successful!")
            self.status_label.setStyleSheet("""
                color: #10B981;
                padding: 10px 12px;
                background-color: rgba(16, 185, 129, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)
            self.accept()
        else:
            error_msg = result.get('error', 'Registration failed')
            if isinstance(error_msg, dict):
                error_msg = str(error_msg)
            self.status_label.setText(f"❌ Registration failed: {error_msg}")
            self.status_label.setStyleSheet("""
                color: #EF4444;
                padding: 10px 12px;
                background-color: rgba(239, 68, 68, 0.1);
                border-radius: 8px;
                font-size: 13px;
            """)
            self.status_label.setVisible(True)


