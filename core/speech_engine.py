#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Speech engine for the Chinese Character Reading Application.
Handles text-to-speech functionality.
"""

from PyQt5.QtCore import QObject, QLocale
from PyQt5.QtTextToSpeech import QTextToSpeech

class SpeechEngine(QObject):
    """Manages text-to-speech functionality."""
    
    def __init__(self, config_manager):
        """Initialize the speech engine.
        
        Args:
            config_manager: The configuration manager.
        """
        super().__init__()
        self.config_manager = config_manager
        
        # Initialize text-to-speech engine
        self.speech = QTextToSpeech()
        self.setup_speech()
    
    def setup_speech(self):
        """Set up the speech engine with available voices."""
        # Find a Chinese voice if available
        voices = self.speech.availableVoices()
        chinese_voice = None
        
        for voice in voices:
            # Check if the locale method exists
            if hasattr(voice, 'locale'):
                locale = voice.locale()
                if locale.language() == QLocale.Chinese:
                    chinese_voice = voice
                    break
            else:
                # Handle the case where locale method does not exist
                print(f"Voice {voice.name()} does not have a locale method.")
        
        if chinese_voice:
            self.speech.setVoice(chinese_voice)
        
        # Set speech rate
        self.speech.setRate(0.0)  # Normal rate
        
        # Set volume
        self.speech.setVolume(1.0)  # Maximum volume
    
    def pronounce(self, text):
        """Pronounce the given text.
        
        Args:
            text (str): The text to pronounce.
        """
        if not self.config_manager.get("auto_pronounce", True):
            return
            
        if text and not self.is_speaking():
            self.speech.say(text)
    
    def stop(self):
        """Stop the current pronunciation."""
        if self.is_speaking():
            self.speech.stop()
    
    def is_speaking(self):
        """Check if the speech engine is currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise.
        """
        return self.speech.state() == QTextToSpeech.Speaking

    def mute(self):
        """Mute the speech engine."""
        self.speech.setVolume(0.0)

    def unmute(self):
        """Unmute the speech engine."""
        self.speech.setVolume(1.0)
