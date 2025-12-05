"""
BunkMeter
Main application entry point

Author: Siddhesh Bisen
GitHub: https://github.com/siddhesh17b
"""

import tkinter as tk
from tkinter import ttk

from data_manager import load_data, save_data, get_app_data, parse_timetable_csv
from modern_dialogs import messagebox
from setup_tab import SetupTab
from timetable_tab import TimetableTab
from attendance_calendar import AttendanceCalendar
from summary_tab import SummaryTab

# Color scheme
COLOR_INFO = "#007bff"
COLOR_BG_LIGHT = "#ffffff"  # Pure white for modern look


class BunkBuddyApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BunkMeter")
        
        # Center the main window
        width = 1400
        height = 1000
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(1200, 800)  # Minimum window size to prevent squishing
        self.root.configure(bg=COLOR_BG_LIGHT)
        
        # Optimize rendering
        self.root.update_idletasks()
        
        # Load data first, then check if setup is needed
        # Note: load_data() updates app_data in-place, so we must call it BEFORE get_app_data()
        data_loaded = load_data()
        app_data = get_app_data()  # Now get reference to the loaded data
        
        if not data_loaded or not app_data.get("batch"):
            self.show_first_time_setup()
        
        # Create main UI
        self.create_ui()
        # Initial tab will refresh on its own during creation
    
    def show_first_time_setup(self):
        """
        First-time setup wizard shown when app launches for the first time
        Allows users to:
        1. Import custom timetable CSV (optional)
        2. Select their batch/group
        
        Note: Batch names are auto-detected from timetable entries with format:
        "Subject (BatchA) / Subject (BatchB)"
        """
        # Create modal dialog window with modern styling
        setup_window = tk.Toplevel(self.root)
        setup_window.title("Welcome to BunkMeter!")
        setup_window.transient(self.root)  # Set as child of main window
        setup_window.grab_set()  # Make window modal (blocks interaction with parent)
        setup_window.configure(bg="#e3f2fd")  # Blue theme background
        setup_window.resizable(False, False)
        
        # Center the window on screen
        setup_window.update_idletasks()
        width = 550
        height = 420
        x = (setup_window.winfo_screenwidth() // 2) - (width // 2)
        y = (setup_window.winfo_screenheight() // 2) - (height // 2)
        setup_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container with border
        main_frame = tk.Frame(
            setup_window, 
            bg="#e3f2fd",
            highlightthickness=2,
            highlightbackground="#1976d2"
        )
        main_frame.pack(fill="both", expand=True)
        
        # Styled header bar (blue theme)
        header = tk.Frame(main_frame, bg="#1976d2", height=65)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎓 Welcome to BunkMeter!",
            font=("Segoe UI", 18, "bold"),
            bg="#1976d2",
            fg="white",
            padx=20
        ).pack(side=tk.LEFT, pady=15)
        
        # Content area
        content = tk.Frame(main_frame, bg="#e3f2fd", padx=25, pady=20)
        content.pack(fill="both", expand=True)
        
        # Import timetable section with styled box
        import_box = tk.Frame(content, bg="#bbdefb", padx=15, pady=12)
        import_box.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(import_box, text="Step 1: Import Your Timetable (Optional)", 
                 font=("Segoe UI", 12, "bold"), bg="#bbdefb", fg="#1565c0").pack(anchor="w")
        tk.Label(import_box, text="Upload your CSV timetable to auto-detect batches", 
                 font=("Segoe UI", 11), bg="#bbdefb", fg="#1976d2").pack(anchor="w", pady=(5, 8))
        
        def import_timetable_firsttime():
            from data_manager import import_timetable_from_csv
            from tkinter import filedialog
            filepath = filedialog.askopenfilename(
                title="Import Custom Timetable",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filepath:
                if import_timetable_from_csv(filepath):
                    # Refresh batch detection
                    update_batch_options()
        
        import_btn = tk.Button(
            import_box, text="📥 Import Timetable CSV", font=("Segoe UI", 11, "bold"),
            bg="#1976d2", fg="white", relief=tk.FLAT, bd=0, highlightthickness=0,
            padx=15, pady=6, cursor="hand2", command=import_timetable_firsttime
        )
        import_btn.pack(anchor="w")
        
        # Batch selection section with styled box
        batch_box = tk.Frame(content, bg="#bbdefb", padx=15, pady=12)
        batch_box.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(batch_box, text="Step 2: Select Your Batch/Group", 
                 font=("Segoe UI", 12, "bold"), bg="#bbdefb", fg="#1565c0").pack(anchor="w")
        tk.Label(batch_box, text="Choose the batch that matches your schedule", 
                 font=("Segoe UI", 11), bg="#bbdefb", fg="#1976d2").pack(anchor="w", pady=(5, 8))
        
        batch_container = tk.Frame(batch_box, bg="#bbdefb")
        batch_container.pack(fill=tk.BOTH, expand=True)
        
        batch_var = tk.StringVar()
        
        def update_batch_options():
            """
            Dynamically detect and display batch options from timetable
            
            How it works:
            1. Scans all timetable entries for format: "Subject (BatchName) / Subject (BatchName2)"
            2. Extracts batch names from parentheses using regex
            3. Creates radio buttons for each unique batch found
            4. Falls back to default B1/B3, B2/B4 if no batches detected
            
            To modify batch detection:
            - Change regex pattern in re.findall() to match your format
            - Update fallback batch names in the 'if not batch_names' block
            """
            # Clear existing radio buttons before recreating them
            for widget in batch_container.winfo_children():
                widget.destroy()
            
            # Get active timetable (custom if imported, otherwise default)
            from data_manager import get_active_timetable
            import re
            active_timetable = get_active_timetable()
            batch_names = set()
            
            # Scan timetable for batch names in parentheses
            for day_data in active_timetable.values():
                for cell_value in day_data.values():
                    if "/" in cell_value and "(" in cell_value:
                        # Extract batch names from format: "Subject (GroupA) / Subject (GroupB)"
                        # Regex \(([^)]+)\) matches text inside parentheses
                        matches = re.findall(r'\(([^)]+)\)', cell_value)
                        batch_names.update(matches)
            
            # Fallback: If no batches found, use default batches
            if not batch_names:
                batch_names = ["B1/B3", "B2/B4"]
            else:
                batch_names = sorted(list(batch_names))
            
            # Safe access - ensure batch_names is not empty before accessing
            if batch_names:
                batch_var.set(batch_names[0])
            else:
                batch_var.set("B1/B3")
                batch_names = ["B1/B3", "B2/B4"]  # Fallback to defaults
            
            for batch_name in batch_names:
                rb = tk.Radiobutton(
                    batch_container, text=batch_name, variable=batch_var, value=batch_name,
                    font=("Segoe UI", 11), bg="#bbdefb", fg="#1565c0",
                    activebackground="#90caf9", selectcolor="#e3f2fd", cursor="hand2"
                )
                rb.pack(anchor=tk.W, pady=3)
        
        # Initial batch detection
        update_batch_options()
        
        def save_and_close():
            """
            Validate selection and initialize app data
            
            Validation steps:
            1. Check if batch is selected
            2. Parse timetable to get subjects for selected batch
            3. Ensure subjects exist (prevents empty subject list)
            4. Initialize all subjects with empty absent_dates (present by default)
            
            To add custom validation:
            - Add checks before the app_data initialization
            - Show error messages using messagebox.showerror()
            """
            # Use modern_dialogs messagebox (already imported at top of file)
            
            selected_batch = batch_var.get()
            
            # Validation 1: Ensure batch is selected
            if not selected_batch:
                messagebox.showerror("Error", "Please select a batch/group before continuing!")
                return
            
            # Parse timetable to extract subjects for this batch
            # Returns dict: {subject_name: weekly_class_count}
            weekly_counts = parse_timetable_csv(selected_batch)
            
            # Validation 2: Ensure subjects exist for selected batch
            if not weekly_counts:
                messagebox.showerror(
                    "Error", 
                    f"No subjects found for batch '{selected_batch}'!\n\n"
                    f"Please import a valid timetable or check your batch selection."
                )
                return
            
            app_data = get_app_data()
            app_data["batch"] = selected_batch
            app_data["subjects"] = [
                {
                    "name": subject,
                    "weekly_count": count,
                    "total_override": None,
                    "attendance_override": None,
                    "absent_dates": []  # All classes present by default
                }
                for subject, count in weekly_counts.items()
            ]
            save_data()
            setup_window.destroy()
        
        # Styled Continue button (blue theme)
        continue_btn = tk.Button(
            content, text="Continue →", font=("Segoe UI", 12, "bold"),
            bg="#1976d2", fg="white", relief=tk.FLAT, bd=0, highlightthickness=0,
            padx=30, pady=10, cursor="hand2", command=save_and_close
        )
        continue_btn.pack(pady=(10, 0))
        
        self.root.wait_window(setup_window)
    
    def create_ui(self):
        """Create main tabbed interface"""
        # Modern header with left-aligned content
        title_frame = tk.Frame(self.root, bg="#000000", height=55)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # Left-aligned content
        tk.Label(
            title_frame,
            text="BunkMeter  —  Be Academically adventurous",
            font=("Segoe UI", 18, "bold"),
            bg="#000000",
            fg="white"
        ).pack(side=tk.LEFT, padx=25, pady=12)
        
        # Configure ttk style for modern ribbon-style tabs
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better customization
        
        # Configure white backgrounds for frames
        style.configure('TFrame', background='#ffffff')
        style.configure('TLabelframe', background='#ffffff')
        style.configure('TLabelframe.Label', background='#ffffff')
        style.configure('TLabel', background='#ffffff')
        
        # Modern notebook styling - clean border
        style.configure('TNotebook', 
                       background='#f5f5f5',
                       borderwidth=0,
                       tabmargins=[10, 5, 10, 0])
        
        # Remove default focus dotted line and center text
        style.layout('TNotebook.Tab', [
            ('Notebook.tab', {'sticky': 'nswe', 'children': [
                ('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [
                    ('Notebook.label', {'side': 'top', 'sticky': 'nswe'})
                ]})
            ]})
        ])
        
        # Modern pill-shaped tabs with centered text
        style.configure('TNotebook.Tab', 
                       font=('Segoe UI', 12, 'bold'),
                       padding=[30, 12],
                       background='#e8eef4',
                       foreground='#5f6368',
                       borderwidth=0,
                       focuscolor='',
                       relief='flat',
                       anchor='center')
        
        # Tab state styling with modern colors
        style.map('TNotebook.Tab',
                 background=[
                     ('selected', '#1a73e8'),  # Google Blue for selected
                     ('active', '#d2e3fc'),    # Light blue on hover
                     ('!selected', '#e8eef4')  # Light gray for unselected
                 ],
                 foreground=[
                     ('selected', '#ffffff'),   # White text when selected
                     ('active', '#1a73e8'),     # Blue text on hover
                     ('!selected', '#5f6368')   # Gray text when not selected
                 ],
                 padding=[
                     ('selected', [30, 14]),    # Slightly larger when selected
                     ('!selected', [30, 12])
                 ])
        
        # Tab control
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Animate tab switch with fade effect
        self.current_tab_index = 0
        
        def on_tab_changed(event):
            new_index = self.notebook.index(self.notebook.select())
            if new_index != self.current_tab_index:
                self.current_tab_index = new_index
                # Quick flash effect
                self.notebook.configure(style='TNotebook')
        
        self.notebook.bind('<<NotebookTabChanged>>', on_tab_changed)
        
        # Block tab switching when in setup mode
        def on_tab_click(event):
            # Check if setup_tab exists and is in setup mode
            if hasattr(self, 'setup_tab') and self.setup_tab.setup_mode:
                # Get the clicked tab (use str() to get widget path - avoids Pylance warning about _w)
                clicked_tab = self.notebook.tk.call(str(self.notebook), "identify", "tab", event.x, event.y)
                if clicked_tab != "" and int(clicked_tab) != 0:  # Not the Setup tab
                    messagebox.showwarning(
                        "Setup Required",
                        "Please complete the setup first:\n\n"
                        "1. Select your batch\n"
                        "2. Set semester start and end dates\n\n"
                        "Then you can access other tabs."
                    )
                    return "break"  # Prevent tab switch
        
        self.notebook.bind('<Button-1>', on_tab_click, add='+')
        
        # Dynamic tab width adjustment for full-width tabs
        def on_notebook_configure(event):
            num_tabs = 4
            tab_width = (event.width - 60) // num_tabs
            style.configure('TNotebook.Tab', width=tab_width)
        self.notebook.bind('<Configure>', on_notebook_configure)
        
        # Create tabs
        self.setup_tab = SetupTab(self.notebook, self.refresh_all_tabs)
        self.notebook.add(self.setup_tab.create(), text="⚙️ Setup")
        
        self.timetable_tab = TimetableTab(self.notebook, self.refresh_all_tabs)
        self.notebook.add(self.timetable_tab.create(), text="📋 Timetable")
        
        self.attendance_calendar = AttendanceCalendar(self.notebook, self.refresh_all_tabs)
        self.notebook.add(self.attendance_calendar.create(), text="📅 Mark Attendance")
        
        self.summary_tab = SummaryTab(self.notebook, self.refresh_all_tabs)
        self.notebook.add(self.summary_tab.create(), text="📊 Summary")
    
    def refresh_all_tabs(self):
        """Refresh all tab displays"""
        # Defer refresh to avoid blocking UI
        self.root.after(10, self._do_refresh)
    
    def _do_refresh(self):
        """Actual refresh logic with optimized order"""
        if hasattr(self, 'setup_tab'):
            self.setup_tab.refresh()
        if hasattr(self, 'timetable_tab'):
            self.timetable_tab.refresh()
        if hasattr(self, 'attendance_calendar'):
            self.attendance_calendar.refresh()
        if hasattr(self, 'summary_tab'):
            self.summary_tab.refresh()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = BunkBuddyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
