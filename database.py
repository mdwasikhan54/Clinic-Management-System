import os
import random
import string
from datetime import datetime

DATA_DIR = "data"

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    users_file = os.path.join(DATA_DIR, "users.txt")
    if not os.path.exists(users_file):
        with open(users_file, 'w', encoding='utf-8') as f:
            f.write("manager1|pass123|Manager\n")
            f.write("doctor1|doc123|Doctor\n")
    old_file = os.path.join(DATA_DIR, "old_patients.txt")
    if not os.path.exists(old_file):
        open(old_file, 'w', encoding='utf-8').close()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip().split('|') for line in f if line.strip() and '|' in line]

def load_raw_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def save_data(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for row in data:
            f.write('|'.join(row) + '\n')

def append_data(filename, line):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def get_next_id(filename):
    data = load_data(filename)
    if not data:
        return "1"
    try:
        ids = [int(row[0]) for row in data if row[0].isdigit()]
        return str(max(ids) + 1) if ids else "1"
    except:
        return str(len(data) + 1)

def delete_line(filename, index):
    data = load_data(filename)
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_data(filename, data)
        return removed
    return None

def format_datetime(dt_str):
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        return f"{dt.day} {dt.strftime('%b %Y')}, {dt.strftime('%I:%M %p')}"
    except:
        return dt_str

def generate_smart_id(phone, time_str):
    clean_phone = ''.join(filter(str.isdigit, phone))[-6:]
    try:
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        hour = dt.hour % 12
        minute = dt.minute
    except:
        hour, minute = 0, 0

    prefix = string.ascii_uppercase[hour % 26]
    phone_part = clean_phone[-4:].zfill(4)
    extra = str(minute % 10)
    candidate = f"{prefix}{phone_part}{extra}"

    final_id = candidate[:5]

    existing = {s[4] for s in load_data("serials.txt") if len(s) > 4}
    attempts = 0
    while final_id in existing and attempts < 10:
        final_id = f"{prefix}{phone_part[-3:]}{random.randint(0,9)}{random.choice(string.digits)}"
        attempts += 1

    return final_id