#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings dialog for the Chinese Character Reading Application.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QCheckBox, QComboBox,
    QSpinBox, QColorDialog, QGroupBox, QFontComboBox
)

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""
    
    def __init__(self, config_manager, parent=None):
        """Initialize the settings dialog.
        
        Args:
            config_manager: The configuration manager.
            parent: The parent widget.
        """
        super().__init__(parent)
        self.config_manager = config_manager
        
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Stroke Color Group
        color_group = QGroupBox("Stroke Color")
        color_layout = QGridLayout()
        
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(50, 30)
        self.color_preview.clicked.connect(self.select_color)
        
        self.mixed_color_checkbox = QCheckBox("Use Mixed Colors")
        
        color_layout.addWidget(QLabel("Stroke Color:"), 0, 0)
        color_layout.addWidget(self.color_preview, 0, 1)
        color_layout.addWidget(self.mixed_color_checkbox, 1, 0, 1, 2)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Font Settings Group
        font_group = QGroupBox("Font Settings")
        font_layout = QGridLayout()
        
        # Font family
        self.font_combo = QFontComboBox()
        # Filter to show only Chinese character supporting fonts
        self.font_combo.setWritingSystem(QFontDatabase.SimplifiedChinese)
        
        # Font size
        font_size_layout = QHBoxLayout()
        
        self.decrease_size_btn = QPushButton("A-")
        self.decrease_size_btn.setFixedSize(40, 30)
        self.decrease_size_btn.clicked.connect(self.decrease_font_size)
        
        self.font_size_label = QLabel("120")
        self.font_size_label.setAlignment(Qt.AlignCenter)
        
        self.increase_size_btn = QPushButton("A+")
        self.increase_size_btn.setFixedSize(40, 30)
        self.increase_size_btn.clicked.connect(self.increase_font_size)
        
        font_size_layout.addWidget(self.decrease_size_btn)
        font_size_layout.addWidget(self.font_size_label)
        font_size_layout.addWidget(self.increase_size_btn)
        
        font_layout.addWidget(QLabel("Font:"), 0, 0)
        font_layout.addWidget(self.font_combo, 0, 1)
        font_layout.addWidget(QLabel("Font Size:"), 1, 0)
        font_layout.addLayout(font_size_layout, 1, 1)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # Animation Settings Group
        animation_group = QGroupBox("Animation Settings")
        animation_layout = QGridLayout()
        
        # Animation count
        self.animation_count_spin = QSpinBox()
        self.animation_count_spin.setMinimum(1)
        self.animation_count_spin.setMaximum(10)
        
        # Animation interval
        self.animation_interval_spin = QSpinBox()
        self.animation_interval_spin.setMinimum(100)
        self.animation_interval_spin.setMaximum(5000)
        self.animation_interval_spin.setSingleStep(100)
        self.animation_interval_spin.setSuffix(" ms")
        
        # Display time
        self.display_time_spin = QSpinBox()
        self.display_time_spin.setMinimum(1000)
        self.display_time_spin.setMaximum(10000)
        self.display_time_spin.setSingleStep(500)
        self.display_time_spin.setSuffix(" ms")
        
        animation_layout.addWidget(QLabel("Animation Count:"), 0, 0)
        animation_layout.addWidget(self.animation_count_spin, 0, 1)
        animation_layout.addWidget(QLabel("Animation Interval:"), 1, 0)
        animation_layout.addWidget(self.animation_interval_spin, 1, 1)
        animation_layout.addWidget(QLabel("Display Time:"), 2, 0)
        animation_layout.addWidget(self.display_time_spin, 2, 1)
        
        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)
        
        # Audio Settings Group
        audio_group = QGroupBox("Audio Settings")
        audio_layout = QVBoxLayout()
        
        self.auto_pronounce_checkbox = QCheckBox("Auto-pronounce Characters")
        
        audio_layout.addWidget(self.auto_pronounce_checkbox)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """Load current settings into UI controls."""
        # Stroke color
        color = self.config_manager.get_stroke_color()
        self._update_color_preview(color)
        
        # Mixed color
        self.mixed_color_checkbox.setChecked(
            self.config_manager.get("is_mixed_color", False)
        )
        
        # Font family
        font_family = self.config_manager.get("font_family", "SimHei")
        index = self.font_combo.findText(font_family)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)
        
        # Font size
        font_size = self.config_manager.get("font_size", 400)
        self.font_size_label.setText(str(font_size))
        
        # Animation count
        self.animation_count_spin.setValue(
            self.config_manager.get("animation_count", 3)
        )
        
        # Animation interval
        self.animation_interval_spin.setValue(
            self.config_manager.get("animation_interval", 1000)
        )
        
        # Display time
        self.display_time_spin.setValue(
            self.config_manager.get("display_time", 3000)
        )
        
        # Auto pronounce
        self.auto_pronounce_checkbox.setChecked(
            self.config_manager.get("auto_pronounce", True)
        )
    
    def save_settings(self):
        """Save settings and close dialog."""
        # Font family
        self.config_manager.set("font_family", self.font_combo.currentText())
        
        # Font size
        font_size = int(self.font_size_label.text())
        self.config_manager.set("font_size", font_size)
        
        # Stroke color is set in select_color()
        
        # Mixed color
        self.config_manager.set("is_mixed_color", self.mixed_color_checkbox.isChecked())
        
        # Animation count
        self.config_manager.set("animation_count", self.animation_count_spin.value())
        
        # Animation interval
        self.config_manager.set("animation_interval", self.animation_interval_spin.value())
        
        # Display time
        self.config_manager.set("display_time", self.display_time_spin.value())
        
        # Auto pronounce
        self.config_manager.set("auto_pronounce", self.auto_pronounce_checkbox.isChecked())
        
        self.accept()
    
    def select_color(self):
        """Open color dialog to select stroke color."""
        current_color = self.config_manager.get_stroke_color()
        color = QColorDialog.getColor(current_color, self, "Select Stroke Color")
        
        if color.isValid():
            self._update_color_preview(color)
            self.config_manager.set_stroke_color(color)
    
    def _update_color_preview(self, color):
        """Update the color preview button.
        
        Args:
            color (QColor): The color to preview.
        """
        self.color_preview.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #888;"
        )
    
    def increase_font_size(self):
        """Increase the font size."""
        current_size = int(self.font_size_label.text())
        new_size = min(current_size + 20, 700)  # Maximum 700
        self.font_size_label.setText(str(new_size))
    
    def decrease_font_size(self):
        """Decrease the font size."""
        current_size = int(self.font_size_label.text())
        new_size = max(current_size - 10, 30)  # Minimum 30
        self.font_size_label.setText(str(new_size))