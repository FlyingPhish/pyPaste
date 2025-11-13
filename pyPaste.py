#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, simpledialog
import pyautogui
import platform
import sys

class StringSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pyPaste")
        
        # Set up platform-specific configurations
        self.configure_for_platform()
        
        self.history = []  # List to store history of strings
        
        # Main Frame for input and sending
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)
        
        self.setup_input_ui()
        self.setup_history_ui()
    
    def configure_for_platform(self):
        """Apply platform-specific configurations"""
        self.platform = platform.system()
        # Add platform-specific configurations if needed in the future
        print(f"Running on {self.platform}")
    
    def setup_input_ui(self):
        # Input frame title
        input_label = tk.Label(self.input_frame, text="Enter text to send:")
        input_label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=(0, 5))
        
        # Text entry frame
        entry_frame = tk.Frame(self.input_frame)
        entry_frame.pack(fill=tk.X)
        
        # Text Entry
        self.text_entry = tk.Entry(entry_frame, width=50)
        self.text_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Delay label
        delay_label = tk.Label(entry_frame, text="Delay (s):")
        delay_label.pack(side=tk.LEFT)
        
        # Delay Entry
        self.delay_var = tk.StringVar(value='2')  # Default delay of 2 seconds
        self.delay_entry = tk.Entry(entry_frame, textvariable=self.delay_var, width=5)
        self.delay_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # Send Button
        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_keys)
        self.send_button.pack(side=tk.LEFT)

    def setup_history_ui(self):
        # History Frame
        self.history_frame = tk.LabelFrame(self.root, text="History")
        self.history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # History Listbox with scrollbar
        listbox_frame = tk.Frame(self.history_frame)
        listbox_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(listbox_frame, width=50, height=10, yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # History Buttons Frame
        self.history_buttons_frame = tk.Frame(self.history_frame)
        self.history_buttons_frame.pack(side=tk.RIGHT, fill="y", padx=5, pady=5)
        
        # History Action Buttons
        self.resend_button = tk.Button(self.history_buttons_frame, text="Resend", command=self.resend_string)
        self.resend_button.pack(fill="x", pady=2)
        
        self.copy_button = tk.Button(self.history_buttons_frame, text="Copy", command=self.copy_string)
        self.copy_button.pack(fill="x", pady=2)
        
        self.delete_button = tk.Button(self.history_buttons_frame, text="Delete", command=self.delete_string)
        self.delete_button.pack(fill="x", pady=2)
        
        self.obfuscate_button = tk.Button(self.history_buttons_frame, text="Obfuscate", command=self.obfuscate_string)
        self.obfuscate_button.pack(fill="x", pady=2)
        
        self.deobfuscate_button = tk.Button(self.history_buttons_frame, text="Deobfuscate", command=self.deobfuscate_string)
        self.deobfuscate_button.pack(fill="x", pady=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def send_keys(self):
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
        self.show_status(f"Sending keys after delay: {delay_time} seconds...")
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
            self.show_status("Keys sent successfully")
        except Exception as e:
            self.root.deiconify()  # Restore app window
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.show_status("Error while sending keys")
    
    def add_to_history(self, string):
        """Add a string to history"""
        self.history.append(string)
        self.history_listbox.insert(tk.END, string)
        self.show_status(f"Added to history: '{string[:20]}{'...' if len(string) > 20 else ''}'")
    
    def resend_string(self):
        """Resend a string from history"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, string)
            self.send_keys()
        else:
            self.show_status("No history item selected")
    
    def copy_string(self):
        """Copy selected string to clipboard"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
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
            self.history_listbox.delete(index)
            self.show_status("Deleted from history")
        else:
            self.show_status("No history item selected")
    
    def obfuscate_string(self):
        """Mask the selected string in the list view"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            self.history_listbox.delete(index)
            self.history_listbox.insert(index, '*' * len(self.history[index]))
            self.show_status("String obfuscated")
        else:
            self.show_status("No history item selected")
    
    def deobfuscate_string(self):
        """Reveal the actual string in the list view"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            actual_string = self.history[index]
            self.history_listbox.delete(index)
            self.history_listbox.insert(index, actual_string)
            self.show_status("String revealed")
        else:
            self.show_status("No history item selected")
    
    def show_status(self, message):
        """Update the status bar with a message"""
        self.status_var.set(message)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = StringSenderApp(root)
    # Set window size and position
    window_width = 500
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.mainloop()

if __name__ == "__main__":
    main()