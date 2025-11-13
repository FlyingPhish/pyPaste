#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk
import pyautogui
import platform

class StringSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pyPaste")
        
        # Set up platform-specific configurations
        self.platform = platform.system()
        print(f"Running on {self.platform}")
        
        # Store real and display state
        self.history = []  # List to store actual text history
        self.history_display_state = []  # List to track if entries are obfuscated (True) or visible (False)
        self.obfuscate_by_default = True  # Default obfuscation setting
        
        # Define special key mappings
        self.setup_key_mappings()
        
        # Main Frame for input and sending
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup UI components
        self.setup_input_frame()
        self.setup_hotkey_frame()
        self.setup_history_frame()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_key_mappings(self):
        """Define mappings for special keys"""
        # Mapping user-friendly names to pyautogui key names
        self.special_keys = {
            # Basic function keys
            'F1': 'f1', 'F2': 'f2', 'F3': 'f3', 'F4': 'f4', 'F5': 'f5',
            'F6': 'f6', 'F7': 'f7', 'F8': 'f8', 'F9': 'f9', 'F10': 'f10',
            'F11': 'f11', 'F12': 'f12',
            
            # Navigation keys
            'UP': 'up', 'DOWN': 'down', 'LEFT': 'left', 'RIGHT': 'right',
            'HOME': 'home', 'END': 'end', 'PGUP': 'pageup', 'PGDN': 'pagedown',
            
            # Editing keys
            'BACKSPACE': 'backspace', 'DELETE': 'delete', 'INSERT': 'insert',
            'TAB': 'tab', 'ENTER': 'enter', 'SPACE': 'space', 'ESC': 'esc',
            
            # Special symbols
            'PLUS': '+', 'MINUS': '-', 'EQUALS': '=',
            
            # Modifier keys
            'SHIFT': 'shift', 'CTRL': 'ctrl', 'ALT': 'alt',
            'WIN': 'win', 'CMD': 'command',  # Windows/Mac keys
        }
        
        # Limited preset shortcuts as requested
        self.shortcut_presets = ["CTRL+ALT+DELETE", "WIN+R"]
    
    def setup_input_frame(self):
        # Text Input Section
        input_frame = tk.LabelFrame(self.main_frame, text="Text Input", padx=5, pady=5)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input label
        input_label = tk.Label(input_frame, text="Enter text to send:")
        input_label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        
        # Text entry and controls frame
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(fill=tk.X)
        
        # Text Entry
        self.text_entry = tk.Entry(entry_frame, width=50)
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Delay label
        delay_label = tk.Label(entry_frame, text="Delay (s):")
        delay_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Delay Entry
        self.delay_var = tk.StringVar(value='2')  # Default delay of 2 seconds
        self.delay_entry = tk.Entry(entry_frame, textvariable=self.delay_var, width=5)
        self.delay_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Send Button
        self.send_button = tk.Button(entry_frame, text="Send Text", command=self.send_text)
        self.send_button.pack(side=tk.LEFT)
    
    def setup_hotkey_frame(self):
        # Hotkey Section
        hotkey_frame = tk.LabelFrame(self.main_frame, text="Hotkey Shortcuts", padx=5, pady=5)
        hotkey_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Preset buttons frame
        presets_frame = tk.Frame(hotkey_frame)
        presets_frame.pack(fill=tk.X, pady=5)
        
        # Add preset buttons
        for shortcut in self.shortcut_presets:
            button = tk.Button(
                presets_frame, 
                text=shortcut, 
                command=lambda s=shortcut: self.send_preset_hotkey(s),
                width=15,
                height=2
            )
            button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Custom hotkey frame
        custom_frame = tk.LabelFrame(hotkey_frame, text="Custom Hotkey", padx=5, pady=5)
        custom_frame.pack(fill=tk.X, pady=5)
        
        # Modifier checkboxes in a row
        modifier_frame = tk.Frame(custom_frame)
        modifier_frame.pack(fill=tk.X, pady=5)
        
        self.ctrl_var = tk.BooleanVar(value=False)
        ctrl_check = tk.Checkbutton(modifier_frame, text="CTRL", variable=self.ctrl_var)
        ctrl_check.pack(side=tk.LEFT, padx=5)
        
        self.alt_var = tk.BooleanVar(value=False)
        alt_check = tk.Checkbutton(modifier_frame, text="ALT", variable=self.alt_var)
        alt_check.pack(side=tk.LEFT, padx=5)
        
        self.shift_var = tk.BooleanVar(value=False)
        shift_check = tk.Checkbutton(modifier_frame, text="SHIFT", variable=self.shift_var)
        shift_check.pack(side=tk.LEFT, padx=5)
        
        self.win_var = tk.BooleanVar(value=False)
        win_label = "CMD" if self.platform == "Darwin" else "WIN"
        win_check = tk.Checkbutton(modifier_frame, text=win_label, variable=self.win_var)
        win_check.pack(side=tk.LEFT, padx=5)
        
        # Key selection frame
        key_frame = tk.Frame(custom_frame)
        key_frame.pack(fill=tk.X, pady=5)
        
        key_label = tk.Label(key_frame, text="Key:")
        key_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Dropdown with common keys
        self.key_var = tk.StringVar()
        common_keys = sorted(list(self.special_keys.keys()))
        key_dropdown = ttk.Combobox(key_frame, textvariable=self.key_var, values=common_keys, width=10)
        key_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Send custom hotkey button
        send_custom_button = tk.Button(custom_frame, text="Send Custom Hotkey", command=self.send_custom_hotkey)
        send_custom_button.pack(fill=tk.X, pady=5)
    
    def setup_history_frame(self):
        # History section
        self.history_frame = tk.LabelFrame(self.main_frame, text="History (Obfuscated by Default)")
        self.history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Option frame with checkbox for obfuscation setting
        options_frame = tk.Frame(self.history_frame)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Obfuscation checkbox
        self.obfuscate_var = tk.BooleanVar(value=self.obfuscate_by_default)
        self.obfuscate_checkbox = tk.Checkbutton(
            options_frame, 
            text="Obfuscate new entries", 
            variable=self.obfuscate_var,
            command=self.update_obfuscation_setting
        )
        self.obfuscate_checkbox.pack(side=tk.LEFT)
        
        # History list and buttons in side-by-side frame
        list_buttons_frame = tk.Frame(self.history_frame)
        list_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # History Listbox with scrollbar
        listbox_frame = tk.Frame(list_buttons_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(listbox_frame, width=50, yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # History buttons frame
        buttons_frame = tk.Frame(list_buttons_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # History action buttons
        self.resend_button = tk.Button(buttons_frame, text="Resend", command=self.resend_string)
        self.resend_button.pack(fill=tk.X, pady=2)
        
        self.copy_button = tk.Button(buttons_frame, text="Copy", command=self.copy_string)
        self.copy_button.pack(fill=tk.X, pady=2)
        
        self.delete_button = tk.Button(buttons_frame, text="Delete", command=self.delete_string)
        self.delete_button.pack(fill=tk.X, pady=2)
        
        self.reveal_button = tk.Button(buttons_frame, text="Reveal", command=self.deobfuscate_string)
        self.reveal_button.pack(fill=tk.X, pady=2)
        
        self.hide_button = tk.Button(buttons_frame, text="Hide", command=self.obfuscate_string)
        self.hide_button.pack(fill=tk.X, pady=2)
        
        self.toggle_all_button = tk.Button(buttons_frame, text="Toggle All", command=self.toggle_all_entries)
        self.toggle_all_button.pack(fill=tk.X, pady=2)
    
    def update_obfuscation_setting(self):
        """Update the obfuscation setting based on checkbox state"""
        self.obfuscate_by_default = self.obfuscate_var.get()
        status = "enabled" if self.obfuscate_by_default else "disabled"
        self.show_status(f"Default obfuscation {status}")
    
    def send_preset_hotkey(self, hotkey_str):
        """Send a preset hotkey combination"""
        if not hotkey_str:
            return
            
        delay_time = self.get_delay_time()
        if delay_time is None:
            messagebox.showerror("Error", "Invalid delay time. Please enter a valid number.")
            return
        
        keys = self.parse_hotkey(hotkey_str)
        
        # Add to history
        history_entry = f"[HOTKEY] {hotkey_str}"
        self.add_to_history(history_entry)
        
        self.show_status(f"Sending hotkey {hotkey_str} after delay: {delay_time} seconds...")
        self.root.after(int(delay_time * 1000), lambda: self.execute_hotkey(keys, hotkey_str))
    
    def send_custom_hotkey(self):
        """Send a custom hotkey combination based on selections"""
        modifiers = []
        if self.ctrl_var.get(): modifiers.append("CTRL")
        if self.alt_var.get(): modifiers.append("ALT")
        if self.shift_var.get(): modifiers.append("SHIFT")
        if self.win_var.get(): modifiers.append("WIN" if self.platform != "Darwin" else "CMD")
        
        key = self.key_var.get()
        
        if not key and not modifiers:
            self.show_status("No hotkey specified")
            return
            
        hotkey_str = "+".join(modifiers)
        if key:
            if hotkey_str:
                hotkey_str += "+"
            hotkey_str += key
        
        # Parse the hotkey and send it
        keys = self.parse_hotkey(hotkey_str)
        
        delay_time = self.get_delay_time()
        if delay_time is None:
            messagebox.showerror("Error", "Invalid delay time. Please enter a valid number.")
            return
        
        # Add to history
        history_entry = f"[HOTKEY] {hotkey_str}"
        self.add_to_history(history_entry)
        
        self.show_status(f"Sending hotkey {hotkey_str} after delay: {delay_time} seconds...")
        self.root.after(int(delay_time * 1000), lambda: self.execute_hotkey(keys, hotkey_str))
    
    def parse_hotkey(self, hotkey_str):
        """Parse a hotkey string into a list of keys for pyautogui"""
        if not hotkey_str:
            return []
            
        keys = []
        parts = hotkey_str.split("+")
        
        for part in parts:
            # Map the key to its pyautogui equivalent if it exists
            key = self.special_keys.get(part, part)
            keys.append(key)
            
        return keys
    
    def execute_hotkey(self, keys, hotkey_str):
        """Execute the hotkey combination"""
        try:
            # Minimize app window and let user focus on target
            self.root.iconify()
            
            # Wait a moment before sending keys
            self.root.after(500, lambda: self.press_hotkey(keys, hotkey_str))
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.show_status("Error sending hotkey")
    
    def press_hotkey(self, keys, hotkey_str):
        """Actually press the hotkey combination"""
        try:
            pyautogui.hotkey(*keys)
            self.root.after(500, self.root.deiconify)
            self.show_status(f"Hotkey {hotkey_str} sent successfully")
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.show_status("Error sending hotkey")
    
    def send_text(self):
        """Get the input string and send it after a delay"""
        input_string = self.text_entry.get()
        if not input_string:
            self.show_status("Error: No text to send")
            return
            
        delay_time = self.get_delay_time()
        if delay_time is None:
            messagebox.showerror("Error", "Invalid delay time. Please enter a valid number.")
            return
        
        self.add_to_history(input_string)
        self.show_status(f"Sending text after delay: {delay_time} seconds...")
        self.root.after(int(delay_time * 1000), lambda: self.type_string(input_string))
    
    def get_delay_time(self):
        """Parse and validate the delay time"""
        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                return None
            return delay
        except ValueError:
            return None
    
    def type_string(self, string):
        """Use pyautogui to type the string"""
        # Check if this is a hotkey entry
        if string.startswith("[HOTKEY] "):
            hotkey_str = string.replace("[HOTKEY] ", "")
            keys = self.parse_hotkey(hotkey_str)
            self.execute_hotkey(keys, hotkey_str)
            return
        
        try:
            # Bring focus to the window where typing should happen
            self.root.iconify()  # Minimize app window
            # Give time for user to focus the target window
            self.root.after(500, lambda: self.execute_typing(string))
        except Exception as e:
            self.root.deiconify()  # Restore app window
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.show_status("Error while sending keys")
    
    def execute_typing(self, string):
        """Actually execute the typing action"""
        try:
            pyautogui.typewrite(string)
            self.root.after(500, self.root.deiconify)  # Restore app window
            self.show_status("Text sent successfully")
        except Exception as e:
            self.root.deiconify()  # Restore app window
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.show_status("Error while sending keys")
    
    def add_to_history(self, string):
        """Add a string to history with obfuscation based on current setting"""
        self.history.append(string)
        
        # Determine if this entry should be obfuscated
        # Don't obfuscate hotkey entries
        is_hotkey = string.startswith("[HOTKEY] ")
        is_obfuscated = False if is_hotkey else self.obfuscate_by_default
        self.history_display_state.append(is_obfuscated)
        
        # Display the actual or obfuscated string
        display_string = string if (is_hotkey or not is_obfuscated) else '*' * len(string)
        self.history_listbox.insert(tk.END, display_string)
        
        status_prefix = "Added to history: "
        self.show_status(f"{status_prefix}'{string[:30]}{'...' if len(string) > 30 else ''}'")
    
    def resend_string(self):
        """Resend a string from history"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
            
            if string.startswith("[HOTKEY] "):
                hotkey_str = string.replace("[HOTKEY] ", "")
                keys = self.parse_hotkey(hotkey_str)
                
                # Set up a delay to send
                delay_time = self.get_delay_time()
                if delay_time is None:
                    messagebox.showerror("Error", "Invalid delay time. Please enter a valid number.")
                    return
                    
                self.show_status(f"Resending hotkey {hotkey_str} after delay: {delay_time} seconds...")
                self.root.after(int(delay_time * 1000), lambda: self.execute_hotkey(keys, hotkey_str))
                return
                
            # For regular text
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, string)
            self.send_text()
        else:
            self.show_status("No history item selected")
    
    def copy_string(self):
        """Copy selected string to clipboard"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]  # Always copy the actual string
            
            # Remove hotkey prefix if present
            if string.startswith("[HOTKEY] "):
                string = string.replace("[HOTKEY] ", "")
                
            self.root.clipboard_clear()
            self.root.clipboard_append(string)
            self.show_status("Copied to clipboard")
        else:
            self.show_status("No history item selected")
    
    def delete_string(self):
        """Delete a string from history"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            del self.history[index]
            del self.history_display_state[index]
            self.history_listbox.delete(index)
            self.show_status("Deleted from history")
        else:
            self.show_status("No history item selected")
    
    def obfuscate_string(self):
        """Mask the selected string in the list view"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
            
            # Don't obfuscate hotkeys
            if string.startswith("[HOTKEY] "):
                self.show_status("Hotkeys cannot be obfuscated")
                return
                
            if not self.history_display_state[index]:  # Only obfuscate if not already obfuscated
                self.history_listbox.delete(index)
                self.history_listbox.insert(index, '*' * len(string))
                self.history_display_state[index] = True
                self.show_status("String hidden")
            else:
                self.show_status("String is already hidden")
        else:
            self.show_status("No history item selected")
    
    def deobfuscate_string(self):
        """Reveal the actual string in the list view"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
            
            # No need to deobfuscate hotkeys
            if string.startswith("[HOTKEY] "):
                self.show_status("Hotkeys are always visible")
                return
                
            if self.history_display_state[index]:  # Only reveal if currently obfuscated
                self.history_listbox.delete(index)
                self.history_listbox.insert(index, string)
                self.history_display_state[index] = False
                self.show_status("String revealed")
            else:
                self.show_status("String is already visible")
        else:
            self.show_status("No history item selected")
    
    def toggle_all_entries(self):
        """Toggle visibility of all entries"""
        if not self.history:
            self.show_status("History is empty")
            return
        
        # Determine the action based on majority state (ignoring hotkeys)
        text_entries = [i for i, s in enumerate(self.history) if not s.startswith("[HOTKEY] ")]
        if not text_entries:
            self.show_status("No text entries to toggle")
            return
            
        text_states = [self.history_display_state[i] for i in text_entries]
        obfuscated_count = sum(text_states)
        # If more than half are obfuscated, reveal all; otherwise, hide all
        reveal_all = obfuscated_count > len(text_entries) / 2
        
        for i in range(len(self.history)):
            # Skip hotkey entries
            if self.history[i].startswith("[HOTKEY] "):
                continue
                
            self.history_listbox.delete(i)  # Delete at current position
            display_string = self.history[i] if reveal_all else '*' * len(self.history[i])
            self.history_listbox.insert(i, display_string)
            self.history_display_state[i] = not reveal_all
        
        status = "revealed" if reveal_all else "hidden"
        self.show_status(f"All text strings {status}")
    
    def show_status(self, message):
        """Update the status bar with a message"""
        self.status_var.set(message)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = StringSenderApp(root)
    # Set window size and position
    window_width = 550
    window_height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.mainloop()

if __name__ == "__main__":
    main()