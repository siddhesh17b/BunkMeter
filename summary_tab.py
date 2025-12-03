"""
Summary Dashboard - Overall attendance statistics and reporting

Features:
- Quick stats cards showing key metrics
- Sortable table with all subjects
- Color-coded status indicators  
- Export report functionality

Author: Siddhesh Bisen
GitHub: https://github.com/siddhesh17b
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from data_manager import get_app_data
from calculations import (
    calculate_weeks_elapsed, 
    calculate_total_classes, 
    calculate_attendance, 
    calculate_safe_skip, 
    get_attendance_status
)

# Color scheme
COLOR_SAFE = "#28a745"    # Green - safe attendance (≥75%)
COLOR_RISK = "#dc3545"    # Red - at risk (<75%)
COLOR_INFO = "#007bff"    # Blue - informational
COLOR_BG_DARK = "#e9ecef" # Light gray background


class SummaryTab:
    """Dashboard showing overall attendance statistics"""
    def __init__(self, notebook, refresh_callback):
        self.notebook = notebook
        self.refresh_all_tabs = refresh_callback
        self.stats_frame = None
        self.summary_tree = None
    
    def create(self):
        """Create the summary dashboard tab"""
        tab = ttk.Frame(self.notebook)
        
        # Header
        tk.Label(
            tab, 
            text="Overall Attendance Summary", 
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)
        
        # Stats cards frame
        self.stats_frame = tk.Frame(tab, bg=COLOR_BG_DARK)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Summary table
        columns = ("Subject", "Present", "Total", "Attendance %", "Status", "Safe to Skip", "Action")
        self.summary_tree = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        
        # Enable mouse wheel scrolling on treeview
        def _on_mousewheel(event):
            self.summary_tree.yview_scroll(int(-1*(event.delta/120)), "units")
        self.summary_tree.bind("<MouseWheel>", _on_mousewheel)
        
        for col in columns:
            self.summary_tree.heading(col, text=col)
            # Set column widths
            if col == "Subject":
                width = 150
            else:
                width = 100
            self.summary_tree.column(col, width=width)
        
        self.summary_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind double-click to open override dialog
        self.summary_tree.bind("<Double-Button-1>", self.on_row_double_click)
        
        # Info label
        tk.Label(
            tab,
            text="💡 Tip: Double-click any subject row to manually override attendance data",
            font=("Arial", 9),
            foreground="#6c757d"
        ).pack(pady=5)
        
        # Export button
        ttk.Button(
            tab, 
            text="📄 Export Report", 
            command=self.export_report
        ).pack(pady=10)
        
        # Initial data load
        self.refresh()
        
        return tab
    
    def refresh(self):
        """Refresh summary display"""
        app_data = get_app_data()
        
        # Optimize UI updates
        self.summary_tree.update_idletasks()
        
        # Clear existing items
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        # Clear stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not app_data.get("semester_start"):
            return
        
        # Calculate metrics
        total_attendance_pct = 0
        at_risk_count = 0
        safe_count = 0
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        if app_data.get("semester_end"):
            end_date = min(end_date, app_data["semester_end"])
        
        weeks = calculate_weeks_elapsed(
            app_data["semester_start"],
            end_date,
            app_data.get("holidays", [])
        )
        
        for subject_data in app_data.get("subjects", []):
            name = subject_data["name"]
            
            # Check if manual override exists
            if subject_data.get("attendance_override") is not None:
                override_data = subject_data["attendance_override"]
                present = override_data["attended"]
                total = override_data["total"]
                action_text = "📝 Edit (Manual)"
            else:
                # Calculate total classes
                if subject_data.get("total_override") is not None:
                    total = subject_data["total_override"]
                else:
                    total = calculate_total_classes(subject_data["weekly_count"], weeks)
                
                # Calculate present classes (total - absent)
                absent_count = len(subject_data.get("absent_dates", []))
                present = max(0, total - absent_count)
                action_text = "📝 Edit"
            
            attendance_pct = calculate_attendance(present, total)
            safe_skip = calculate_safe_skip(present, total)
            status, color = get_attendance_status(attendance_pct)
            
            total_attendance_pct += attendance_pct
            if attendance_pct < 75:
                at_risk_count += 1
            else:
                safe_count += 1
            
            item = self.summary_tree.insert(
                "", tk.END,
                values=(name, present, total, f"{attendance_pct:.1f}%", status, safe_skip, action_text)
            )
            
            if attendance_pct < 75:
                self.summary_tree.item(item, tags=("risk",))
            else:
                self.summary_tree.item(item, tags=("safe",))
        
        self.summary_tree.tag_configure("risk", foreground=COLOR_RISK)
        self.summary_tree.tag_configure("safe", foreground=COLOR_SAFE)
        
        # Display stats cards
        num_subjects = len(app_data.get("subjects", []))
        avg_attendance = total_attendance_pct / num_subjects if num_subjects > 0 else 0
        
        stats_info = [
            ("Total Subjects", num_subjects, COLOR_INFO),
            ("Average Attendance", f"{avg_attendance:.1f}%", COLOR_INFO),
            ("Safe Subjects", safe_count, COLOR_SAFE),
            ("At-Risk Subjects", at_risk_count, COLOR_RISK if at_risk_count > 0 else COLOR_INFO)
        ]
        
        for label, value, color in stats_info:
            # Create card frame
            frame = tk.Frame(self.stats_frame, bg=COLOR_BG_DARK)
            frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
            
            # Label
            tk.Label(
                frame, 
                text=label, 
                font=("Segoe UI", 10), 
                bg=COLOR_BG_DARK
            ).pack()
            
            # Value
            tk.Label(
                frame, 
                text=str(value), 
                font=("Segoe UI", 16, "bold"), 
                fg=color, 
                bg=COLOR_BG_DARK
            ).pack()
    
    def export_report(self):
        """Export attendance report to text file"""
        app_data = get_app_data()
        
        if not app_data.get("subjects"):
            messagebox.showwarning("Warning", "No data to export")
            return
        
        try:
            filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w') as f:
                # Header
                f.write("=" * 70 + "\n")
                f.write("MYATTENDANCE - ATTENDANCE REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Batch: {app_data.get('batch', 'N/A')}\n")
                f.write(f"Semester: {app_data.get('semester_start', 'N/A')} to {app_data.get('semester_end', 'N/A')}\n\n")
                
                f.write("-" * 70 + "\n")
                f.write(f"{'Subject':<20} {'Present':>10} {'Total':>10} {'%':>8} {'Status':>10}\n")
                f.write("-" * 70 + "\n")
                
                end_date = datetime.now().strftime("%Y-%m-%d")
                if app_data.get("semester_end"):
                    end_date = min(end_date, app_data["semester_end"])
                
                weeks = calculate_weeks_elapsed(
                    app_data["semester_start"],
                    end_date,
                    app_data.get("holidays", [])
                )
                
                for subject_data in app_data.get("subjects", []):
                    name = subject_data["name"]
                    
                    # Check if manual override exists
                    if subject_data.get("attendance_override") is not None:
                        override_data = subject_data["attendance_override"]
                        present = override_data["attended"]
                        total = override_data["total"]
                    else:
                        if subject_data.get("total_override") is not None:
                            total = subject_data["total_override"]
                        else:
                            total = calculate_total_classes(subject_data["weekly_count"], weeks)
                        
                        absent_count = len(subject_data.get("absent_dates", []))
                        present = max(0, total - absent_count)
                    
                    attendance_pct = calculate_attendance(present, total)
                    status, _ = get_attendance_status(attendance_pct)
                    
                    f.write(f"{name:<20} {present:>10} {total:>10} {attendance_pct:>7.1f}% {status:>10}\n")
                
                f.write("-" * 70 + "\n")
            
            messagebox.showinfo("Success", f"Report exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def on_row_double_click(self, event):
        """Handle double-click on tree row to open override dialog"""
        selection = self.summary_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.summary_tree.item(item, "values")
        if not values:
            return
        
        subject_name = values[0]
        self.open_override_dialog(subject_name)
    
    def open_override_dialog(self, subject_name):
        """Open dialog to manually override attendance data"""
        from data_manager import get_app_data, save_data
        
        app_data = get_app_data()
        subject_data = None
        
        # Find the subject
        for subj in app_data.get("subjects", []):
            if subj["name"] == subject_name:
                subject_data = subj
                break
        
        if not subject_data:
            return
        
        # Create dialog
        dialog = tk.Toplevel()
        dialog.title(f"Manual Override - {subject_name}")
        dialog.geometry("500x450")
        dialog.resizable(True, True)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        dialog.transient(self.notebook.master)
        dialog.grab_set()
        
        # Header
        tk.Label(
            dialog,
            text=f"📝 Manual Attendance Override",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)
        
        tk.Label(
            dialog,
            text=f"Subject: {subject_name}",
            font=("Segoe UI", 11)
        ).pack(pady=5)
        
        # Calculate current values
        end_date = datetime.now().strftime("%Y-%m-%d")
        if app_data.get("semester_end"):
            end_date = min(end_date, app_data["semester_end"])
        
        weeks = calculate_weeks_elapsed(
            app_data["semester_start"],
            end_date,
            app_data.get("holidays", [])
        )
        
        # Check for existing override
        has_override = subject_data.get("attendance_override") is not None
        if has_override:
            current_attended = subject_data["attendance_override"]["attended"]
            current_total = subject_data["attendance_override"]["total"]
        else:
            if subject_data.get("total_override") is not None:
                current_total = subject_data["total_override"]
            else:
                current_total = calculate_total_classes(subject_data["weekly_count"], weeks)
            
            absent_count = len(subject_data.get("absent_dates", []))
            current_attended = max(0, current_total - absent_count)
        
        # Current data frame
        current_frame = tk.LabelFrame(dialog, text="📊 Current Data", font=("Segoe UI", 10, "bold"))
        current_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            current_frame,
            text=f"Attended: {current_attended} classes",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Label(
            current_frame,
            text=f"Total: {current_total} classes",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        current_pct = calculate_attendance(current_attended, current_total)
        status_color = COLOR_SAFE if current_pct >= 75 else COLOR_RISK
        
        tk.Label(
            current_frame,
            text=f"Attendance: {current_pct:.1f}%",
            font=("Segoe UI", 10, "bold"),
            foreground=status_color
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        if has_override:
            tk.Label(
                current_frame,
                text="⚠️ Manual override is active",
                font=("Segoe UI", 9),
                foreground="#ff9800"
            ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Override inputs frame
        input_frame = tk.LabelFrame(dialog, text="✏️ Override Attendance", font=("Segoe UI", 10, "bold"))
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            input_frame,
            text="Enter actual attendance data:",
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Total classes input
        tk.Label(input_frame, text="Total Classes Held:", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10, pady=(10, 0))
        total_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=15)
        total_entry.insert(0, str(current_total))
        total_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        # Attended classes input
        tk.Label(input_frame, text="Classes Attended:", font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10, pady=(10, 0))
        attended_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=15)
        attended_entry.insert(0, str(current_attended))
        attended_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        # Info label
        tk.Label(
            dialog,
            text="💡 Use this when actual attendance differs from timetable\n(cancellations, rescheduling, extra classes, etc.)",
            font=("Arial", 8),
            foreground="#6c757d",
            justify=tk.CENTER
        ).pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        def save_override():
            try:
                total = int(total_entry.get())
                attended = int(attended_entry.get())
                
                if total < 0 or attended < 0:
                    messagebox.showerror("Error", "Values must be non-negative")
                    return
                
                if attended > total:
                    messagebox.showerror("Error", "Attended cannot be greater than total")
                    return
                
                # Save override
                subject_data["attendance_override"] = {
                    "total": total,
                    "attended": attended
                }
                
                save_data()
                self.refresh_all_tabs()
                dialog.destroy()
                messagebox.showinfo("Success", f"Manual override applied for {subject_name}")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        def clear_override():
            if not has_override:
                messagebox.showinfo("Info", "No override exists for this subject")
                return
            
            if messagebox.askyesno("Confirm", "Remove manual override and use calculated attendance?"):
                subject_data["attendance_override"] = None
                save_data()
                self.refresh_all_tabs()
                dialog.destroy()
                messagebox.showinfo("Success", f"Manual override removed for {subject_name}")
        
        ttk.Button(btn_frame, text="💾 Save Override", command=save_override).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Clear Override", command=clear_override).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
