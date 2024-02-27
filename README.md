### Overview

This Python script implements a GUI-based application, named **pyPaste**, designed to automate the process of sending strings (text inputs) to the system or an application interface, for example, VMs and remote sessions (RDP, Citrix, etc) where shared clipboards are disabled. The application allows users to input text, specify a delay before sending the text, and manage a history of sent strings, including features to resend, delete, obfuscate, and deobfuscate strings. You can use this to paste code or paragraphs.

### Key Features

- **Text and Delay Input**: Users can input the text they wish to send and specify a delay (in seconds) before the text is sent.
- **Send Functionality**: After the specified delay, the application uses `pyautogui.typewrite` to simulate typing the input text.
- **History Management**: The application maintains a history of sent texts. Users can resend, delete, or obfuscate/deobfuscate these entries.
- **Error Handling**: The application provides error messages for invalid delay times or other issues during text sending.

### Implementation Details

- **Tkinter GUI**: The interface is built using Tkinter, with a simple layout consisting of input fields for text and delay, a send button, and a history section with management options.
- **Delayed Sending**: The delay functionality is implemented using the `after` method from Tkinter, which waits for the specified time (in milliseconds) before executing the typing simulation.
- **History Features**: Users can interact with the history of sent strings through buttons that allow resending, deleting, and obfuscating (replacing the string with asterisks) or deobfuscating (restoring the original string) entries.

### Installation and Usage

1. Ensure Python 3.x is installed on your system.
2. Install the required packages using pip. I recommend using venv wherever possible:
   ```
   pip install -r requirements.txt
   ```
3. Run the script:
   ```
   ./pyPaste.py
   python3 ./pyPaste.py
   ```

### Note on Security and Memory Management

As a Python script, this application does not utilize automatic garbage collection for cleartext strings. Therefore, cleartext strings will remain stored in memory until the script is terminated. Users should be aware of this behavior, especially when sending sensitive information, as it may pose a security risk. I think you may have greater problems if someone/thing is dumping your memory...