"""
Horizontal layout frames - optimized for wide screens
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional, Dict, List
import string

from ui.components import UIComponentFactory, FormValidator
from core.hotkey_manager import HotkeyManager
from core.history_manager import HistoryManager


class HorizontalInputFrame(tk.LabelFrame):
    """Compact input frame for horizontal layout"""
    
    def __init__(self, parent: tk.Widget, send_callback: Callable, default_delay: float = 2):
        super().__init__(parent, text="Text Input", padx=5, pady=5)
        self.send_callback = send_callback
        self._setup_ui(default_delay)
    
    def _setup_ui(self, default_delay: float) -> None:
        """Setup compact vertical input UI"""
        # Text input
        tk.Label(self, text="Enter text:").pack(anchor=tk.W, pady=(0, 5))
        
        self.text_area = tk.Text(self, height=8, width=25, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Delay control
        delay_frame = tk.Frame(self)
        delay_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(delay_frame, text="Delay:").pack(side=tk.LEFT)
        self.delay_entry = tk.Entry(delay_frame, width=5)
        self.delay_entry.insert(0, str(default_delay))
        self.delay_entry.pack(side=tk.LEFT, padx=(5, 5))
        tk.Label(delay_frame, text="sec").pack(side=tk.LEFT)
        
        # Send button
        tk.Button(self, text="Send Text", command=self._send_text, 
                 bg='lightgreen', width=20).pack(fill=tk.X, pady=(0, 5))
        
        # Quick actions
        tk.Label(self, text="Quick Keys:").pack(anchor=tk.W, pady=(10, 5))
        
        quick_frame = tk.Frame(self)
        quick_frame.pack(fill=tk.X)
        
        quick_keys = [('ENTER', 'Enter'), ('TAB', 'Tab'), ('ESC', 'Esc')]
        for key, label in quick_keys:
            tk.Button(quick_frame, text=label, width=8,
                     command=lambda k=key: self._quick_send(k)).pack(side=tk.LEFT, padx=1)
    
    def _send_text(self) -> None:
        """Validate and send text"""
        text = self.text_area.get(1.0, tk.END).strip()
        delay = self.get_delay()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to send")
            return
        
        if delay is None:
            messagebox.showerror("Error", "Invalid delay time")
            return
        
        self.send_callback(text, delay)
        self.text_area.delete(1.0, tk.END)
    
    def _quick_send(self, key: str) -> None:
        """Quick send a single key"""
        delay = 0.5  # Quick delay for single keys
        # This would need to be connected to hotkey sending
        # For now, just add to text area
        current_text = self.text_area.get(1.0, tk.END).strip()
        key_name = {'ENTER': '\n', 'TAB': '\t', 'ESC': '[ESC]'}.get(key, key)
        self.text_area.insert(tk.END, key_name)
    
    def get_delay(self) -> Optional[float]:
        """Get validated delay value"""
        valid, delay = FormValidator.validate_float(self.delay_entry.get(), 0, 60)
        return delay if valid else None
    
    def set_text(self, text: str) -> None:
        """Set text in text area"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, text)


