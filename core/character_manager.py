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
    
    def add_character(self, character, group_name="基础汉字"):
        """添加新字符到指定分组
        
        Args:
            character (str): 要添加的汉字
            group_name (str): 目标分组名称，默认为"基础汉字"
            
        Returns:
            bool: 添加成功返回True，失败返回False
        """
        if not character:
            return False

        # 读取现有YAML数据
        with open(self.character_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {'groups': []}

        # 查找或创建目标分组
        target_group = next((g for g in data['groups'] if g['name'] == group_name), None)
        if not target_group:
            target_group = {'name': group_name, 'characters': []}
            data['groups'].append(target_group)

        # 检查字符是否已存在
        if any(c['character'] == character for c in target_group['characters']):
            return False

        # 添加新字符
        target_group['characters'].append({'character': character, 'words': []})
        
        # 更新内存数据
        self.characters.append(character)
        self.character_data[character] = {
            'group': group_name,
            'words': []
        }
        
        # 保存到YAML文件
        with open(self.character_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        
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
