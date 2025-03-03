#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main window for the Chinese Character Reading Application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAction, QMenu, 
    QMessageBox, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QFont, QKeyEvent, QMouseEvent

from core.character_manager import CharacterManager
from core.animation_engine import AnimationEngine
from core.speech_engine import SpeechEngine
from ui.settings_dialog import SettingsDialog
from ui.about_dialog import AboutDialog
from ui.font_dialog import FontDialog


class CharacterWidget(QWidget):
    """Widget for displaying animated Chinese characters."""
    
    def __init__(self, animation_engine, parent=None):
        """Initialize the character widget.
        
        Args:
            animation_engine: The animation engine.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.animation_engine = animation_engine
        self.animation_engine.animation_updated.connect(self.update)
        
        # Set focus policy to receive key events
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def paintEvent(self, event):
        """Handle paint event.
        
        Args:
            event: Paint event.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Clear background
        painter.fillRect(self.rect(), self.palette().window())
        
        # Render character animation
        self.animation_engine.render(painter, self.rect())
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events.
        
        Args:
            event (QMouseEvent): Mouse event.
        """
        if event.button() == Qt.LeftButton:
            main_window = self.window()  # 获取主窗口实例
            
            if hasattr(main_window, 're_pronounce_character'):
                main_window.re_pronounce_character()


class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self, config_manager):
        """Initialize the main window.
        
        Args:
            config_manager: The configuration manager.
        """
        super().__init__()
        self.config_manager = config_manager
        
        # Initialize core components
        self.character_manager = CharacterManager()
        self.animation_engine = AnimationEngine(config_manager)
        self.speech_engine = SpeechEngine(config_manager)
        
        # Connect animation engine signals
        self.animation_engine.animation_completed.connect(self.on_animation_completed)
        self.animation_engine.stroke_added.connect(self.on_stroke_added)
        
        # Set up the UI
        self.setup_ui()
        
        # Load initial character
        self.load_current_character()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Set window title
        self.setWindowTitle("小丕拾字")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create character display widget
        self.character_widget = CharacterWidget(self.animation_engine, self)
        layout.addWidget(self.character_widget)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Create menus
        self.create_menus()
    
    def create_menus(self):
        """Create application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Dict menu
        fonts_menu = self.menuBar().addMenu("&Dict")
        
        add_font_action = QAction("&Add Character", self)
        add_font_action.triggered.connect(self.show_font_dialog)
        fonts_menu.addAction(add_font_action)
        
        # Settings menu
        settings_menu = self.menuBar().addMenu("&Settings")
        
        settings_action = QAction("&Preferences", self)
        settings_action.triggered.connect(self.show_settings_dialog)
        settings_menu.addAction(settings_action)
        
        # About menu
        about_menu = self.menuBar().addMenu("&About")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)
    
    def keyPressEvent(self, event):
        """Handle key press events.
        
        Args:
            event (QKeyEvent): Key event.
        """
        if event.key() == Qt.Key_Up:
            self.show_previous_character()
        elif event.key() == Qt.Key_Down:
            self.show_next_character()
        else:
            super().keyPressEvent(event)
    
    def show_next_character(self):
        """Show the next character."""
        character = self.character_manager.next_character()
        self.update_character(character)
    
    def show_previous_character(self):
        """Show the previous character."""
        character = self.character_manager.previous_character()
        self.update_character(character)
    
    def load_current_character(self):
        """Load the current character."""
        character = self.character_manager.get_current_character()
        self.update_character(character)
    
    def update_character(self, character):
        """Update the displayed character.
        
        Args:
            character (str): Character to display.
        """
        if not character:
            return
        
        # Update status bar
        index = self.character_manager.get_current_index() + 1
        count = self.character_manager.get_character_count()
        self.statusBar().showMessage(f"Character {index} of {count}")
        
        # Pronounce the character
        self.speech_engine.pronounce(character)
        
        # Set character for animation
        self.animation_engine.set_character(character)
    
    def re_pronounce_character(self):
        """Re-pronounce the current character."""
        character = self.character_manager.get_current_character()
        if character:
            self.speech_engine.pronounce(character)
    
    @pyqtSlot()
    def on_animation_completed(self):
        """Handle animation completion."""
        # Animation sequence is complete
        pass
    
    @pyqtSlot()
    def on_stroke_added(self):
        """Handle new stroke added during animation."""
        # Pronounce the character when a new stroke is added
        if self.config_manager.get("auto_pronounce", True):
            character = self.character_manager.get_current_character()
            self.speech_engine.pronounce(character)
    
    def show_settings_dialog(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec_():
            # Reload character with new settings
            self.load_current_character()
    
    def show_font_dialog(self):
        """Show the font dialog."""
        dialog = FontDialog(self.character_manager, self)
        dialog.exec_()
    
    def show_about_dialog(self):
        """Show the about dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()