class HorizontalHotkeyFrame(tk.LabelFrame):
    """Compact hotkey frame for horizontal layout"""
    
    def __init__(self, parent: tk.Widget, hotkey_manager: HotkeyManager, 
                 send_callback: Callable):
        super().__init__(parent, text="Hotkeys", padx=5, pady=5)
        self.hotkey_manager = hotkey_manager
        self.send_callback = send_callback
        self.selected_key = None
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup compact hotkey UI"""
        # Common shortcuts at top
        tk.Label(self, text="Common:").pack(anchor=tk.W, pady=(0, 5))
        
        common_frame = tk.Frame(self)
        common_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Most used shortcuts
        # Select specific important presets from hotkey manager
        important_presets = ["CTRL+C", "CTRL+V", "CTRL+Z", "ALT+F4", "WIN+R", "CTRL+ALT+DELETE"]
        common = [preset for preset in self.hotkey_manager.presets if preset in important_presets]
        row, col = 0, 0
        for shortcut in common:
            btn = tk.Button(common_frame, text=shortcut, width=8,
                           command=lambda s=shortcut: self._send_preset(s))
            btn.grid(row=row, column=col, padx=1, pady=1, sticky='ew')
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        # Configure column weights
        for i in range(3):
            common_frame.columnconfigure(i, weight=1)
        
        # Custom builder
        tk.Label(self, text="Custom:").pack(anchor=tk.W, pady=(10, 5))
        
        # Modifiers
        mod_frame = tk.Frame(self)
        mod_frame.pack(fill=tk.X, pady=(0, 5))
        
        modifier_config = [
            {'key': 'ctrl', 'text': 'CTRL'},
            {'key': 'alt', 'text': 'ALT'},
            {'key': 'shift', 'text': 'SHIFT'},
            {'key': 'win', 'text': self.hotkey_manager.get_modifier_name('WIN')}
        ]
        self.modifier_vars = {}
        for config in modifier_config:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(mod_frame, text=config['text'], variable=var)
            cb.pack(side=tk.LEFT)
            self.modifier_vars[config['key']] = var
        
        # Key selection dropdown
        key_frame = tk.Frame(self)
        key_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(key_frame, text="Key:").pack(side=tk.LEFT)
        
        # Combine all available keys
        all_keys = (list(string.ascii_uppercase) + 
                   [f'F{i}' for i in range(1, 13)] +
                   ['TAB', 'ENTER', 'ESC', 'SPACE', 'UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        self.key_combo = ttk.Combobox(key_frame, values=all_keys, width=8, state='readonly')
        self.key_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.key_combo.bind('<<ComboboxSelected>>', self._key_selected)
        
        # Preview
        preview_frame = tk.Frame(self)
        preview_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(preview_frame, text="Preview:").pack(side=tk.LEFT)
        self.preview_var = tk.StringVar()
        tk.Label(preview_frame, textvariable=self.preview_var, 
                relief=tk.SUNKEN, width=15, bg='white').pack(side=tk.LEFT, padx=(5, 0))
        
        # Send custom
        tk.Button(self, text="Send Custom", command=self._send_custom,
                 bg='lightblue', width=20).pack(fill=tk.X)
    
    def _key_selected(self, event=None) -> None:
        """Handle key selection"""
        self._update_preview()
    
    def _update_preview(self) -> None:
        """Update hotkey preview"""
        selected_key = self.key_combo.get()
        if not selected_key:
            self.preview_var.set("")
            return
        
        modifiers = []
        for mod_key, var in self.modifier_vars.items():
            if var.get():
                modifiers.append(mod_key.upper())
        
        combo = "+".join(modifiers + [selected_key])
        self.preview_var.set(combo)
    
    def _send_preset(self, preset: str) -> None:
        """Send preset hotkey"""
        self.send_callback(preset, 1.0)
    
    def _send_custom(self) -> None:
        """Send custom hotkey"""
        combo = self.preview_var.get()
        if not combo:
            messagebox.showwarning("Warning", "Please select a hotkey combination")
            return
        
        self.send_callback(combo, 2.0)


class HorizontalHistoryFrame(tk.LabelFrame):
    """Compact history frame for horizontal layout"""
    
    def __init__(self, parent: tk.Widget, history_manager: HistoryManager,
                 resend_callback: Callable):
        super().__init__(parent, text="History", padx=5, pady=5)
        self.history_manager = history_manager
        self.resend_callback = resend_callback
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup compact history UI"""
        # Listbox
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.listbox = tk.Listbox(list_frame, height=12)
        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons - vertical layout
        button_configs = [
            ('Resend', self._resend_selected, 'lightgreen'),
            ('Copy', self._copy_selected, 'lightblue'),
            ('Delete', self._delete_selected, 'lightcoral'),
            ('Toggle', self._toggle_selected, 'lightyellow'),
            ('Clear All', self._clear_all, 'lightgray')
        ]
        
        for text, command, color in button_configs:
            btn = tk.Button(self, text=text, command=command, 
                           bg=color, width=15)
            btn.pack(fill=tk.X, pady=1)
    
    def _get_selected_index(self) -> Optional[int]:
        """Get selected item index"""
        selection = self.listbox.curselection()
        return selection[0] if selection else None
    
    def _resend_selected(self) -> None:
        """Resend selected item"""
        index = self._get_selected_index()
        if index is not None:
            item_data = self.history_manager.get_item_data(index)
            if item_data:
                self.resend_callback(item_data)
        else:
            messagebox.showinfo("Info", "No item selected")
    
    def _copy_selected(self) -> None:
        """Copy selected item to clipboard"""
        index = self._get_selected_index()
        if index is not None:
            item = self.history_manager.get_item(index)
            if item:
                self.master.clipboard_clear()
                self.master.clipboard_append(item.content)
        else:
            messagebox.showinfo("Info", "No item selected")
    
    def _delete_selected(self) -> None:
        """Delete selected item"""
        index = self._get_selected_index()
        if index is not None:
            if self.history_manager.delete_item(index):
                self.refresh()
        else:
            messagebox.showinfo("Info", "No item selected")
    
    def _toggle_selected(self) -> None:
        """Toggle selected item visibility"""
        index = self._get_selected_index()
        if index is not None:
            if self.history_manager.toggle_visibility(index):
                self.refresh()
    
    def _clear_all(self) -> None:
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.history_manager.clear()
            self.refresh()
    
    def refresh(self) -> None:
        """Refresh listbox display"""
        self.listbox.delete(0, tk.END)
        for item_text in self.history_manager.get_display_items():
            self.listbox.insert(tk.END, item_text)