# MyAttendance

**Track your college attendance. Know exactly how many classes you can skip while staying above 75%.**

![Setup Tab](setup_tab.png)
![Calendar Tab](mark_attendance_tab.png)

---

## Quick Start

```bash
pip install tkcalendar
python app.py
```

First run? The app walks you through setup. Import your timetable CSV or use the default, pick your batch, set semester dates. Done.

---

## How It Works

1. **You're present by default** — Only mark when you're absent
2. **Left-click a date** → Uncheck the classes you missed → Save
3. **Right-click a date** → Skip entire day instantly (click again to undo)
4. **Check Summary tab** → See which subjects are safe 🟢 and which are at risk 🔴

That's the whole app.

---

## Your Timetable

### Option 1: Import Your Own (Recommended)

Go to **Setup → Export Timetable Template** to get a CSV file. Edit it:

```csv
Day,Time,Subject
MONDAY,09:00-10:00,Data Structures
MONDAY,10:00-11:00,Algorithms
TUESDAY,02:00-04:00,Lab (Group A) / Lab (Group B)
```

- **Day**: MONDAY through SATURDAY (uppercase)
- **Time**: Any format works (08:00-09:00, 2-3pm, whatever)
- **Subject**: Any name. For batch-specific: `Subject (BatchA) / Subject (BatchB)`

Import it back via **Setup → Import Custom Timetable**. App auto-detects your batch options.

### Option 2: Use Default

Just select your batch (B1/B3 or B2/B4) and go. You can always import your own later.

---

## Calendar Colors

| Color | Meaning |
|-------|---------|
| White/Green | All present |
| Cyan | Some absent |
| Dark Red | Completely skipped |
| Yellow | Holiday |
| Gray | Sunday or future |

---

## Common Tasks

| Task | How |
|------|-----|
| Mark absent | Left-click date → uncheck subjects → Save |
| Skip entire day | Right-click the date |
| Add holiday | Setup → Add Holiday Period |
| Sick leave (multi-day) | Setup → Add Skipped Period |
| Fix wrong count | Summary → double-click subject → override manually |
| New semester | Setup → Reset Data |

---

## Summary Tab

Your dashboard. Shows for each subject:
- Classes attended / total
- Attendance percentage  
- **How many more you can skip** (the number you actually want)
- Color-coded status (green = safe, red = danger)

Double-click any row to manually override if classes got cancelled or rescheduled.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Won't start | `pip install tkcalendar` |
| Wrong subjects showing | Check batch in Setup tab |
| Import fails | Day must be uppercase (MONDAY not Monday) |
| Want fresh start | Delete `data.json` or use Setup → Reset Data |

---

## Files

- `app.py` — Run this
- `data.json` — Your attendance data (auto-created)
- `custom_timetable.json` — Your imported timetable (if any)
- `COMPLETE_GUIDE.md` — Detailed CSV format guide

---

## Contributing

Issues and PRs welcome. It's a simple Tkinter app, easy to hack on.

---

**Made by** [Siddhesh Bisen](https://github.com/siddhesh17b) — MIT License
