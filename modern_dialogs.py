"""
Modern Dialog System for BunkMeter
Custom styled dialogs to replace plain tkinter messageboxes

Author: Siddhesh Bisen, GitHub: https://github.com/siddhesh17b
"""

import tkinter as tk
from tkinter import ttk

class ModernDialog:
    """
    Custom modern dialog class with sleek, professional styling
    
    Dialog types:
    - info: Blue theme with ℹ️ icon
    - success: Green theme with ✅ icon
    - warning: Orange/Yellow theme with ⚠️ icon
    - error: Red theme with ❌ icon
    - confirm: Blue theme with ❓ icon, Yes/No buttons
    """
    
    # Theme colors for different dialog types - modern Material Design inspired
    THEMES = {
        "info": {
            "bg": "#ffffff",
            "header_bg": "#2196F3",
            "header_fg": "white",
            "text_fg": "#333333",
            "icon": "ℹ️",
            "icon_bg": "#E3F2FD",
            "btn_bg": "#2196F3",
            "btn_fg": "white",
            "btn_hover": "#1976D2"
        },
        "success": {
            "bg": "#ffffff",
            "header_bg": "#4CAF50",
            "header_fg": "white",
            "text_fg": "#333333",
            "icon": "✓",
            "icon_bg": "#E8F5E9",
            "btn_bg": "#4CAF50",
            "btn_fg": "white",
            "btn_hover": "#388E3C"
        },
        "warning": {
            "bg": "#ffffff",
            "header_bg": "#FF9800",
            "header_fg": "white",
            "text_fg": "#333333",
            "icon": "⚠",
            "icon_bg": "#FFF3E0",
            "btn_bg": "#FF9800",
            "btn_fg": "white",
            "btn_hover": "#F57C00"
        },
        "error": {
            "bg": "#ffffff",
            "header_bg": "#F44336",
            "header_fg": "white",
            "text_fg": "#333333",
            "icon": "✕",
            "icon_bg": "#FFEBEE",
            "btn_bg": "#F44336",
            "btn_fg": "white",
            "btn_hover": "#D32F2F"
        },
        "confirm": {
            "bg": "#ffffff",
            "header_bg": "#2196F3",
            "header_fg": "white",
            "text_fg": "#333333",
            "icon": "?",
            "icon_bg": "#E3F2FD",
            "btn_bg": "#2196F3",
            "btn_fg": "white",
            "btn_hover": "#1976D2"
        }
    }
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None):
        """
        Create a modern styled dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
            dialog_type: One of 'info', 'success', 'warning', 'error', 'confirm'
            buttons: List of button configs [{"text": "OK", "command": func, "primary": True}]
        """
        self.result = None
        
        # Handle None parent - get default root or create one
        if parent is None:
            parent = tk._default_root
        if parent is None:
            # Create a hidden root window if none exists
            parent = tk.Tk()
            parent.withdraw()
            self._created_root = True
        else:
            self._created_root = False
        
        self.parent = parent
        
        # Get theme
        theme = self.THEMES.get(dialog_type, self.THEMES["info"])
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.configure(bg=theme["bg"])
        self.dialog.resizable(False, False)
        if parent is not None:
            self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Add shadow effect via border
        self.dialog.configure(highlightthickness=1, highlightbackground="#e0e0e0")
        
        # Main container
        main_frame = tk.Frame(self.dialog, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Content area with icon and message
        content = tk.Frame(main_frame, bg=theme["bg"], padx=30, pady=30)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Icon circle - large circular background with icon
        icon_frame = tk.Frame(content, bg=theme["bg"])
        icon_frame.pack(pady=(0, 20))
        
        # Create circular icon background using a canvas
        icon_size = 70
        icon_canvas = tk.Canvas(
            icon_frame, 
            width=icon_size, 
            height=icon_size, 
            bg=theme["bg"], 
            highlightthickness=0
        )
        icon_canvas.pack()
        
        # Draw circle
        icon_canvas.create_oval(
            2, 2, icon_size-2, icon_size-2,
            fill=theme["icon_bg"],
            outline=theme["header_bg"],
            width=3
        )
        
        # Add icon text
        icon_canvas.create_text(
            icon_size//2, icon_size//2,
            text=theme["icon"],
            font=("Segoe UI", 28, "bold"),
            fill=theme["header_bg"]
        )
        
        # Title - large and bold
        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 18, "bold"),
            bg=theme["bg"],
            fg="#222222"
        ).pack(pady=(0, 10))
        
        # Message - centered, readable
        tk.Label(
            content,
            text=message,
            font=("Segoe UI", 12),
            bg=theme["bg"],
            fg=theme["text_fg"],
            justify=tk.CENTER,
            wraplength=350
        ).pack(pady=(0, 25))
        
        # Button area
        btn_frame = tk.Frame(content, bg=theme["bg"])
        btn_frame.pack(fill=tk.X)
        
        # Default buttons if none provided
        if buttons is None:
            buttons = [{"text": "OK", "command": self.close, "primary": True}]
        
        # Center buttons
        btn_container = tk.Frame(btn_frame, bg=theme["bg"])
        btn_container.pack()
        
        # Create buttons - modern rounded style
        for i, btn_config in enumerate(buttons):
            is_primary = btn_config.get("primary", False)
            
            btn = tk.Button(
                btn_container,
                text=btn_config["text"],
                font=("Segoe UI", 11, "bold"),
                bg=theme["btn_bg"] if is_primary else "#f5f5f5",
                fg=theme["btn_fg"] if is_primary else "#666666",
                activebackground=theme["btn_hover"] if is_primary else "#e0e0e0",
                activeforeground="white" if is_primary else "#333333",
                relief=tk.FLAT,
                bd=0,
                highlightthickness=0,
                padx=30,
                pady=10,
                cursor="hand2",
                command=btn_config.get("command", self.close)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Add hover effect
            if is_primary:
                btn.bind("<Enter>", lambda e, b=btn, c=theme["btn_hover"]: b.configure(bg=c))
                btn.bind("<Leave>", lambda e, b=btn, c=theme["btn_bg"]: b.configure(bg=c))
            else:
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#e8e8e8"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#f5f5f5"))
        
        # Center dialog on parent
        self.center_on_parent()
        
        # Handle close button
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        
        # Bind escape key
        self.dialog.bind("<Escape>", lambda e: self.close())
        
        # Focus dialog
        self.dialog.focus_set()
    
    def center_on_parent(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get sizes
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Ensure minimum size
        min_width = 400
        if dialog_width < min_width:
            dialog_width = min_width
            self.dialog.geometry(f"{dialog_width}x{dialog_height}")
        
        # Get parent position
        if self.parent:
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
        else:
            # Center on screen
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width - dialog_width) // 2
            y = (screen_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def close(self):
        """Close the dialog"""
        self.dialog.destroy()
    
    def wait(self):
        """Wait for dialog to close and return result"""
        self.dialog.wait_window()
        return self.result


# Convenience functions to replace messagebox calls

def show_info(parent, title, message):
    """Show an info dialog (replaces messagebox.showinfo)"""
    dialog = ModernDialog(parent, title, message, "info")
    dialog.wait()

def show_success(parent, title, message):
    """Show a success dialog"""
    dialog = ModernDialog(parent, title, message, "success")
    dialog.wait()

def show_warning(parent, title, message):
    """Show a warning dialog (replaces messagebox.showwarning)"""
    dialog = ModernDialog(parent, title, message, "warning")
    dialog.wait()

def show_error(parent, title, message):
    """Show an error dialog (replaces messagebox.showerror)"""
    dialog = ModernDialog(parent, title, message, "error")
    dialog.wait()

def ask_yes_no(parent, title, message):
    """Show a confirmation dialog (replaces messagebox.askyesno)"""
    result = [False]  # Use list to allow modification in nested function
    
    def on_yes():
        result[0] = True
        dialog.close()
    
    def on_no():
        result[0] = False
        dialog.close()
    
    buttons = [
        {"text": "Yes", "command": on_yes, "primary": True},
        {"text": "No", "command": on_no, "primary": False}
    ]
    
    dialog = ModernDialog(parent, title, message, "confirm", buttons)
    dialog.wait()
    return result[0]


# Drop-in replacement class that mimics tkinter.messagebox API exactly
class messagebox:
    """
    Drop-in replacement for tkinter.messagebox with modern styling.
    
    Usage - just replace the import:
        # OLD: from tkinter import messagebox
        # NEW: from modern_dialogs import messagebox
        
        messagebox.showinfo("Title", "Message")  # Works exactly like before!
    """
    
    @staticmethod
    def showinfo(title, message, **kwargs):
        """Show info dialog - compatible with tkinter.messagebox.showinfo"""
        show_info(None, title, message)
    
    @staticmethod
    def showwarning(title, message, **kwargs):
        """Show warning dialog - compatible with tkinter.messagebox.showwarning"""
        show_warning(None, title, message)
    
    @staticmethod
    def showerror(title, message, **kwargs):
        """Show error dialog - compatible with tkinter.messagebox.showerror"""
        show_error(None, title, message)
    
    @staticmethod
    def askyesno(title, message, **kwargs):
        """Show yes/no dialog - compatible with tkinter.messagebox.askyesno"""
        return ask_yes_no(None, title, message)
    
    @staticmethod
    def showsuccess(title, message, **kwargs):
        """Show success dialog (BunkMeter extension)"""
        show_success(None, title, message)
