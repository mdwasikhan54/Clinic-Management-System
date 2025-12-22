import os
from datetime import datetime
import re
import random

# ====================== CONFIGURATION & DATABASE ======================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Database Helper Functions ---
def load_data(filename):
    """Loads pipe-separated data from text files."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip().split('|') for line in f if line.strip() and '|' in line]

def load_raw_lines(filename):
    """Loads raw text lines (used for reading full prescription text)."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def save_data(filename, data):
    """Saves structured data back to file."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for row in data:
            f.write('|'.join(map(str, row)) + '\n')

def append_data(filename, line):
    """Appends a new record to the file."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def delete_line(filename, index):
    """Deletes a specific line by index."""
    data = load_data(filename)
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_data(filename, data)
        return removed
    return None

def get_next_id(filename):
    """Generates auto-increment ID."""
    data = load_data(filename)
    if not data:
        return "1"
    ids = [int(row[0]) for row in data if row and row[0].isdigit()]
    return str(max(ids) + 1) if ids else "1"

def format_datetime(dt_str):
    """Formats datetime string for display."""
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        return f"{dt.day} {dt.strftime('%b %Y')}, {dt.strftime('%I:%M %p')}"
    except:
        return dt_str

def generate_smart_id(phone, time_str):
    """Generates a unique 5-char Smart ID based on logic."""
    clean_phone = ''.join(filter(str.isdigit, phone))[-6:]
    try:
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        hour = dt.hour % 12
        minute = dt.minute
    except:
        hour, minute = 0, 0
    prefix = chr(65 + (hour % 26))
    phone_part = clean_phone[-4:].zfill(4)
    extra = str(minute % 10)
    candidate = f"{prefix}{phone_part}{extra}"
    existing = {str(row[4]) for row in load_data("serials.txt") if len(row) > 4}
    final_id = candidate
    attempts = 0
    while final_id in existing and attempts < 10:
        final_id = f"{prefix}{phone_part[-3:]}{random.randint(0,9)}{random.randint(0,9)}"
        attempts += 1
    return final_id