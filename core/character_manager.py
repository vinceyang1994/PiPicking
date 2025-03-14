#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Character manager for the Chinese Character Reading Application.
Handles loading, storing, and accessing Chinese characters.
"""

import os
import random

class CharacterManager:
    """Manages Chinese character data for the application."""
    
    def __init__(self, character_file="characters.txt"):
        """Initialize the character manager.
        
        Args:
            character_file (str): Path to the character file.
        """
        self.character_file = character_file
        self.characters = []
        self.current_index = 0
        self.original_characters = []  # 保存原始顺序
        self.load_characters()
    
    def load_characters(self):
        """Load characters from the character file."""
        if not os.path.exists(self.character_file):
            # Create empty file if it doesn't exist
            with open(self.character_file, 'w', encoding='utf-8') as f:
                f.write("一\n二\n三\n四\n五\n六\n七\n八\n九\n十")
        
        try:
            with open(self.character_file, 'r', encoding='utf-8') as f:
                self.characters = [line.strip() for line in f if line.strip()]
                self.original_characters = self.characters.copy()  # 保存原始顺序
        except IOError:
            print(f"Error loading character file.")
            self.characters = ["一", "二", "三", "四", "五"]
            self.original_characters = self.characters.copy()
        
        # Reset current index
        self.current_index = 0
    
    def save_characters(self):
        """Save characters to the character file."""
        try:
            with open(self.character_file, 'w', encoding='utf-8') as f:
                for char in self.characters:
                    f.write(f"{char}\n")
        except IOError:
            print(f"Error saving character file.")
    
    def get_current_character(self):
        """Get the currently selected character.
        
        Returns:
            str: The current character or empty string if no characters.
        """
        if not self.characters:
            return ""
        
        return self.characters[self.current_index]
    
    def next_character(self):
        """Move to the next character and return it.
        
        Returns:
            str: The next character or empty string if no characters.
        """
        if not self.characters:
            return ""
        
        self.current_index = (self.current_index + 1) % len(self.characters)
        return self.get_current_character()
    
    def previous_character(self):
        """Move to the previous character and return it.
        
        Returns:
            str: The previous character or empty string if no characters.
        """
        if not self.characters:
            return ""
        
        self.current_index = (self.current_index - 1) % len(self.characters)
        return self.get_current_character()
    
    def add_character(self, character):
        """Add a new character to the list.
        
        Args:
            character (str): Character to add.
            
        Returns:
            bool: True if added successfully, False otherwise.
        """
        if not character or character in self.characters:
            return False
        
        self.characters.append(character)
        self.save_characters()
        return True
    
    def get_character_count(self):
        """Get the total number of characters.
        
        Returns:
            int: Number of characters.
        """
        return len(self.characters)
    
    def get_current_index(self):
        """Get the current character index.
        
        Returns:
            int: Current index.
        """
        return self.current_index
    
    def get_random_character(self):
        """获取一个随机汉字
        
        Returns:
            str: 随机选择的汉字，如果列表为空则返回空字符串
        """
        if not self.characters:
            return ""
        
        return random.choice(self.characters)

    def shuffle_characters(self):
        """将字符列表随机打乱（考试模式）"""
        random.shuffle(self.characters)
        self.current_index = 0  # 重置索引

    def restore_order(self):
        """恢复字符列表原始顺序（学习模式）"""
        self.characters = self.original_characters.copy()
        self.current_index = 0  # 重置索引
