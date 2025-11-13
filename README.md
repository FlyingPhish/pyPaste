# pyPaste

### Overview

**pyPaste** is a Python GUI application designed to automate text and hotkey input for systems where clipboard functionality is limited or disabled, such as VMs, remote sessions (RDP, Citrix), and secure environments. The application features a horizontal layout optimized for wide screens and provides comprehensive text input automation and hotkey management.

### Key Features

#### Text Input
- **Multi-line Text Entry**: Large text area supporting paragraphs, code blocks, and formatted content
- **Configurable Delays**: Customizable delay (0-60 seconds) before text transmission
- **Quick Actions**: Instant access to common keys (Enter, Tab, Esc)

#### Hotkey Management
- **Common Shortcuts**: Pre-configured buttons for frequently used combinations (Ctrl+C, Ctrl+V, Ctrl+Z, Alt+F4, Win+R, Ctrl+Alt+Delete)
- **Custom Hotkeys**: Build custom key combinations using modifiers (Ctrl, Alt, Shift, Win) with any key
- **Live Preview**: Real-time preview of custom hotkey combinations
- **Cross-Platform**: Automatic platform detection for proper modifier key mapping (Win/Cmd)

#### History Management
- **Comprehensive History**: Tracks both text inputs and hotkey combinations
- **Privacy Controls**: Toggle visibility for sensitive text (obfuscation with asterisks)
- **Quick Actions**: Resend, copy to clipboard, delete, or clear all history
- **Persistent Session**: History maintained throughout application session

#### User Interface
- **Horizontal Layout**: Three-column design optimized for wide screens
- **Responsive Design**: Proper scaling and space utilization
- **Status Feedback**: Real-time status updates and error handling
- **Intuitive Controls**: Clean, organized interface with logical grouping

### Architecture

The application follows a modular architecture with clean separation of concerns:

- **Core Components**:
  - `HotkeyManager`: Cross-platform hotkey parsing and key mapping
  - `HistoryManager`: Session history with privacy controls
  
- **UI Framework**:
  - `HorizontalInputFrame`: Text input with delay controls
  - `HorizontalHotkeyFrame`: Common and custom hotkey management
  - `HorizontalHistoryFrame`: History display and management
  - `UIComponentFactory`: Reusable UI components

- **Main Application**: `PyPasteHorizontalApp` orchestrates all components

### Installation and Usage

#### Requirements
- Python 3.7+
- Required packages: `tkinter`, `pyautogui`

#### Setup
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