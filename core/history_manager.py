"""
History management - handles storage and display of sent items
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    TEXT = "text"
    HOTKEY = "hotkey"


@dataclass
class HistoryItem:
    """Represents a history item"""
    content: str
    type: ItemType
    visible: bool = True
    
    def display_text(self) -> str:
        """Get display text for UI"""
        if self.type == ItemType.HOTKEY:
            return f"[HOTKEY] {self.content}"
        return self.content if self.visible else '*' * len(self.content)


class HistoryManager:
    """Manages history of sent items"""
    
    def __init__(self, obfuscate_by_default: bool = True):
        self.items: List[HistoryItem] = []
        self.obfuscate_by_default = obfuscate_by_default
    
    def add_text(self, text: str) -> None:
        """Add text to history"""
        item = HistoryItem(
            content=text,
            type=ItemType.TEXT,
            visible=not self.obfuscate_by_default
        )
        self.items.append(item)
    
    def add_hotkey(self, hotkey: str) -> None:
        """Add hotkey to history"""
        item = HistoryItem(
            content=hotkey,
            type=ItemType.HOTKEY,
            visible=True  # Hotkeys are always visible
        )
        self.items.append(item)
    
    def get_item(self, index: int) -> Optional[HistoryItem]:
        """Get item by index"""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def delete_item(self, index: int) -> bool:
        """Delete item by index"""
        if 0 <= index < len(self.items):
            del self.items[index]
            return True
        return False
    
    def toggle_visibility(self, index: int) -> bool:
        """Toggle item visibility"""
        item = self.get_item(index)
        if item and item.type == ItemType.TEXT:
            item.visible = not item.visible
            return True
        return False
    
    def toggle_all_visibility(self) -> None:
        """Toggle all text items visibility"""
        text_items = [item for item in self.items if item.type == ItemType.TEXT]
        if not text_items:
            return
        
        # Determine action based on majority state
        hidden_count = sum(1 for item in text_items if not item.visible)
        reveal_all = hidden_count > len(text_items) / 2
        
        for item in text_items:
            item.visible = reveal_all
    
    def get_display_items(self) -> List[str]:
        """Get list of display strings for UI"""
        return [item.display_text() for item in self.items]
    
    def get_item_data(self, index: int) -> Optional[Dict]:
        """Get item data for operations"""
        item = self.get_item(index)
        if item:
            return {
                'content': item.content,
                'type': item.type.value
            }
        return None
    
    def clear(self) -> None:
        """Clear all history"""
        self.items.clear()
    
    def __len__(self) -> int:
        return len(self.items)