# MyAttendance - 75% Rule Tracker

Track college attendance, never drop below 75%, know exactly how many classes you can skip.

## Install & Run (30 seconds)

```bash
git clone https://github.com/siddhesh17b/MyAttendance.git
cd MyAttendance
pip install tkcalendar
python app.py
```

That's it. Windows/Mac/Linux all work.

---

## First Time Setup (Do This ONCE)

### Step 1: Set Your Timetable

**Option A: Use Your Own Timetable (Recommended)**
1. Open app → Go to **Setup Tab**
2. Click **"📤 Export Timetable Template"** - saves a CSV file
3. Open the CSV in Excel/Notepad
4. Edit it with YOUR timetable (see format below)
5. Click **"📥 Import Custom Timetable"**
6. Select your batch (B1/B3 or B2/B4 or whatever your college uses)

**CSV Format:**
```csv
Day,Time,Subject
MONDAY,09:00-10:00,Data Mining
MONDAY,10:00-11:00,Algorithms
MONDAY,11:00-12:00,Lunch Break
WEDNESDAY,03:00-05:00,Lab (B1&B3) / Different Lab (B2&B4)
```
- Day: MONDAY to SATURDAY (uppercase)
- Time: Any format you want (08:00-09:00, 2:30-3:30 PM, whatever)
- Subject: Any name. For different labs per batch use `Subject1 (B1&B3) / Subject2 (B2&B4)`

**Option B: Use Default Timetable**
1. Select your batch (B1/B3 or B2/B4)
2. App loads default timetable automatically
3. You can export → edit → import later

### Step 2: Set Semester Dates
1. Setup Tab → Pick semester start date
2. Pick semester end date
3. Done.

### Step 3: Mark Attendance
Go to **"Mark Attendance"** tab. That's your main screen.

---

## Daily Use (10 seconds)

### Calendar Tab - Your Main Screen

**Left-click a date** → Uncheck subjects you were absent → Save  
**Right-click a date** → Toggles entire day (absent ↔ present)

**Colors mean:**
- 🟢 Green = All present
- 🔴 Light Red = Some absent
- 🔴 Dark Red = All absent (completely skipped)
- 🟡 Yellow = Holiday
- Gray = Future dates

**Right-click to toggle:** Present → All absent → Present (quick undo!)

### Summary Tab - See Your Status

Shows all subjects with:
- Present/Total classes
- Percentage (must stay ≥75%)
- How many more you can skip
- Visual progress bars (🟢 = safe, 🔴 = danger)

**Double-click any subject** → Manually set attendance (for cancelled classes, make-up lectures, etc.)

---

## Common Tasks

### Add Holidays
Setup Tab → Add Holiday Period → Pick dates → Save

### Mark Sick Leave (Multiple Days)
Setup Tab → Add Skipped Period → Pick date range → Auto-marks all classes absent

### Reset Everything (New Semester)
Setup Tab → Reset Data → Confirms → Fresh start (keeps your timetable)

### Reset Timetable Too
Setup Tab → Reset to Default → Loads hardcoded timetable → Then export/edit/import your own

### Change Timetable Mid-Semester
1. Export current → Edit CSV → Import
2. Or click "Reset to Default" first, then import yours

---

## Key Features

- **You're present by default** - Only click when absent (saves time)
- **Right-click = absent entire day** - Fast when you skip everything
- **Visual dashboard** - Instantly see safe/danger subjects
- **Manual override** - Fix attendance when classes get cancelled/rescheduled
- **Smart batch filtering** - Upload 1 timetable with both batches, app shows only your classes
- **Works offline** - No internet, no account, data stored locally
- **Fast** - Updates instantly, no lag

---

## File Structure

```
MyAttendance/
├── app.py                    # Run this
├── data_manager.py           # Timetable + data handling
├── calculations.py           # Attendance math
├── setup_tab.py              # Configuration screen
├── timetable_tab.py          # Weekly schedule view
├── attendance_calendar.py    # Main calendar screen
├── summary_tab.py            # Dashboard with stats
├── data.json                 # Your data (auto-created)
└── COMPLETE_GUIDE.md         # Detailed CSV guide
```

---

## Troubleshooting

**App won't start:** Install tkcalendar → `pip install tkcalendar`

**Wrong labs showing:** Check batch selection (Setup Tab)

**Data not saving:** Run app with file write permissions

**Want fresh start:** Setup Tab → Reset Data (or delete data.json)

**CSV import fails:** Check format - Day must be MONDAY-SATURDAY uppercase, needs Day,Time,Subject columns

---

## Tech

Python 3.8+, Tkinter (built-in), tkcalendar. ~500 lines per file. MIT License.

**Made by:** Siddhesh Bisen ([@siddhesh17b](https://github.com/siddhesh17b))  
**Why:** College project + actually needed this myself

---

## Support

- Check `COMPLETE_GUIDE.md` for detailed CSV format
- Export Template to see example
- [GitHub Issues](https://github.com/siddhesh17b/MyAttendance/issues)

## Screenshots

![Setup Tab](setup_tab.png)
![Timetable Tab](timetable_tab.png)
![Calendar Tab](mark_attendance_tab.png)
