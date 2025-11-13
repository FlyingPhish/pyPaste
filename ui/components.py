"""
Reusable UI component factory - eliminates repetitive UI code
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable, Any


class UIComponentFactory:
    """Factory for creating common UI components with consistent styling"""
    
    @staticmethod
    def create_labeled_frame(parent: tk.Widget, text: str, 
                           padx: int = 5, pady: int = 5) -> tk.LabelFrame:
        """Create a labeled frame with consistent styling"""
        frame = tk.LabelFrame(parent, text=text, padx=padx, pady=pady)
        return frame
    
    @staticmethod
    def create_button_grid(parent: tk.Widget, buttons_config: List[Dict],
                          columns: int = 9) -> Dict[str, tk.Button]:
        """Create a grid of buttons from configuration"""
        buttons = {}
        row, col = 0, 0
        
        for config in buttons_config:
            button = tk.Button(
                parent,
                text=config['text'],
                width=config.get('width', 3),
                command=config['command']
            )
            button.grid(row=row, column=col, padx=2, pady=2)
            buttons[config['text']] = button
            
            col += 1
            if col >= columns:
                col = 0
                row += 1
        
        return buttons
    
    @staticmethod
    def create_entry_with_label(parent: tk.Widget, label_text: str,
                               default_value: str = "", width: int = 10) -> tuple[tk.Label, tk.Entry]:
        """Create label and entry pair"""
        label = tk.Label(parent, text=label_text)
        entry = tk.Entry(parent, width=width)
        if default_value:
            entry.insert(0, default_value)
        return label, entry
    
    @staticmethod
    def create_checkbox_group(parent: tk.Widget, 
                             checkboxes: List[Dict]) -> Dict[str, tk.BooleanVar]:
        """Create a group of checkboxes"""
        vars_dict = {}
        
        for cb_config in checkboxes:
            var = tk.BooleanVar(value=cb_config.get('default', False))
            checkbox = tk.Checkbutton(
                parent, 
                text=cb_config['text'],
                variable=var
            )
            checkbox.pack(side=tk.LEFT, padx=5)
            vars_dict[cb_config['key']] = var
        
        return vars_dict
    
    @staticmethod
    def create_dropdown(parent: tk.Widget, values: List[str],
                       default: str = "", width: int = 20) -> ttk.Combobox:
        """Create a dropdown combobox"""
        combo = ttk.Combobox(parent, values=values, width=width, state='readonly')
        if default in values:
            combo.set(default)
        elif values:
            combo.set(values[0])
        return combo
    
    @staticmethod
    def create_button_row(parent: tk.Widget, 
                         buttons: List[Dict]) -> List[tk.Button]:
        """Create a row of buttons"""
        button_widgets = []
        
        for btn_config in buttons:
            btn = tk.Button(
                parent,
                text=btn_config['text'],
                command=btn_config['command'],
                width=btn_config.get('width', 10)
            )
            btn.pack(side=tk.LEFT, padx=5)
            button_widgets.append(btn)
        
        return button_widgets
    
    @staticmethod
    def create_listbox_with_scrollbar(parent: tk.Widget, 
                                     height: int = 10) -> tuple[tk.Listbox, tk.Scrollbar]:
        """Create listbox with scrollbar"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=height)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=listbox.yview)
        
        return listbox, scrollbar


class FormValidator:
    """Simple form validation utilities"""
    
    @staticmethod
    def validate_float(value: str, min_val: float = 0, max_val: float = 60) -> tuple[bool, Optional[float]]:
        """Validate float input"""
        try:
            num = float(value)
            if min_val <= num <= max_val:
                return True, num
            return False, None
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_required(value: str) -> bool:
        """Validate required field"""
        return bool(value.strip())