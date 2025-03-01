#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Font dialog for the Chinese Character Reading Application.
Allows adding new characters to the character set.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QListWidget,
    QMessageBox
)

class FontDialog(QDialog):
    """Dialog for managing Chinese characters."""
    
    def __init__(self, character_manager, parent=None):
        """Initialize the font dialog.
        
        Args:
            character_manager: The character manager.
            parent: The parent widget.
        """
        super().__init__(parent)
        self.character_manager = character_manager
        
        self.setWindowTitle("Character Management")
        self.resize(400, 500)
        
        self.setup_ui()
        self.load_characters()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Add character section
        add_layout = QHBoxLayout()
        
        self.char_input = QLineEdit()
        self.char_input.setMaxLength(1)  # Allow only one character at a time
        self.char_input.setPlaceholderText("Enter a Chinese character")
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_character)
        
        add_layout.addWidget(self.char_input)
        add_layout.addWidget(add_button)
        
        layout.addLayout(add_layout)
        
        # Character list
        list_label = QLabel("Current Characters:")
        layout.addWidget(list_label)
        
        self.char_list = QListWidget()
        layout.addWidget(self.char_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_character)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(remove_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_characters(self):
        """Load current characters into the list."""
        self.char_list.clear()
        for char in self.character_manager.characters:
            self.char_list.addItem(char)
    
    def add_character(self):
        """Add a new character to the list."""
        character = self.char_input.text().strip()
        
        if not character:
            QMessageBox.warning(self, "Warning", "Please enter a character.")
            return
            
        # Check if it's a valid Chinese character
        if not self._is_chinese_character(character):
            QMessageBox.warning(self, "Warning", "Please enter a valid Chinese character.")
            return
            
        if character in self.character_manager.characters:
            QMessageBox.information(self, "Information", 
                                  f"Character '{character}' already exists.")
            return
            
        # Add the character
        self.character_manager.add_character(character)
        
        # Refresh the list
        self.load_characters()
        
        # Clear the input
        self.char_input.clear()
    
    def remove_character(self):
        """Remove the selected character from the list."""
        selected_items = self.char_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a character to remove.")
            return
            
        character = selected_items[0].text()
        
        # Confirm removal
        confirm = QMessageBox.question(
            self, "Confirm Removal",
            f"Are you sure you want to remove '{character}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Remove the character
            self.character_manager.characters.remove(character)
            self.character_manager.save_characters()
            
            # Refresh the list
            self.load_characters()
    
    def _is_chinese_character(self, char):
        """Check if a character is a Chinese character.
        
        Args:
            char (str): The character to check.
            
        Returns:
            bool: True if it's a Chinese character.
        """
        if not char or len(char) != 1:
            return False
            
        # Unicode ranges for Chinese characters
        code_point = ord(char)
        
        # CJK Unified Ideographs (Basic)
        if 0x4E00 <= code_point <= 0x9FFF:
            return True
            
        # CJK Unified Ideographs Extension A
        if 0x3400 <= code_point <= 0x4DBF:
            return True
            
        # CJK Unified Ideographs Extension B
        if 0x20000 <= code_point <= 0x2A6DF:
            return True
            
        # CJK Unified Ideographs Extension C
        if 0x2A700 <= code_point <= 0x2B73F:
            return True
            
        # CJK Unified Ideographs Extension D
        if 0x2B740 <= code_point <= 0x2B81F:
            return True
            
        # CJK Unified Ideographs Extension E
        if 0x2B820 <= code_point <= 0x2CEAF:
            return True
            
        return False
