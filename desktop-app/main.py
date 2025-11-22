"""
Main entry point for the desktop application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from main_window import MainWindow


def main():
    """Run the desktop application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better appearance
    
    # Set application properties
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("ChemViz")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

