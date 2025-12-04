"""
Attendance Calculations - Math and date logic
Handles attendance percentage, safe skip calculations, and date utilities

Author: Siddhesh Bisen
GitHub: https://github.com/siddhesh17b
"""

from datetime import datetime

# Color constants
COLOR_SAFE = "#28a745"
COLOR_RISK = "#dc3545"


def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


def is_date_in_holidays(date, holidays):
    """Check if a date falls within any holiday period
    
    Args:
        date: datetime object to check
        holidays: List of holiday dicts with 'start' and 'end' keys
    
    Returns:
        bool: True if date is within any holiday period
    """
    if not date or not holidays:
        return False
    
    for holiday in holidays:
        try:
            start = parse_date(holiday.get('start'))
            end = parse_date(holiday.get('end'))
            if start and end and start <= date <= end:
                return True
        except (KeyError, TypeError, AttributeError):
            # Skip malformed holiday entries
            continue
    return False


def calculate_attendance(attended, total):
    """Calculate attendance percentage"""
    if total == 0:
        return 0.0
    return (attended / total) * 100


def calculate_safe_skip(attended, total, threshold=75):
    """
    Calculate how many classes can be safely skipped while maintaining threshold
    
    Formula derivation:
    - Requirement: attendance% >= 75%
    - After skipping 'x' classes: attended / (total + x) >= 0.75
    - Rearranging: attended >= 0.75 * (total + x)
    - Solve for x: x <= (attended - 0.75 * total) / 0.75
    
    Args:
        attended: Number of classes attended so far
        total: Total classes conducted so far
        threshold: Minimum attendance percentage required (default 75%)
    
    Returns:
        int: Maximum number of classes that can be skipped safely
    
    Example:
        Attended: 80 classes, Total: 100 classes
        Current %: 80%
        Safe skip: (80 - 0.75*100) / 0.75 = (80 - 75) / 0.75 = 6.67 ≈ 6 classes
        After skipping 6: 80/(100+6) = 75.47% (still safe)
    """
    # Edge case validation
    if total == 0 or attended < 0 or total < 0:
        return 0
    
    if threshold <= 0 or threshold > 100:
        threshold = 75  # Default fallback
    
    # Calculate maximum classes that can be skipped
    # Formula: skips = (attended - threshold% * total) / threshold%
    try:
        threshold_decimal = threshold / 100.0
        safe = int((attended - threshold_decimal * total) / threshold_decimal)
        return max(0, safe)  # Never return negative
    except (ZeroDivisionError, OverflowError):
        return 0


def get_attendance_status(percentage):
    """Get status text and color based on percentage"""
    if percentage >= 75:
        return ("Safe", COLOR_SAFE)
    else:
        return ("At Risk", COLOR_RISK)
