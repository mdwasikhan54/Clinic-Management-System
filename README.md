<div align="center">

# 🏥 Clinic Management System
### *Advanced Python CLI Application*

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-Text%20File%20System-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

<br>

> A comprehensive, terminal-based solution to manage clinic operations, patient queues, digital prescriptions, and pharmacy inventory without needing a heavy SQL database.

[View Demo](#-project-demo) • [Features](#-key-features) • [Installation](#-installation--usage) • [Structure](#-project-structure)

</div>

---

## 📺 Project Demo

Watch the full system in action! Click the banner below to play the video.

<a href="https://www.youtube.com/watch?v=F59Zkkpb-bM" target="_blank">
  <img src="https://img.youtube.com/vi/F59Zkkpb-bM/maxresdefault.jpg" alt="Watch the Demo System">
</a>

## 🌟 Key Features

This system is divided into two secure modules based on user roles:

### 👨‍💼 Manager Module
* **📋 Serial Management:** Take patient entries and generate unique serial tokens.
* **🗂️ Queue Control:** View active waiting lists and cancel serials if necessary.
* **💊 Inventory Control:** Complete CRUD (Create, Read, Update, Delete) operations for medicines.
* **📊 Sales Reporting:** * View daily sales logs.
    * Generate item-wise summary reports.
    * Filter sales history by specific dates.

### 👨‍⚕️ Doctor Module
* **🩺 Live Queue:** See real-time patients waiting for consultation.
* **📝 Digital Prescription:** * Auto-fetches patient info (Name, Age, Gender).
    * Add medicines with dosage (e.g., `1+0+1`) and duration.
    * Prescribe clinical tests.
* **🆔 Smart Search:** Find patients using Phone Number or Smart ID.
* **📜 History Tracking:** View past prescriptions and visit history of any patient.

### 🔐 Core System Features
* **Security:** Password masking during login (works on both Windows & Linux).
* **Smart ID Generation:** Creates unique IDs (e.g., `J0018`) based on time and phone number logic.
* **Data Persistence:** Uses a structured file handling system (`.txt`) to save all data permanently.

---

## 🛠️ Tech Stack

* **Language:** Python 3 (Core)
* **Data Storage:** Flat File Database (`|` separated values)
* **Libraries Used:** `sys`, `os`, `datetime`, `random`, `string`, `getpass` (No external pip install required!)

---

## 🚀 Installation & Usage

Follow these steps to run the project on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/mdwasikhan54/Clinic-Management-System.git
cd Clinic-Management-System
````

### 2\. Run the Application

```bash
python main.py
```

### 3\. Login Credentials

Use the default credentials stored in the system to log in:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Manager** 👔 | `manager1` | `pass123` | Inventory, Sales, Appt. |
| **Doctor** 🩺 | `doctor1` | `doc123` | Patient Queue, Prescriptions |

-----

## 📂 Project Structure

```bash
Clinic-Management-System/
├── 📂 data/                 # The brain of the database
│   ├── drugs.txt           # Inventory stock
│   ├── patients.txt        # Prescriptions & History
│   ├── sales.txt           # Sales records
│   ├── serials.txt         # Daily queue
│   └── users.txt           # Auth credentials
│
├── main.py                 # 🚀 Entry Point
├── authentication.py       # Login logic
├── database.py             # File handling & Utilities
├── doctor.py               # Doctor class & methods
├── manager.py              # Manager class & methods
├── drug_manager.py         # Pharmacy logic
└── user.py                 # Base User class
```

-----

## 📸 Highlights (Code Snippets)

**Smart ID Generation Logic:**

```python
def generate_smart_id(phone, time_str):
    # Generates a unique 5-character alphanumeric ID
    # based on the hour and phone digits.
    prefix = string.ascii_uppercase[hour % 26]
    final_id = candidate[:5]
    return final_id
```

**Secure Password Input:**

```python
# Hides password typing in the terminal
import msvcrt # Windows
import termios # Linux
```

-----

### 👨‍💻 Developed by [MD WASI KHAN](https://mdwasikhan-portfolio.netlify.app/) 

If you find this project helpful, please drop a ⭐ star on the repo\!

[GitHub Profile](https://github.com/mdwasikhan54)
