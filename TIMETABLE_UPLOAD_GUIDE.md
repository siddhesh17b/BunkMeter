# Timetable Upload Guide

## Overview
MyAttendance now supports custom timetable upload! Users can create their own timetable CSV file and import it into the application.

## CSV Format

### Structure
Your CSV file should follow this structure:
- **Column 1**: Day of the week (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)
- **Column 2**: Time slot (format: HH:MM-HH:MM, e.g., 09:00-10:00)
- **Column 3**: Subject details

### Example CSV:
```csv
Day,Time,Subject
MONDAY,09:00-10:00,Minor
MONDAY,10:00-11:00,24HS03TH0301-DM (DT203)
MONDAY,11:00-12:00,24CS01TH0302-DAA (DT203)
MONDAY,12:00-01:00,Lunch Break
MONDAY,01:00-02:00,24CS01TH0301-TOC (DT203)
MONDAY,02:00-03:00,24CS01TH0304-CN (DT203)
TUESDAY,09:00-10:00,Minor
TUESDAY,10:00-11:00,24CS01TH0304-CN (DT203)
...
```

### Important Rules:

1. **Time Slots**: Use 8 hourly slots from 09:00 to 17:00
   - 09:00-10:00, 10:00-11:00, 11:00-12:00, 12:00-01:00
   - 01:00-02:00, 02:00-03:00, 03:00-04:00, 04:00-05:00

2. **Subject Format**:
   - Simple: `DM`, `DAA`, `TOC`, `CN`
   - With code: `24CS01TH0302-DAA (DT203)`
   - Labs: `24CS01PR0304-CN Lab (DT105)`
   - Batch-specific labs: `CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)`

3. **Special Entries**:
   - `Lunch Break` - Ignored for attendance
   - `Minor`, `MDM`, `OE`, `HONORS` - Tracked as subjects
   - `Mentor-Mentee Meeting` - Ignored
   - Empty slots: Leave subject blank or use empty string

4. **Batch-Aware Labs**:
   - Format: `Subject1 (Location1) (B1&B3) / Subject2 (Location2) (B2&B4)`
   - Example: `CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)`
   - App will automatically show correct lab based on batch selection

## How to Upload

1. **Prepare Your CSV**:
   - Create a CSV file with structure above
   - Save as `my_timetable.csv` or any name you prefer
   - Ensure all days (MONDAY-SATURDAY) are included

2. **Export Template** (Optional):
   - Open MyAttendance app
   - Go to **Setup Tab**
   - Click **"Export Timetable Template"** button
   - This generates a CSV with current timetable format

3. **Import Your Timetable**:
   - Go to **Setup Tab**
   - Click **"Import Custom Timetable"** button
   - Select your CSV file
   - Review the preview/confirmation
   - Click **"Confirm Import"**

4. **Verify**:
   - Go to **Timetable Tab** to view imported schedule
   - Check **Mark Attendance Tab** to ensure subjects are listed correctly
   - Go to **Summary Tab** to see all tracked subjects

## Subject Naming

The app automatically extracts clean subject names:
- `24CS01TH0302-DAA (DT203)` → `DAA`
- `24CS01PR0304-CN Lab (DT105)` → `CN Lab`
- `24HS03TH0301-DM (DT203)` → `DM`

## Troubleshooting

### CSV Format Errors
- **Error**: "Invalid CSV format"
  - **Fix**: Ensure CSV has 3 columns: Day, Time, Subject
  - Check for missing commas or extra columns

### Time Slot Issues
- **Error**: "Invalid time format"
  - **Fix**: Use format HH:MM-HH:MM (24-hour format)
  - Example: `09:00-10:00`, `01:00-02:00`

### Missing Days
- **Error**: "Missing required days"
  - **Fix**: Include all days from MONDAY to SATURDAY
  - Each day must have all 8 time slots

### Subjects Not Appearing
- **Issue**: Subject not showing in attendance
  - **Check**: Subject name is not "Lunch Break", "Minor", "OE", or "Mentor-Mentee"
  - **Fix**: Rename subject if it contains excluded keywords

## Sample CSV Files

### Minimal Example (One Day):
```csv
Day,Time,Subject
MONDAY,09:00-10:00,Math
MONDAY,10:00-11:00,Physics
MONDAY,11:00-12:00,Chemistry
MONDAY,12:00-01:00,Lunch Break
MONDAY,01:00-02:00,Biology
MONDAY,02:00-03:00,English
MONDAY,03:00-04:00,
MONDAY,04:00-05:00,
```

### Full Week Example:
Available in the exported template from the app.

## Best Practices

1. ✅ **Backup First**: Export current timetable before importing new one
2. ✅ **Test Import**: Import and verify before deleting backup
3. ✅ **Consistent Naming**: Use same subject names throughout (e.g., "DAA" not "daa" or "Data Structures")
4. ✅ **Include All Days**: Always include Saturday even if no classes
5. ✅ **Clear Formatting**: Remove special characters that might cause parsing issues

## Advanced: Batch-Specific Schedule

If different batches have different labs:
```csv
Day,Time,Subject
WEDNESDAY,03:00-04:00,CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)
WEDNESDAY,04:00-05:00,CN Lab (DT105) (B1&B3) / DAA Lab (DT111) (B2&B4)
```

This will show:
- **B1/B3 students**: CN Lab on Wednesday 3-5pm
- **B2/B4 students**: DAA Lab on Wednesday 3-5pm

## Support

For issues or questions:
- Check this guide first
- Review the exported template for correct format
- Ensure CSV encoding is UTF-8
- Contact: [GitHub Issues](https://github.com/siddhesh17b/MyAttendance/issues)

---

**Author**: Siddhesh Bisen  
**GitHub**: https://github.com/siddhesh17b  
**Project**: MyAttendance - Smart Attendance Tracker
