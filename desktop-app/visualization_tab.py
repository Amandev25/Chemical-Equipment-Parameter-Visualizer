"""
Visualization tab with data table and filtering.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QHeaderView, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv
import io


class VisualizationTab(QWidget):
    """Tab for visualizing equipment data."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.equipment_data = []
        self.csv_uploads = []
        self.equipment_types = []
        self.setup_ui()
        # Don't load data immediately - wait for authentication
        # Data will be loaded after user logs in
    
    def setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with export buttons
        header_layout = QHBoxLayout()
        
        header_text = QVBoxLayout()
        header = QLabel("📈 Data Visualization")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0F172A; padding: 5px;")
        header_text.addWidget(header)
        
        subtitle = QLabel("Analyze equipment parameters and trends")
        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
            padding-bottom: 5px;
        """)
        header_text.addWidget(subtitle)
        
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        # Export buttons with enhanced styling
        export_csv_btn = QPushButton("📥 Export CSV")
        export_csv_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4F46E5;
                padding: 10px 20px;
                border: 2px solid #4F46E5;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #EEF2FF;
                border-color: #6366F1;
            }
            QPushButton:pressed {
                background-color: #E0E7FF;
            }
        """)
        export_csv_btn.clicked.connect(self.export_csv)
        header_layout.addWidget(export_csv_btn)
        
        export_pdf_btn = QPushButton("📄 Generate PDF")
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4F46E5, stop:1 #6366F1);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
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
        export_pdf_btn.clicked.connect(self.generate_pdf)
        header_layout.addWidget(export_pdf_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)
        
        # Search
        search_label = QLabel("Search:")
        filters_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search equipment...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                min-width: 220px;
                background-color: #F8FAFC;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_data)
        filters_layout.addWidget(self.search_input)
        
        # CSV Upload filter
        csv_label = QLabel("CSV File:")
        csv_label.setStyleSheet("color: #334155; font-weight: 600;")
        filters_layout.addWidget(csv_label)
        
        self.csv_filter = QComboBox()
        self.csv_filter.setStyleSheet("""
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                min-width: 220px;
                background-color: #F8FAFC;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 2px solid #94A3B8;
            }
            QComboBox:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        self.csv_filter.currentTextChanged.connect(self.on_csv_filter_changed)
        filters_layout.addWidget(self.csv_filter)
        
        # Type filter
        type_label = QLabel("Type:")
        type_label.setStyleSheet("color: #334155; font-weight: 600;")
        filters_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.setStyleSheet("""
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #CBD5E1;
                border-radius: 8px;
                min-width: 170px;
                background-color: #F8FAFC;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 2px solid #94A3B8;
            }
            QComboBox:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        self.type_filter.currentTextChanged.connect(self.filter_data)
        filters_layout.addWidget(self.type_filter)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)
        
        # Data table with enhanced styling
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                background-color: white;
                gridline-color: #F1F5F9;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F1F5F9;
            }
            QTableWidget::item:selected {
                background-color: #EEF2FF;
                color: #4F46E5;
            }
            QTableWidget::item:alternate {
                background-color: #F8FAFC;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F1F5F9, stop:1 #E2E8F0);
                padding: 12px;
                border: none;
                border-bottom: 2px solid #CBD5E1;
                font-weight: bold;
                color: #0F172A;
                font-size: 13px;
            }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
    
    def load_data(self):
        """Load data from API."""
        # Load CSV uploads
        uploads_result = self.api_client.get_csv_uploads()
        if uploads_result['success']:
            self.csv_uploads = uploads_result['data']
            self.csv_filter.clear()
            self.csv_filter.addItem("All CSV Files")
            for upload in self.csv_uploads:
                filename = upload.get('filename', 'Unknown')
                total = upload.get('total_records', 0)
                self.csv_filter.addItem(f"{filename} ({total} records)", upload.get('id'))
        
        # Load equipment types
        types_result = self.api_client.get_equipment_types()
        if types_result['success']:
            self.equipment_types = types_result['data'].get('types', [])
            self.type_filter.clear()
            self.type_filter.addItem("All Types")
            for eq_type in self.equipment_types:
                self.type_filter.addItem(eq_type)
        
        # Load equipment data
        self.refresh_equipment_data()
    
    def refresh_equipment_data(self):
        """Refresh equipment data based on filters."""
        csv_upload_id = None
        if self.csv_filter.currentData():
            csv_upload_id = self.csv_filter.currentData()
        
        equipment_type = None
        if self.type_filter.currentText() != "All Types":
            equipment_type = self.type_filter.currentText()
        
        result = self.api_client.get_equipment(
            csv_upload_id=csv_upload_id,
            equipment_type=equipment_type
        )
        
        if result['success']:
            self.equipment_data = result['data']
            self.populate_table()
        else:
            QMessageBox.warning(self, "Error", f"Failed to load equipment data: {result.get('error', 'Unknown error')}")
    
    def on_csv_filter_changed(self):
        """Handle CSV filter change."""
        self.refresh_equipment_data()
    
    def filter_data(self):
        """Filter table data based on search term."""
        search_term = self.search_input.text().lower()
        
        if not search_term:
            self.populate_table()
            return
        
        filtered_data = [
            item for item in self.equipment_data
            if search_term in str(item.get('equipment_name', '')).lower() or
               search_term in str(item.get('equipment_id', '')).lower()
        ]
        
        self.populate_table(filtered_data)
    
    def populate_table(self, data=None):
        """Populate the table with equipment data."""
        if data is None:
            data = self.equipment_data
        
        if not data:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        
        # Get all unique keys (columns)
        exclude_fields = ['id', 'csv_upload_id', 'created_at', 'updated_at', 
                         'is_operational', 'needs_maintenance', 'additional_params']
        all_keys = set()
        for item in data:
            for key in item.keys():
                if key not in exclude_fields:
                    all_keys.add(key)
        
        # Sort columns: standard fields first
        standard_fields = ['equipment_name', 'equipment_type']
        columns = sorted(all_keys, key=lambda x: (
            standard_fields.index(x) if x in standard_fields else 999,
            x
        ))
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([self.format_column_name(col) for col in columns])
        
        # Populate data
        for row, item in enumerate(data):
            for col, column in enumerate(columns):
                value = item.get(column, '')
                if value is None:
                    value = 'N/A'
                elif isinstance(value, (int, float)):
                    value = str(value)
                else:
                    value = str(value)
                
                table_item = QTableWidgetItem(value)
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, table_item)
        
        # Resize columns
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
    
    def format_column_name(self, key: str) -> str:
        """Format column name for display."""
        return key.replace('_', ' ').title()
    
    def export_csv(self):
        """Export filtered data to CSV."""
        if not self.equipment_data:
            QMessageBox.warning(self, "No Data", "No equipment data to export.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "equipment_data.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                # Get columns
                exclude_fields = ['id', 'csv_upload_id', 'created_at', 'updated_at',
                                 'is_operational', 'needs_maintenance', 'additional_params']
                all_keys = set()
                for item in self.equipment_data:
                    for key in item.keys():
                        if key not in exclude_fields:
                            all_keys.add(key)
                
                standard_fields = ['equipment_name', 'equipment_type']
                columns = sorted(all_keys, key=lambda x: (
                    standard_fields.index(x) if x in standard_fields else 999,
                    x
                ))
                
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([self.format_column_name(col) for col in columns])
                    
                    for item in self.equipment_data:
                        row = [str(item.get(col, '')) for col in columns]
                        writer.writerow(row)
                
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export CSV: {str(e)}")
    
    def generate_pdf(self):
        """Generate PDF report."""
        equipment_type = None
        if self.type_filter.currentText() != "All Types":
            equipment_type = self.type_filter.currentText()
        
        result = self.api_client.generate_report(equipment_type=equipment_type)
        
        if result['success']:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                "equipment_report.pdf",
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(result['data'])
                    QMessageBox.information(self, "Success", f"PDF report saved to {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {result.get('error', 'Unknown error')}")
    
    def refresh(self):
        """Refresh visualization data."""
        if self.api_client.is_authenticated:
            self.load_data()


