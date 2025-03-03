#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Animation engine for the Chinese Character Reading Application.
Handles stroke animation and rendering using Make Me A Hanzi data.
"""

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush
import json
import re
import random

class StrokeInfo:
    """Stores information about a character stroke."""
    
    def __init__(self, path, visible=False):
        """Initialize a stroke.
        
        Args:
            path (QPainterPath): The path representing the stroke.
            visible (bool): Whether the stroke is visible.
        """
        self.path = path
        self.visible = visible


class AnimationEngine(QObject):
    """Manages character animation and rendering."""
    
    # Signal emitted when animation state changes
    animation_updated = pyqtSignal()
    # Signal emitted when animation sequence completes
    animation_completed = pyqtSignal()
    # Signal emitted when a new stroke is shown (for pronunciation)
    stroke_added = pyqtSignal()

    def __init__(self, config_manager):
        """Initialize the animation engine.
        
        Args:
            config_manager: The configuration manager.
        """
        super().__init__()
        self.config_manager = config_manager
        self.current_character = ""
        self.strokes = []
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_next_stroke)
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.start_stroke_animation)
        
        self.animation_count = 0
        self.target_animation_count = self.config_manager.get("animation_count", 3)
        self.is_animating = False
        self.background_path = QPainterPath()  # 添加背景路径存储

    def set_character(self, character):
        """Set the current character for animation.
        
        Args:
            character (str): The character to animate.
        """
        self.current_character = character
        self.reset_animation()
        self.prepare_strokes()
        
        # 构建背景路径
        self.background_path = QPainterPath()
        for stroke in self.strokes:
            self.background_path.addPath(stroke.path)
        # 填充背景路径为浅灰色
        self.background_path.setFillRule(Qt.WindingFill)
        
        self.animation_count = 0
        
        self.start_stroke_animation()
        # Signal to update the display
        self.animation_updated.emit()

    def load_hanzi_data(self, character):
        """Load stroke data from graphics.txt for a given character."""
        try:
            with open('assets/graphics.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line.strip())
                    if data.get('character') == character:
                        return data
            print(f"No data found for character '{character}' in graphics.txt")
            return None
        except Exception as e:
            print(f"Error loading graphics.txt: {e}")
            return None

    def parse_svg_path(self, path_string):
        """Parse SVG path string into a QPainterPath with original coordinates."""
        path = QPainterPath()
        commands = re.findall(r'([MLQCZ])\s*([-\d.,\s]*)', path_string)
        
        for cmd, args_str in commands:
            args = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', args_str)]
            if cmd == 'M' and len(args) >= 2:
                path.moveTo(args[0], args[1])
            elif cmd == 'L' and len(args) >= 2:
                path.lineTo(args[0], args[1])
            elif cmd == 'Q' and len(args) >= 4:
                path.quadTo(args[0], args[1], args[2], args[3])
            elif cmd == 'C' and len(args) >= 6:
                path.cubicTo(args[0], args[1], args[2], args[3], args[4], args[5])
            elif cmd == 'Z':
                path.closeSubpath()
        return path

    def prepare_strokes(self):
        """Prepare stroke paths for the current character using Make Me A Hanzi data."""
        self.strokes = []
        
        if not self.current_character:
            return
        
        hanzi_data = self.load_hanzi_data(self.current_character)
        if not hanzi_data or 'strokes' not in hanzi_data:
            print(f"No stroke data available for '{self.current_character}'")
            return
        
        for stroke in hanzi_data['strokes']:
            path = self.parse_svg_path(stroke)
            if not path.isEmpty():
                self.strokes.append(StrokeInfo(path, False))
        
        print(f"Prepared {len(self.strokes)} strokes for '{self.current_character}'")

    def reset_animation(self):
        """Reset the animation state."""
        self.animation_timer.stop()
        self.display_timer.stop()
        self.is_animating = False
        
        # Reset all strokes to invisible
        for stroke in self.strokes:
            stroke.visible = False

    def start_stroke_animation(self):
        """Start the stroke animation sequence."""
        self.is_animating = True
        self.display_timer.stop()
        
        # Increment animation count
        self.animation_count += 1
        
        if self.animation_count > self.target_animation_count:
            # Animation sequence complete
            self.animation_completed.emit()
            return  # 结束动画，不再重置笔画可见性
        
        # Reset all strokes to invisible
        for stroke in self.strokes:
            stroke.visible = False
        
        # Start animation timer
        interval = self.config_manager.get("animation_interval", 1000)
        self.animation_timer.start(interval)
        
        # Signal to update the display
        self.animation_updated.emit()

    def animate_next_stroke(self):
        """
            Animate the next stroke in sequence.
            connected with timer, after time out, execute automatically.
        """
        # Find the next invisible stroke
        for stroke in self.strokes:
            if not stroke.visible:
                stroke.visible = True
                self.stroke_added.emit()
                self.animation_updated.emit()
                return
        
        # All strokes are visible, end of sequence
        self.animation_timer.stop()
        
        self.is_animating = False
        # Start next animation round after a delay
        for stroke in self.strokes:
            stroke.visible = False  # 这里可以选择重置可见性，True则保持为笔画着色
        
        # Set the aftertaste time after all strokes are displayed, 
        # and then re-display this/next the Chinese character animation.
        self.display_timer.start(self.config_manager.get("display_time", 3000))

    def render(self, painter, rect):
        """Render the current animation state.
        
        Args:
            painter (QPainter): The painter to render with.
            rect (QRect): The rectangle to render in.
        """
        if not self.strokes:
            return
        
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        
        # ==== 核心坐标系调整 ====
        scale = min(rect.width(), rect.height()) * 0.9  # 使用90%的窗口空间
        offset_x = rect.width() / 2
        offset_y = rect.height() / 2
        
        # 坐标系变换
        painter.translate(offset_x, offset_y)          # 原点移到绘制区域中心
        painter.scale(scale / 1024, -scale / 1024)    # Y轴翻转并缩放
        painter.translate(-512, -412)                # 中心对齐原始坐标系，根据控件微调
        
        # 填充背景路径为浅灰色
        painter.fillPath(self.background_path, QColor(210, 210, 210))  # 浅灰色填充
        
        # 设置绘制样式
        stroke_color = QColor(self.config_manager.get_stroke_color())
        brush = QBrush(stroke_color)  # 创建填充笔刷
        painter.setBrush(brush)  # 设置填充笔刷
        
        # 绘制可见笔画
        for stroke in self.strokes:
            if stroke.visible:
                painter.drawPath(stroke.path)  # 使用填充笔刷绘制路径
        
        painter.restore()