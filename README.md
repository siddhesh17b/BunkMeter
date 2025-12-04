# MyAttendance

**Track your college attendance and know exactly how many classes you can skip.**

Most colleges require **75% minimum attendance**. Fall below and you can't sit for exams. This app helps you stay above that line.

![Mark Attendance Tab](screenshots/mark_attendance_tab.png)

---

## Quick Start

```bash
pip install tkcalendar
python app.py
```

That's it! The app will guide you through setup on first run.

---

## What This Does

You tell it your class schedule. It tracks which days you were absent. It tells you:
- Your current attendance %
- How many more classes you can safely skip
- Which subjects are at risk (below 75%)

---

## First Time Setup

### Step 1: Install Python
Download from [python.org](https://python.org). During install, **check "Add Python to PATH"**.

### Step 2: Get the App
```bash
git clone https://github.com/siddhesh17b/MyAttendance.git
cd MyAttendance
```
Or: Click green "Code" button → "Download ZIP" → Extract

### Step 3: Install & Run
```bash
pip install tkcalendar
python app.py
```

---

## First Run: What You'll See

1. **Batch Selection Popup** - Choose your batch (like B1, B2, Group A, etc.)
   - *What's a batch?* If your class is divided into groups for labs, that's your batch
   - If your college doesn't have batches, just pick any option

2. **Setup Tab** - Set your semester dates
   - Pick semester start and end dates (check your college calendar)
   - Add holidays (Diwali break, etc.)

![Setup Tab](screenshots/setup_tab.png)

3. **You're done!** The app now knows your schedule.

---

## Daily Use

### Mark Absences (Attendance Tab)
- **Left-click a date** → Opens side panel to mark specific subjects absent
- **Right-click a date** → Marks the ENTIRE day absent (quick option when you bunked everything)

The calendar shows:
| Color | Meaning |
|-------|---------|
| Green | All classes attended |
| Pink | Some classes missed |
| Dark Red | Whole day absent |
| Yellow | Holiday |
| Blue | Today |

### Check Your Status (Summary Tab)
See all subjects with:
- Current attendance %
- Classes you can still skip
- 🟢 Safe / 🔴 At Risk indicators

**Pro tip:** Double-click any subject to manually override attendance (useful when professor cancels class)

---

## Your Weekly Schedule (Timetable Tab)

View your entire week at a glance. Each subject gets a unique color.

![Timetable Tab](screenshots/timetable_tab.png)

---

## Using Your Own Timetable

The app has a default timetable built-in. To use your own:

1. Go to **Setup Tab** → Click **Import Custom Timetable**
2. Select your CSV file
3. Done!

### 📁 Sample Timetables Included

The repo includes **ready-to-use test timetables** you can try:

| File | Description |
|------|-------------|
| `test_timetable-1.csv` | Full week schedule with Group A / Group B batches |
| `test_timetable-2.csv` | Alternative timetable format |

Try importing one to see how it works!

### CSV Format (3 columns):
```csv
Day,Time,Subject
MONDAY,09:00-10:00,Mathematics
MONDAY,10:00-11:00,Physics
TUESDAY,09:00-10:00,Chemistry
```

For batch-specific classes:
```csv
MONDAY,02:00-04:00,Physics Lab (Group A) / Chemistry Lab (Group B)
```

📖 **[Full Timetable Guide →](COMPLETE_GUIDE.md)** - Detailed format rules, examples, troubleshooting

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Run `pip install tkcalendar` |
| `ModuleNotFoundError` | Make sure you're in the app folder when running |
| Wrong attendance showing | Check semester dates in Setup tab |
| Subject missing | Import a custom timetable with your subjects |
| Data lost after restart | Normal - `data.json` stores everything |

---

## Files Explained

| File | Purpose |
|------|---------|
| `app.py` | **Run this to start the app** |
| `data.json` | Your attendance data (auto-created, don't delete!) |
| `custom_timetable.json` | Your uploaded timetable (if any) |
| `test_timetable-1.csv` | Sample timetable you can import |
| `test_timetable-2.csv` | Another sample timetable |
| `COMPLETE_GUIDE.md` | Detailed timetable CSV format guide |

---

## Features

- ✅ Google Calendar-style monthly view
- ✅ One-click "mark whole day absent"
- ✅ Automatic "safe to skip" calculation
- ✅ Holiday management
- ✅ Custom timetable import (CSV)
- ✅ Manual attendance override
- ✅ Export attendance report
- ✅ Works offline (no internet needed)

---

## License

MIT License - feel free to use and modify!

---

Made by **Siddhesh Bisen** • [GitHub](https://github.com/siddhesh17b)
