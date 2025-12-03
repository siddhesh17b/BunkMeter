"""
Data Manager - Timetable and JSON persistence
Handles hardcoded timetable data and subject management

Author: Siddhesh Bisen
GitHub: https://github.com/siddhesh17b
"""

import json
import os
import csv
from tkinter import messagebox, filedialog
from collections import defaultdict

DATA_FILE = "data.json"
CUSTOM_TIMETABLE_FILE = "custom_timetable.json"
TIMETABLE_DATA = {
    "MONDAY": {
        "09:00-10:00": "Minor",
        "10:00-11:00": "24HS03TH0301-DM (DT203)",
        "11:00-12:00": "24CS01TH0302-DAA (DT203)",
        "12:00-01:00": "Lunch Break",
        "01:00-02:00": "24CS01TH0301-TOC (DT203)",
        "02:00-03:00": "24CS01TH0304-CN (DT203)",
        "03:00-04:00": "",
        "04:00-05:00": ""
    },
    "TUESDAY": {
        "09:00-10:00": "Minor",
        "10:00-11:00": "24CS01TH0304-CN (DT203)",
        "11:00-12:00": "24CS01TH0301-TOC (DT203)",
        "12:00-01:00": "Lunch Break",
        "01:00-02:00": "24CS01TH0302-DAA (DT203)",
        "02:00-03:00": "",
        "03:00-04:00": "",
        "04:00-05:00": ""
    },
    "WEDNESDAY": {
        "09:00-10:00": "Minor",
        "10:00-11:00": "",
        "11:00-12:00": "",
        "12:00-01:00": "24HS03TH0301-DM (DT203)",
        "01:00-02:00": "Lunch Break",
        "02:00-03:00": "24CS01TH0302-DAA (DT203)",
        "03:00-04:00": "24CS01PR0304-CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)",
        "04:00-05:00": "24CS01PR0304-CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)"
    },
    "THURSDAY": {
        "09:00-10:00": "MDM",
        "10:00-11:00": "",
        "11:00-12:00": "24HS03TH0301-DM (DT203)",
        "12:00-01:00": "Lunch Break",
        "01:00-02:00": "24CS01TH0301-TOC (DT304)",
        "02:00-03:00": "24CS01PR0304-CN Lab (DT105) (B2&B4) / DAA Lab (DT111) (B1&B3)",
        "03:00-04:00": "24CS01PR0304-CN Lab (DT105) (B2&B4) / DAA Lab (DT111) (B1&B3)",
        "04:00-05:00": ""
    },
    "FRIDAY": {
        "09:00-10:00": "MDM",
        "10:00-11:00": "24CS01PR0303-Software Lab (DT105) (B1&B3) / Software Lab (DT111) (B2&B4)",
        "11:00-12:00": "24CS01PR0303-Software Lab (DT105) (B1&B3) / Software Lab (DT111) (B2&B4)",
        "12:00-01:00": "Lunch Break",
        "01:00-02:00": "24CS01TH0304-CN (DT212)",
        "02:00-03:00": "Technical Skill session (DT109)",
        "03:00-04:00": "Technical Skill session (DT109)",
        "04:00-05:00": ""
    },
    "SATURDAY": {
        "09:00-10:00": "MDM",
        "10:00-11:00": "OE",
        "11:00-12:00": "Mentor-Mentee Meeting Slot",
        "12:00-01:00": "HONORS (DT301)",  # 12:00-12:30 Lunch, 12:30-1:00 HONORS
        "01:00-02:00": "HONORS (DT301)",
        "02:00-03:00": "HONORS (DT301)",
        "03:00-04:00": "HONORS (DT301)",  # Ends at 3:30
        "04:00-05:00": ""
    }
}

app_data = {
    "batch": None,
    "semester_start": None,
    "semester_end": None,
    "holidays": [],
    "subjects": []
}

def extract_subject_name(cell_value):
    if not cell_value or cell_value.strip() == "":
        return None
    cell_value = cell_value.strip()
    if "Lunch" in cell_value or cell_value == "":
        return None
    if cell_value in ["Minor", "OE"] or "Mentor-Mentee" in cell_value:
        return None
    if cell_value == "MDM":
        return "MDM"
    if "HONORS" in cell_value:
        return "HONORS"
    if "Technical Skill" in cell_value:
        return "Technical Skill"
    if "-" in cell_value:
        parts = cell_value.split("-")
        if len(parts) >= 2:
            subject = parts[1].split("(")[0].strip()
            if "Lab" in subject:
                return subject.split("DT")[0].strip()
            return subject
    return cell_value


def parse_timetable_csv(batch):
    subject_counts = defaultdict(int)
    try:
        active_timetable = get_active_timetable()
        for day, time_slots_dict in active_timetable.items():
            for time_slot, cell_value in time_slots_dict.items():
                if not cell_value or cell_value == "Lunch Break":
                    continue
                subject = extract_subject_name(cell_value)
                if subject:
                    if "/" in cell_value and ("B1&B3" in cell_value or "B2&B4" in cell_value):
                        parts = cell_value.split("/")
                        for part in parts:
                            if batch in ["B1/B3", "B1", "B3"] and "B1&B3" in part:
                                lab_subject = extract_subject_name(part.split("(")[0])
                                if lab_subject:
                                    subject_counts[lab_subject] += 1
                                    break
                            elif batch in ["B2/B4", "B2", "B4"] and "B2&B4" in part:
                                lab_subject = extract_subject_name(part.split("(")[0])
                                if lab_subject:
                                    subject_counts[lab_subject] += 1
                                    break
                    else:
                        subject_counts[subject] += 1
        return dict(subject_counts)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse timetable: {str(e)}")
        return {}


