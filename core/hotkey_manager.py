"""
Hotkey management - handles key mappings and parsing
"""

import string
from typing import Dict, List


class HotkeyManager:
    """Manages hotkey mappings and parsing logic"""
    
    def __init__(self, platform: str):
        self.platform = platform
        self._setup_key_mappings()
        self._setup_presets()
    
    def _setup_key_mappings(self) -> None:
        """Define key mappings for pyautogui"""
        self.special_keys = {
            # Letters and numbers
            **{letter: letter.lower() for letter in string.ascii_uppercase},
            **{str(num): str(num) for num in range(10)},
            
            # Function keys
            **{f'F{i}': f'f{i}' for i in range(1, 13)},
            
            # Navigation
            'UP': 'up', 'DOWN': 'down', 'LEFT': 'left', 'RIGHT': 'right',
            'HOME': 'home', 'END': 'end', 'PGUP': 'pageup', 'PGDN': 'pagedown',
            
            # Editing
            'BACKSPACE': 'backspace', 'DELETE': 'delete', 'INSERT': 'insert',
            'TAB': 'tab', 'ENTER': 'enter', 'SPACE': 'space', 'ESC': 'esc',
            
            # Symbols
            'PLUS': '+', 'MINUS': '-', 'EQUALS': '=',
            
            # Modifiers
            'SHIFT': 'shift', 'CTRL': 'ctrl', 'ALT': 'alt',
            'WIN': 'win', 'CMD': 'command',
        }
    
    def _setup_presets(self) -> None:
        """Define common hotkey presets"""
        self.presets = [
            "CTRL+C", "CTRL+V", "CTRL+X", "CTRL+Z", "CTRL+A", "CTRL+F",
            "CTRL+S", "CTRL+W", "CTRL+N", "CTRL+T",
            "ALT+F4", "WIN+R", "WIN+E", "WIN+D",
            "CTRL+ALT+DELETE", "CTRL+ALT+T"
        ]
    
    def parse_hotkey(self, hotkey_str: str) -> List[str]:
        """Parse hotkey string into pyautogui key list"""
        if '+' not in hotkey_str:
            # Single key
            return [self.special_keys.get(hotkey_str.upper(), hotkey_str.lower())]
        
        # Multiple keys
        parts = [part.strip().upper() for part in hotkey_str.split('+')]
        return [self.special_keys.get(part, part.lower()) for part in parts]
    
    def get_modifier_name(self, modifier: str) -> str:
        """Get platform-specific modifier name"""
        if modifier.upper() == 'WIN' and self.platform == 'Darwin':
            return 'CMD'
        return modifier.upper()
    
    def get_available_keys(self) -> Dict[str, List[str]]:
        """Get categorized available keys"""
        return {
            'letters': list(string.ascii_uppercase),
            'function_keys': [f'F{i}' for i in range(1, 13)],
            'navigation': ['UP', 'DOWN', 'LEFT', 'RIGHT', 'HOME', 'END', 'PGUP', 'PGDN'],
            'editing': ['BACKSPACE', 'DELETE', 'INSERT', 'TAB', 'ENTER', 'SPACE', 'ESC'],
            'modifiers': ['CTRL', 'ALT', 'SHIFT', self.get_modifier_name('WIN')]
        }