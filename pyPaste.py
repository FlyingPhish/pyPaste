#!/usr/bin/env python3
"""
pyPaste - Horizontal layout version
Optimized for wide screens with better space utilization
"""

import tkinter as tk
from tkinter import messagebox, ttk
import pyautogui
import platform
from typing import List, Dict, Optional, Callable

from core.hotkey_manager import HotkeyManager
from core.history_manager import HistoryManager
from ui.components import UIComponentFactory
from ui.frames import HorizontalInputFrame, HorizontalHotkeyFrame, HorizontalHistoryFrame


class PyPasteHorizontalApp:
    """Main application with horizontal layout"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("pyPaste")
        self._setup_window()
        
        # Core components
        self.hotkey_manager = HotkeyManager(platform.system())
        self.history_manager = HistoryManager()
        
        # UI setup
        self._setup_ui()
        self._setup_status_bar()
    
    def _setup_window(self) -> None:
        """Configure main window for horizontal layout"""
        self.root.geometry('900x450')  # Wider, shorter
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (450 // 2)
        self.root.geometry(f'900x450+{x}+{y}')
    
    def _setup_ui(self) -> None:
        """Setup horizontal UI layout"""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Input and quick actions
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Middle column - Hotkeys
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column - History
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Setup frames
        self.input_frame = HorizontalInputFrame(
            left_frame, 
            send_callback=self._send_text,
            default_delay=2
        )
        self.input_frame.pack(fill=tk.BOTH, expand=True)
        
        self.hotkey_frame = HorizontalHotkeyFrame(
            middle_frame,
            self.hotkey_manager,
            send_callback=self._send_hotkey
        )
        self.hotkey_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_frame = HorizontalHistoryFrame(
            right_frame,
            self.history_manager,
            resend_callback=self._resend_from_history
        )
        self.history_frame.pack(fill=tk.BOTH, expand=True)
    
    def _setup_status_bar(self) -> None:
        """Setup status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var,
            bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _send_text(self, text: str, delay: float) -> None:
        """Send text with delay"""
        if not text.strip():
            self._show_status("No text to send")
            return
            
        self._show_status(f"Sending text in {delay} seconds...")
        self.history_manager.add_text(text)
        self.history_frame.refresh()
        
        self.root.after(int(delay * 1000), lambda: self._execute_text_input(text))
    
    def _send_hotkey(self, hotkey_combo: str, delay: float) -> None:
        """Send hotkey combination with delay"""
        if not hotkey_combo:
            self._show_status("No hotkey selected")
            return
            
        self._show_status(f"Sending hotkey {hotkey_combo} in {delay} seconds...")
        self.history_manager.add_hotkey(hotkey_combo)
        self.history_frame.refresh()
        
        keys = self.hotkey_manager.parse_hotkey(hotkey_combo)
        self.root.after(int(delay * 1000), lambda: self._execute_hotkey(keys, hotkey_combo))
    
    def _execute_text_input(self, text: str) -> None:
        """Execute text typing"""
        try:
            self.root.iconify()
            pyautogui.typewrite(text)
            self.root.after(500, self.root.deiconify)
            self._show_status("Text sent successfully")
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Failed to send text: {e}")
            self._show_status("Error sending text")
    
    def _execute_hotkey(self, keys: List[str], hotkey_str: str) -> None:
        """Execute hotkey combination"""
        try:
            self.root.iconify()
            if len(keys) == 1:
                pyautogui.press(keys[0])
            else:
                pyautogui.hotkey(*keys)
            self.root.after(500, self.root.deiconify)
            self._show_status(f"Hotkey {hotkey_str} sent successfully")
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Failed to send hotkey: {e}")
            self._show_status("Error sending hotkey")
    
    def _resend_from_history(self, item: Dict) -> None:
        """Resend item from history"""
        delay = 1.0  # Quick resend
        
        if item['type'] == 'text':
            self._send_text(item['content'], delay)
            self.input_frame.set_text(item['content'])
        elif item['type'] == 'hotkey':
            self._send_hotkey(item['content'], delay)
    
    def _show_status(self, message: str) -> None:
        """Update status bar"""
        self.status_var.set(message)


def main():
    """Application entry point"""
    root = tk.Tk()
    app = PyPasteHorizontalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()