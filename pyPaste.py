#!.venv/bin/python3

import tkinter as tk
from tkinter import messagebox, simpledialog
import pyautogui
import time

class StringSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pyPaste")
        
        self.history = []  # List to store history of strings
        
        # Main Frame for input and sending
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)
        
        self.setup_input_ui()
        self.setup_history_ui()
    
    def setup_input_ui(self):
        # Text Entry
        self.text_entry = tk.Entry(self.input_frame, width=50)
        self.text_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delay Entry
        self.delay_var = tk.StringVar(value='2')  # Default delay of 2 seconds
        self.delay_entry = tk.Entry(self.input_frame, textvariable=self.delay_var, width=5)
        self.delay_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Send Button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_keys)
        self.send_button.pack(side=tk.LEFT)

    def setup_history_ui(self):
        # History Frame
        self.history_frame = tk.LabelFrame(self.root, text="History")
        self.history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # History Listbox
        self.history_listbox = tk.Listbox(self.history_frame, width=50, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        # History Buttons Frame
        self.history_buttons_frame = tk.Frame(self.history_frame)
        self.history_buttons_frame.pack(side=tk.RIGHT, fill="y")
        
        # History Action Buttons
        self.resend_button = tk.Button(self.history_buttons_frame, text="Resend", command=self.resend_string)
        self.resend_button.pack(fill="x")
        
        self.delete_button = tk.Button(self.history_buttons_frame, text="Delete", command=self.delete_string)
        self.delete_button.pack(fill="x")
        
        self.obfuscate_button = tk.Button(self.history_buttons_frame, text="Obfuscate", command=self.obfuscate_string)
        self.obfuscate_button.pack(fill="x")
        
        self.deobfuscate_button = tk.Button(self.history_buttons_frame, text="Deobfuscate", command=self.deobfuscate_string)
        self.deobfuscate_button.pack(fill="x")

    def send_keys(self):
        input_string = self.text_entry.get()
        delay_time = self.get_delay_time()
        if delay_time is None:
            messagebox.showerror("Error", "Invalid delay time. Please enter a valid number.")
            return
        self.add_to_history(input_string)
        print("Sending keys after delay:", delay_time, "seconds")
        self.root.after(int(delay_time * 1000), lambda: self.type_string(input_string))
    
    def get_delay_time(self):
        try:
            return float(self.delay_var.get())
        except ValueError:
            return None
    
    def type_string(self, string):
        try:
            pyautogui.typewrite(string)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def add_to_history(self, string):
        self.history.append(string)
        self.history_listbox.insert(tk.END, string)
    
    def resend_string(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            string = self.history[index]
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, string)
            self.send_keys()
    
    def delete_string(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            del self.history[index]
            self.history_listbox.delete(index)
    
    def obfuscate_string(self):
        selection = self.history_listbox.curselection()
        if selection:
            self.history_listbox.delete(selection[0])
            self.history_listbox.insert(selection[0], '*' * len(self.history[selection[0]]))
    
    def deobfuscate_string(self):
        selection = self.history_listbox.curselection()
        if selection:
            actual_string = self.history[selection[0]]
            self.history_listbox.delete(selection[0])
            self.history_listbox.insert(selection[0], actual_string)

if __name__ == "__main__":
    root = tk.Tk()
    app = StringSenderApp(root)
    root.mainloop()
