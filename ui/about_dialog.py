#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About dialog for the Chinese Character Reading Application.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton
)

class AboutDialog(QDialog):
    """Dialog displaying information about the application."""
    
    def __init__(self, parent=None):
        """Initialize the about dialog.
        
        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        
        self.setWindowTitle("About Chinese Character Reading App")
        self.setFixedSize(500, 300)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Application title
        title_label = QLabel("Chinese Character Reading App")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Version
        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignCenter)
        
        # Description
        description = """
        <p>The Chinese Character Reading App is designed to help children learn 
        Chinese characters through visual animations and pronunciation.</p>
        
        <p>Features include:</p>
        <ul>
          <li>Stroke-by-stroke character animation</li>
          <li>Text-to-speech pronunciation</li>
          <li>Customizable display settings</li>
          <li>Character management</li>
        </ul>
        
        <p>© 2025 Chinese Character Learning Project</p>
        """
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc_label.setTextFormat(Qt.RichText)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()