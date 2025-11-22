"""
Dashboard tab with statistics and charts.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


class StatsCard(QFrame):
    """Widget for displaying a statistic card."""
    
    def __init__(self, title: str, value: str, unit: str = "", color: str = "#4F46E5", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        # Create gradient background based on color
        color_map = {
            "#4F46E5": ("#4F46E5", "#6366F1", "#818CF8"),
            "#06B6D4": ("#06B6D4", "#0891B2", "#22D3EE"),
            "#F97316": ("#F97316", "#FB923C", "#FDBA74"),
            "#A855F7": ("#A855F7", "#C084FC", "#D8B4FE"),
        }
        gradient_colors = color_map.get(color, ("#4F46E5", "#6366F1", "#818CF8"))
        
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {gradient_colors[0]}, stop:0.5 {gradient_colors[1]}, stop:1 {gradient_colors[2]});
                border: none;
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 13px;
            font-weight: 500;
        """)
        layout.addWidget(title_label)
        
        value_layout = QHBoxLayout()
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: white;")
        value_layout.addWidget(value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                font-weight: 500;
            """)
            value_layout.addWidget(unit_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)


class DashboardTab(QWidget):
    """Dashboard tab showing overview statistics and charts."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
        # Don't load data immediately - wait for authentication
        # Data will be loaded after user logs in
    
    def setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with enhanced styling
        header = QLabel("📊 Dashboard Overview")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0F172A; padding: 5px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Real-time monitoring of chemical equipment parameters")
        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
            padding-bottom: 5px;
        """)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Stats Cards
        self.stats_layout = QGridLayout()
        self.stats_layout.setSpacing(15)
        
        self.total_equipment_card = StatsCard("📦 Total Equipment", "0", color="#4F46E5")
        self.avg_flowrate_card = StatsCard("💧 Avg Flowrate", "0.0", "L/min", color="#06B6D4")
        self.avg_pressure_card = StatsCard("🔧 Avg Pressure", "0.0", "PSI", color="#F97316")
        self.avg_temperature_card = StatsCard("🌡️ Avg Temperature", "0.0", "°C", color="#A855F7")
        
        self.stats_layout.addWidget(self.total_equipment_card, 0, 0)
        self.stats_layout.addWidget(self.avg_flowrate_card, 0, 1)
        self.stats_layout.addWidget(self.avg_pressure_card, 0, 2)
        self.stats_layout.addWidget(self.avg_temperature_card, 0, 3)
        
        layout.addLayout(self.stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Equipment Distribution Chart
        self.type_dist_chart = MatplotlibChart("Equipment Distribution", "By equipment type")
        charts_layout.addWidget(self.type_dist_chart)
        
        # Flowrate Chart
        self.flowrate_chart = MatplotlibChart("Top Flowrate Equipment", "Flowrate by equipment")
        charts_layout.addWidget(self.flowrate_chart)
        
        layout.addLayout(charts_layout)
        
        layout.addStretch()
    
    def load_data(self):
        """Load dashboard data from API."""
        # Load summary
        summary_result = self.api_client.get_dashboard_summary()
        if summary_result['success']:
            summary = summary_result['data']
            
            # Update stats cards
            total = summary.get('total_equipment', 0) or 0
            self.update_card(self.total_equipment_card, str(total))
            
            avg_flowrate = summary.get('avg_flowrate', 0) or 0
            self.update_card(self.avg_flowrate_card, f"{avg_flowrate:.1f}")
            
            avg_pressure = summary.get('avg_pressure', 0) or 0
            self.update_card(self.avg_pressure_card, f"{avg_pressure:.1f}")
            
            avg_temp = summary.get('avg_temperature', 0) or 0
            self.update_card(self.avg_temperature_card, f"{avg_temp:.1f}")
        
        # Load type distribution
        type_result = self.api_client.get_type_distribution_data()
        if type_result['success']:
            data = type_result['data']
            types = data.get('types', [])
            counts = data.get('counts', [])
            self.type_dist_chart.plot_bar(types, counts)
        
        # Load flowrate data
        flowrate_result = self.api_client.get_flowrate_chart_data()
        if flowrate_result['success']:
            data = flowrate_result['data']
            equipment_ids = data.get('equipment_ids', [])[:10]  # Top 10
            flowrates = data.get('flowrates', [])[:10]
            self.flowrate_chart.plot_line(equipment_ids, flowrates)
    
    def update_card(self, card: StatsCard, value: str):
        """Update a stats card value."""
        layout = card.layout()
        value_layout = layout.itemAt(1).layout()
        value_label = value_layout.itemAt(0).widget()
        value_label.setText(value)
    
    def refresh(self):
        """Refresh dashboard data."""
        if self.api_client.is_authenticated:
            self.load_data()


class MatplotlibChart(QWidget):
    """Widget for displaying matplotlib charts."""
    
    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(380)
        
        # Chart container with styled background
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                padding: 5px;
            }
        """)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0F172A; padding: 5px;")
        chart_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #64748B; font-size: 12px; padding-bottom: 5px;")
        chart_layout.addWidget(subtitle_label)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(6, 4), facecolor='#FAFBFC')
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        
        # Set chart_frame as the main widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(chart_frame)
    
    def plot_bar(self, categories: list, values: list):
        """Plot a bar chart with enhanced colors."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#FAFBFC')
        
        if categories and values:
            # Use gradient colors for bars
            colors = ['#4F46E5', '#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE']
            bars = ax.bar(categories, values, color=colors[:len(categories)], 
                         edgecolor='white', linewidth=2, alpha=0.9)
            ax.set_xlabel('Equipment Type', fontsize=11, fontweight='bold', color='#334155')
            ax.set_ylabel('Count', fontsize=11, fontweight='bold', color='#334155')
            ax.tick_params(axis='x', rotation=45, labelsize=10, colors='#475569')
            ax.tick_params(axis='y', labelsize=10, colors='#475569')
            ax.grid(True, alpha=0.2, linestyle='--', color='#CBD5E1')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E2E8F0')
            ax.spines['bottom'].set_color('#E2E8F0')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_line(self, x_data: list, y_data: list):
        """Plot a line chart with enhanced colors."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#FAFBFC')
        
        if x_data and y_data:
            ax.plot(x_data, y_data, marker='o', color='#06B6D4', linewidth=3, 
                   markersize=8, markerfacecolor='#22D3EE', markeredgecolor='white', 
                   markeredgewidth=2, alpha=0.9)
            ax.fill_between(x_data, y_data, alpha=0.2, color='#06B6D4')
            ax.set_xlabel('Equipment ID', fontsize=11, fontweight='bold', color='#334155')
            ax.set_ylabel('Flowrate (L/min)', fontsize=11, fontweight='bold', color='#334155')
            ax.tick_params(axis='x', rotation=45, labelsize=10, colors='#475569')
            ax.tick_params(axis='y', labelsize=10, colors='#475569')
            ax.grid(True, alpha=0.2, linestyle='--', color='#CBD5E1')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E2E8F0')
            ax.spines['bottom'].set_color('#E2E8F0')
        
        self.figure.tight_layout()
        self.canvas.draw()

