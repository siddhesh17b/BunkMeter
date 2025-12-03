# Timetable Upload Guide

## Quick Start

### Export → Edit → Import (Easiest Way)

1. **Setup Tab → Export Template** → saves CSV file
2. **Open CSV** in Excel or Notepad
3. **Edit** your times and subjects
4. **Setup Tab → Import** → select your file
5. Done. No restart needed.

---

## CSV Format (Simple)

Must have 3 columns: `Day,Time,Subject`

```csv
Day,Time,Subject
MONDAY,09:00-10:00,Math
MONDAY,10:00-11:00,Physics
MONDAY,12:00-01:00,Lunch Break
TUESDAY,09:00-10:00,Chemistry
```

### Rules:

**Day:**
- MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
- Uppercase required
- Include all 6 days even if no classes

**Time:**
- ANY format works: `09:00-10:00`, `08:00-09:00`, `2:30-3:30 PM`
- No validation - write whatever
- Any duration: `08:00-10:00` (2 hours) is fine

**Subject:**
- ANY name works: `Math`, `CS101 - Algorithms`, `Lab Session 3`
- Kept exactly as you type it
- Only "Lunch" keyword is ignored for attendance

---

## Different Batches, Different Classes

For labs where batches have different subjects:

```csv
Day,Time,Subject
WEDNESDAY,03:00-04:00,CN Lab (B1&B3) / DAA Lab (B2&B4)
```

App shows:
- B1/B3 students see: CN Lab
- B2/B4 students see: DAA Lab

Works with custom batch names too: `(GroupA) / (GroupB)`

---

## Examples

### Simple Timetable:
```csv
Day,Time,Subject
MONDAY,09:00-10:00,Math
MONDAY,10:00-11:00,Physics
MONDAY,11:00-12:00,Chemistry
MONDAY,12:00-01:00,Lunch Break
TUESDAY,09:00-10:00,Biology
TUESDAY,10:00-11:00,English
```

### With Early Classes:
```csv
Day,Time,Subject
MONDAY,08:00-09:00,Extra Class
MONDAY,09:00-10:00,Math
MONDAY,10:00-11:00,Physics
```

### With Custom Names:
```csv
Day,Time,Subject
MONDAY,09:00-10:00,CS101 - Data Structures
MONDAY,10:00-11:00,MATH201 - Calculus II
MONDAY,11:00-12:00,Advanced Java Programming
```

---

## Errors & Fixes

**"Invalid CSV format"**
- Fix: Must have exactly 3 columns (Day, Time, Subject)
- Check for missing commas

**"Missing days"**
- Fix: Include all 6 days (MONDAY to SATURDAY)
- Empty days are fine: `SATURDAY,09:00-10:00,`

**"Invalid day"**
- Fix: Days must be MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
- Must be uppercase

**Subjects not appearing**
- Check: Subject name doesn't contain "Lunch"
- All other names are tracked automatically

---

## Need Help?

**Can't import:** Make sure CSV has Day, Time, Subject columns with commas  
**Wrong subjects showing:** Check batch selection in Setup tab  
**Want to start over:** Setup Tab → Reset to Default → Then import your CSV  

**GitHub Issues:** https://github.com/siddhesh17b/MyAttendance/issues

---

Made by Siddhesh Bisen ([@siddhesh17b](https://github.com/siddhesh17b))
