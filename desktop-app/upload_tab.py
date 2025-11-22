"""
Upload tab for CSV file upload.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QProgressBar, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import os


class UploadThread(QThread):
    """Thread for handling file upload."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        """Run the upload process."""
        try:
            # Simulate progress
            for i in range(0, 90, 10):
                self.progress.emit(i)
                self.msleep(100)
            
            result = self.api_client.upload_csv(self.file_path)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit({'success': False, 'error': str(e)})


class UploadTab(QWidget):
    """Tab for uploading CSV files."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.selected_file = None
        self.upload_thread = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header with enhanced styling
        header = QLabel("📤 Upload CSV Data")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0F172A; padding: 5px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Import equipment data from CSV files")
        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
            padding-bottom: 5px;
        """)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Upload area with enhanced styling
        upload_frame = QFrame()
        upload_frame.setFrameStyle(QFrame.Box)
        upload_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAFC, stop:1 #F1F5F9);
                border: 3px dashed #CBD5E1;
                border-radius: 16px;
                padding: 50px;
            }
        """)
        upload_frame.setMinimumHeight(320)
        
        upload_layout = QVBoxLayout(upload_frame)
        upload_layout.setAlignment(Qt.AlignCenter)
        upload_layout.setSpacing(20)
        
        # File info label
        self.file_label = QLabel("📄 No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("""
            color: #64748B;
            font-size: 15px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.6);
            border-radius: 8px;
        """)
        upload_layout.addWidget(self.file_label)
        
        # Select file button
        select_btn = QPushButton("📁 Select CSV File")
        select_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4F46E5, stop:1 #6366F1);
                color: white;
                padding: 14px 28px;
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
        select_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(select_btn, alignment=Qt.AlignCenter)
        
        # Upload button
        self.upload_btn = QPushButton("🚀 Upload File")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06B6D4, stop:1 #0891B2);
                color: white;
                padding: 14px 28px;
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
            QPushButton:disabled {
                background-color: #CBD5E1;
                color: #94A3B8;
            }
        """)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)
        
        # Progress bar with enhanced styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                text-align: center;
                height: 30px;
                background-color: #F8FAFC;
                font-weight: bold;
                color: #334155;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4F46E5, stop:1 #818CF8);
                border-radius: 8px;
            }
        """)
        upload_layout.addWidget(self.progress_bar)
        
        layout.addWidget(upload_frame)
        
        # Instructions with enhanced styling
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #DBEAFE, stop:1 #BFDBFE);
                border: 2px solid #93C5FD;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        instructions_layout = QVBoxLayout(instructions_frame)
        
        instructions_title = QLabel("ℹ️ CSV Format Requirements")
        instructions_title.setStyleSheet("""
            color: #1E40AF;
            font-weight: bold;
            font-size: 16px;
            padding-bottom: 8px;
        """)
        instructions_layout.addWidget(instructions_title)
        
        instructions_text = QLabel("""
        • Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
        • Use comma (,) as delimiter
        • First row should contain column headers
        • Numeric values should not contain units in the CSV
        """)
        instructions_text.setStyleSheet("""
            color: #1E3A8A;
            font-size: 13px;
            line-height: 1.6;
        """)
        instructions_layout.addWidget(instructions_text)
        
        layout.addWidget(instructions_frame)
        layout.addStretch()
    
    def select_file(self):
        """Open file dialog to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            self.file_label.setText(f"{filename} ({file_size:.2f} KB)")
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload the selected CSV file."""
        if not self.selected_file:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return
        
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start upload thread
        self.upload_thread = UploadThread(self.api_client, self.selected_file)
        self.upload_thread.progress.connect(self.progress_bar.setValue)
        self.upload_thread.finished.connect(self.upload_finished)
        self.upload_thread.start()
    
    def upload_finished(self, result: dict):
        """Handle upload completion."""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        if result['success']:
            data = result['data']
            created = data.get('created_count', 0)
            updated = data.get('updated_count', 0)
            total = data.get('total_records', 0)
            
            QMessageBox.information(
                self,
                "Upload Successful",
                f"CSV file processed successfully!\n\n"
                f"Created: {created} records\n"
                f"Updated: {updated} records\n"
                f"Total: {total} records"
            )
            
            # Reset
            self.selected_file = None
            self.file_label.setText("No file selected")
            self.upload_btn.setEnabled(False)
            
            # Notify parent to refresh data
            parent = self.parent()
            while parent:
                if hasattr(parent, 'refresh_all'):
                    parent.refresh_all()
                    break
                parent = parent.parent()
        else:
            error_msg = result.get('error', 'Upload failed')
            if isinstance(error_msg, dict):
                error_msg = str(error_msg)
            QMessageBox.critical(self, "Upload Failed", f"Error: {error_msg}")

