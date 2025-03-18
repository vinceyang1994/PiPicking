#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Character manager for the Chinese Character Reading Application.
Handles loading, storing, and accessing Chinese characters.
"""

import os
import random
import yaml

class CharacterManager:
    """Manages Chinese character data for the application."""
    
    def __init__(self, character_file="characters.yaml"):
        """Initialize the character manager.
        
        Args:
            character_file (str): Path to the character file.
        """
        self.character_file = character_file
        self.characters = []
        self.character_data = {}  # 新增属性
        self.current_index = 0
        self.original_characters = []  # 保存原始顺序
        self.load_characters()
    
    def load_characters(self):
        """Load characters from the YAML character file."""
        if not os.path.exists(self.character_file):
            # 创建示例YAML文件
            sample_data = {
                'groups': [
                    {
                        'name': '基础汉字',
                        'characters': [
                            {'character': '一', 'words': []},
                            {'character': '二', 'words': []}
                        ]
                    }
                ]
            }
            with open(self.character_file, 'w', encoding='utf-8') as f:
                yaml.dump(sample_data, f, allow_unicode=True)

        try:
            with open(self.character_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            # 提取所有字符并保持原始顺序
            self.characters = []
            self.character_data = {}  # 新增数据结构存储完整信息
            for group in data['groups']:
                for char_info in group['characters']:
                    char = char_info['character']
                    if char not in self.character_data:
                        self.characters.append(char)
                        self.character_data[char] = {
                            'group': group['name'],
                            'words': char_info['words']
                        }
            
            self.original_characters = self.characters.copy()
            
        except (IOError, yaml.YAMLError) as e:
            print(f"Error loading character file: {str(e)}")
            self.characters = ["一", "二", "三"]
            self.original_characters = self.characters.copy()
        
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
        
        if self.current_index < len(self.characters) - 1:
            self.current_index += 1
        return self.get_current_character()
    
    def previous_character(self):
        """Move to the previous character and return it.
        
        Returns:
            str: The previous character or empty string if no characters.
        """
        if not self.characters:
            return ""
        
        if self.current_index > 0:
            self.current_index -= 1
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

    def get_current_character_info(self):
        """获取当前字符的完整信息"""
        char = self.get_current_character()
        return self.character_data.get(char, {})
