#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Animation engine for the Chinese Character Reading Application.
Handles stroke animation and rendering.
"""

from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QFont
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
        self.is_hollow = True
        self.is_animating = False
    
    def set_character(self, character):
        """Set the current character for animation.
        
        Args:
            character (str): The character to animate.
        """
        self.current_character = character
        self.reset_animation()
        self.prepare_strokes()
        
        # Start with hollow display
        self.is_hollow = True
        self.animation_count = 0
        
        # Schedule start of animation after display time
        self.display_timer.start(self.config_manager.get("display_time", 3000))
        
        # Signal to update the display
        self.animation_updated.emit()
    
    def prepare_strokes(self):
        """Prepare stroke paths for the current character."""
        # This is a simplified method of stroke extraction
        # In a real application, you would use a stroke database or font information
        
        self.strokes = []
        
        if not self.current_character:
            return
        
        # For demonstration purposes, we'll create artificial strokes
        # In a real app, you would use HanLP, OpenCC, or similar libraries to get real stroke data
        
        # Get font metrics
        font = QFont(
            self.config_manager.get("font_family", "SimHei"),
            self.config_manager.get("font_size", 400)
        )
        
        # This is just a placeholder - in a real app you'd have proper stroke data
        # Here we're just dividing the character into artificial "strokes"
        char_path = QPainterPath()
        char_path.addText(0, 0, font, self.current_character)
        
        # Simulate 3-8 strokes per character
        stroke_count = random.randint(3, 8)
        
        # Create artificial strokes by dividing the bounding rect
        bounds = char_path.boundingRect()
        width = bounds.width()
        height = bounds.height()
        
        for i in range(stroke_count):
            stroke_path = QPainterPath()
            
            # Create a small sub-rectangle representing a "stroke"
            x = bounds.x() + (i * width / stroke_count)
            y = bounds.y() + (i * height / stroke_count)
            w = width / stroke_count
            h = height / stroke_count
            
            # Add part of the character to this "stroke"
            stroke_path.addRect(x, y, w, h)
            stroke_path = char_path.intersected(stroke_path)
            
            if not stroke_path.isEmpty():
                self.strokes.append(StrokeInfo(stroke_path, False))
    
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
        self.is_hollow = False
        
        # Reset all strokes to invisible
        for stroke in self.strokes:
            stroke.visible = False
        
        # Start animation timer
        interval = self.config_manager.get("animation_interval", 1000)
        self.animation_timer.start(interval)
        
        # Signal to update the display
        self.animation_updated.emit()
    
    def animate_next_stroke(self):
        """Animate the next stroke in sequence."""
        # Find the next invisible stroke
        for stroke in self.strokes:
            if not stroke.visible:
                stroke.visible = True
                self.stroke_added.emit()
                self.animation_updated.emit()
                return
        
        # All strokes are visible, end of sequence
        self.animation_timer.stop()
        
        # Increment animation count
        self.animation_count += 1
        
        if self.animation_count >= self.target_animation_count:
            # Animation sequence complete
            self.is_animating = False
            self.animation_completed.emit()
        else:
            # Start next animation round after a delay
            self.is_hollow = True
            for stroke in self.strokes:
                stroke.visible = False
            
            self.animation_updated.emit()
            self.display_timer.start(self.config_manager.get("display_time", 3000))
    
    def render(self, painter, rect):
        """Render the current animation state.
        
        Args:
            painter (QPainter): The painter to render with.
            rect (QRect): The rectangle to render in.
        """
        if not self.current_character:
            return
        
        # Set up font
        font = QFont(
            self.config_manager.get("font_family", "SimHei"),
            self.config_manager.get("font_size", 400)
        )
        painter.setFont(font)
        
        # Create the full character path
        char_path = QPainterPath()
        char_path.addText(rect.center().x(), rect.center().y(), font, self.current_character)
        
        # Center the character
        bounds = char_path.boundingRect()
        painter.translate(
            rect.center().x() - bounds.center().x(),
            rect.center().y() - bounds.center().y()
        )
        
        # Draw the hollow outline
        painter.setPen(self.config_manager.get_stroke_color())
        painter.setBrush(painter.background())
        painter.drawPath(char_path)
        
        # If not in hollow mode, draw the visible strokes
        if not self.is_hollow:
            # Set up fill color
            if self.config_manager.get("is_mixed_color", False):
                # Use different colors for each stroke
                colors = []
                base_color = self.config_manager.get_stroke_color()
                for _ in range(len(self.strokes)):
                    h = (base_color.hue() + random.randint(-30, 30)) % 360
                    s = min(max(base_color.saturation() + random.randint(-30, 30), 0), 255)
                    v = min(max(base_color.value() + random.randint(-30, 30), 0), 255)
                    colors.append(base_color.convertTo(QColor.Hsv).setHsv(h, s, v))
            else:
                # Use a single color for all strokes
                colors = [self.config_manager.get_stroke_color()] * len(self.strokes)
            
            # Draw each visible stroke
            for i, stroke in enumerate(self.strokes):
                if stroke.visible:
                    painter.setPen(colors[i % len(colors)])
                    painter.setBrush(colors[i % len(colors)])
                    painter.drawPath(stroke.path)
