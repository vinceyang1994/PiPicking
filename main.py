#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Chinese Character Reading Application.
"""

import sys
import main

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config_manager import ConfigManager


def main():
    """Initialize and run the application."""
    # Create the application
    app = QApplication(sys.argv)
    
    # Initialize configuration
    config_manager = ConfigManager()
    
    # Create and show the main window
    main_window = MainWindow(config_manager)
    main_window.showMaximized()
    
    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