def get_subjects_for_day(day_name, batch):
    subjects = []
    day_upper = day_name.upper()
    active_timetable = get_active_timetable()
    if day_upper not in active_timetable:
        return []
    try:
        time_slots_dict = active_timetable[day_upper]
        for time_slot, cell_value in time_slots_dict.items():
            if not cell_value or cell_value == "Lunch Break":
                continue
            subject = extract_subject_name(cell_value)
            if subject:
                if "/" in cell_value and ("B1&B3" in cell_value or "B2&B4" in cell_value):
                    parts = cell_value.split("/")
                    for part in parts:
                        if batch in ["B1/B3", "B1", "B3"] and "B1&B3" in part:
                            lab_subject = extract_subject_name(part.split("(")[0])
                            if lab_subject and lab_subject not in subjects:
                                subjects.append(lab_subject)
                                break
                        elif batch in ["B2/B4", "B2", "B4"] and "B2&B4" in part:
                            lab_subject = extract_subject_name(part.split("(")[0])
                            if lab_subject and lab_subject not in subjects:
                                subjects.append(lab_subject)
                                break
                else:
                    if subject not in subjects:
                        subjects.append(subject)
    except Exception as e:
        print(f"Error reading timetable for day {day_name}: {e}")
    return subjects

def save_data():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(app_data, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

def load_data():
    global app_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                app_data = json.load(f)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            return False
    return False

def get_app_data():
    return app_data


def get_active_timetable():
    """Get the active timetable (custom if exists, otherwise default)"""
    if os.path.exists(CUSTOM_TIMETABLE_FILE):
        try:
            with open(CUSTOM_TIMETABLE_FILE, 'r') as f:
                custom_timetable = json.load(f)
                return custom_timetable
        except Exception as e:
            print(f"Error loading custom timetable: {e}")
            return TIMETABLE_DATA
    return TIMETABLE_DATA


def export_timetable_to_csv(filepath=None):
    """Export current timetable to CSV format"""
    if not filepath:
        filepath = filedialog.asksaveasfilename(
            title="Export Timetable",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="my_timetable.csv"
        )
    
    if not filepath:
        return False
    
    try:
        active_timetable = get_active_timetable()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Day', 'Time', 'Subject'])
            
            days_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
            time_slots = ['09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-01:00',
                         '01:00-02:00', '02:00-03:00', '03:00-04:00', '04:00-05:00']
            
            for day in days_order:
                if day in active_timetable:
                    for time_slot in time_slots:
                        subject = active_timetable[day].get(time_slot, '')
                        writer.writerow([day, time_slot, subject])
        
        messagebox.showinfo("Success", f"Timetable exported successfully to:\n{filepath}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export timetable: {str(e)}")
        return False


def import_timetable_from_csv(filepath=None):
    """Import custom timetable from CSV file"""
    if not filepath:
        filepath = filedialog.askopenfilename(
            title="Import Custom Timetable",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
    
    if not filepath:
        return False
    
    try:
        new_timetable = {}
        required_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
        time_slots = ['09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-01:00',
                     '01:00-02:00', '02:00-03:00', '03:00-04:00', '04:00-05:00']
        
        # Initialize structure
        for day in required_days:
            new_timetable[day] = {slot: '' for slot in time_slots}
        
        # Read CSV
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate headers
            if not all(col in reader.fieldnames for col in ['Day', 'Time', 'Subject']):
                messagebox.showerror("Error", "CSV must have columns: Day, Time, Subject")
                return False
            
            for row in reader:
                day = row['Day'].strip().upper()
                time = row['Time'].strip()
                subject = row['Subject'].strip()
                
                if day not in required_days:
                    messagebox.showwarning("Warning", f"Invalid day: {day}. Skipping...")
                    continue
                
                if time not in time_slots:
                    messagebox.showwarning("Warning", f"Invalid time slot: {time}. Skipping...")
                    continue
                
                new_timetable[day][time] = subject
        
        # Validate all days present
        for day in required_days:
            if day not in new_timetable or not new_timetable[day]:
                response = messagebox.askyesno(
                    "Missing Days",
                    f"Day {day} is missing or incomplete. Continue anyway?"
                )
                if not response:
                    return False
        
        # Preview and confirm
        subject_count = sum(1 for day in new_timetable.values() 
                          for subject in day.values() 
                          if subject and subject != 'Lunch Break')
        
        response = messagebox.askyesno(
            "Confirm Import",
            f"Timetable loaded successfully!\n\n"
            f"Days: {len(new_timetable)}\n"
            f"Subjects found: {subject_count}\n\n"
            f"This will replace your current timetable.\n"
            f"Continue?"
        )
        
        if response:
            # Save custom timetable
            with open(CUSTOM_TIMETABLE_FILE, 'w') as f:
                json.dump(new_timetable, f, indent=2)
            
            messagebox.showinfo("Success", "Custom timetable imported successfully!\nRestart the app to apply changes.")
            return True
        
        return False
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import timetable:\n{str(e)}")
        return False


def reset_to_default_timetable():
    """Reset to the default hardcoded timetable"""
    if os.path.exists(CUSTOM_TIMETABLE_FILE):
        response = messagebox.askyesno(
            "Confirm Reset",
            "This will delete your custom timetable and restore the default.\n"
            "Continue?"
        )
        if response:
            try:
                os.remove(CUSTOM_TIMETABLE_FILE)
                messagebox.showinfo("Success", "Timetable reset to default.\nRestart the app to apply changes.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset timetable: {str(e)}")
                return False
    else:
        messagebox.showinfo("Info", "Already using default timetable.")
        return False
