#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration manager for the Chinese Character Reading Application.
Handles loading and saving configuration settings.
"""

import json
import os
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, pyqtSignal

class ConfigManager(QObject):
    """Manages application configuration settings."""
    
    DEFAULT_CONFIG = {
        "stroke_color": "#FF0000",  # Default red color
        "is_mixed_color": False,    # Single color by default
        "font_size": 400,           # Default font size
        "font_family": "SimHei",    # Default font
        "animation_count": 3,       # Default number of animations
        "animation_interval": 1000, # Default animation interval in ms
        "display_time": 3000,       # Time to display character before animation (ms)
        "auto_pronounce": True,     # Auto-pronounce new characters
        "background_brightness": 100,  # Default background brightness
        "window_state": "maximized"  # Default window state
    }
    
    config_updated = pyqtSignal()  # 新增信号
    
    def __init__(self, config_file="config.json"):
        """Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        super().__init__()
        self.config_file = config_file
        self.config = self._load_config()
        self.update_background()  # 添加初始背景设置
    
    def _load_config(self):
        """Load configuration from file or create default if not exists.
        
        Returns:
            dict: The configuration settings.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading config file. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Save configuration to file.
        
        Args:
            config (dict, optional): Configuration to save. Defaults to current config.
        """
        if config is not None:
            self.config = config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Error saving config file.")
    
    def get(self, key, default=None):
        """Get a configuration value.
        
        Args:
            key (str): Configuration key.
            default: Default value if key not found.
            
        Returns:
            The configuration value or default.
        """
        return self.config.get(key, default)
    
    def set(self, key, value, temporary=False):
        """Set a configuration value and save.
        
        Args:
            key (str): Configuration key.
            value: Value to set.
            temporary: Whether the change is temporary (not saved to file)
        """
        self.config[key] = value
        if not temporary:
            self.save_config()
        self.config_updated.emit()
    
    def get_stroke_color(self):
        """Get the stroke color as a QColor object.
        
        Returns:
            QColor: The stroke color.
        """
        return QColor(self.get("stroke_color", "#FF0000"))
    
    def set_stroke_color(self, color):
        """Set the stroke color from a QColor object.
        
        Args:
            color (QColor): The color to set.
        """
        self.set("stroke_color", color.name())
    
    def get_background_brightness(self):
        return self.get("background_brightness", 100)
    
    def set_background_brightness(self, value):
        self.set("background_brightness", value)

    def update_background(self):
        # Implementation of update_background method
        pass

    def get_window_state(self):
        return self.get("window_state", "maximized")
    
    def set_window_state(self, state):
        self.set("window_state", state)
