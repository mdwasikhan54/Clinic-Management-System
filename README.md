<div align="center">

# 🏥 Clinic Management System v2.0
### *Professional Python GUI Application*

![Python](https://img.shields.io/badge/Python-3.12.3-blue?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/Interface-Tkinter%20GUI-green?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-Text%20File%20System-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Version-2.0-purple?style=for-the-badge)

<br>

> A comprehensive, desktop-based solution to manage clinic operations, patient queues, digital prescriptions, and pharmacy inventory. **Now upgraded from CLI to a modern, user-friendly Graphical User Interface (GUI).**

[Features](#-key-features) • [Installation](#-installation--usage) • [Tech Stack](#-Tech-Stack) • [Structure](#-project-structure)

</div>

---

## 🚀 What's New in Version 2.0?

We have completely revamped the system from a terminal-based application to a **Full Modular GUI Application**.

* **🖥️ Modern UI:** Built with `Tkinter` & `TTK` for a professional look and feel.
* **🖱️ Interactive Controls:** Buttons, Input Fields, Tabbed Navigation, and Treeview Tables.
* **🏗️ Modular Architecture:** Codebase split into logical modules (`manager`, `doctor`, `database`) for better scalability.
* **📊 Enhanced Reporting:** Searchable sales reports and visual stock management.

---

## 🌟 Key Features

This system is divided into two secure modules based on user roles:

### 👨‍💼 Manager Dashboard
* **📋 Patient Entry:** Graphical form to register new patients and generate smart serial tokens (e.g., `J0018`).
* **🗂️ Queue Management:** View active waiting lists in a table format and cancel appointments with a click.
* **💊 Inventory Control:** View stock in a sortable table.
    * **Edit/Delete** drugs directly from the UI.
    * Visual indicators for expired medicines.
* **📊 Sales Reporting:** **Daily Reports:** Auto-loads today's sales.
    * **Date Search:** Filter sales history by specific dates.
    * **Item Summary:** View total sales per medicine.

### 👨‍⚕️ Doctor Dashboard
* **🩺 Digital Workspace:** A unified tabbed interface for workflow efficiency.
* **📝 Visual Prescription Pad:** Select patients from the live queue.
    * Add medicines and tests using input fields and "Add" buttons.
    * Review the prescription list before saving.
* **🆔 Smart Search:** Instantly verify patient history using Phone Number or Smart ID.
* **📜 History Viewer:** Split-screen view showing the patient list on the left and detailed prescription records on the right.

### 🔐 Core System Features
* **Secure Login:** Role-based authentication (Manager vs. Doctor).
* **Data Persistence:** Uses a structured file handling system (`.txt`) to save all data permanently.
* **Smart ID Logic:** Unique IDs generated based on time and phone logic.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12.3
* **GUI Framework:** `tkinter` (Standard Python Interface), `tkinter.ttk` (Themed Widgets).
* **Data Storage:** Custom file-based NoSQL-style storage system (`|` separated values).
* **Modules Used:** `os`, `datetime`, `re`, `random`, `messagebox`, `simpledialog`.

---

## 📂 Project Structure

The project follows a clean, modular architecture:

```bash
Clinic-Management-System/
│
├── main.py              # 🚀 Entry Point (Run this file)
├── database.py          # 💾 Backend: File handling & Data operations
├── login_module.py      # 🔐 UI: Login screen & Role selection
├── manager_module.py    # 👔 UI: Manager dashboard & Inventory logic
├── doctor_module.py     # 🩺 UI: Doctor dashboard & Prescription logic
│
└── data/                # 📂 Database Storage
    ├── drugs.txt        # Inventory stock data
    ├── patients.txt     # Prescriptions & Medical history
    ├── sales.txt        # Sales logs
    ├── serials.txt      # Daily patient queue
    ├── old_patients.txt # Archived patient list
    └── users.txt        # Auth credentials

```

---

## 🚀 Installation & Usage

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/mdwasikhan54/Clinic-Management-System.git
   cd Clinic-Management-System

2. **Check for Tkinter (Optional):**
Tkinter is included with standard Python installations. No external `pip` install is required. (Linux users might need `sudo apt-get install python3-tk`).

4. **Run Application:**
```bash
  python main.py
  ```

---

### 3. Login Credentials

Use the default credentials stored in the system to log in:

| Role | Username | Password | Access Level |
| --- | --- | --- | --- |
| **Manager** 👔 | `manager` | `pass123` | Inventory, Sales, Appointments |
| **Doctor** 🩺 | `doctor` | `doc123` | Patient Queue, Prescriptions, History |

---

## 📸 Highlights (Code Logic)

**Modular Class Structure (Mixin Approach):**

```python
class ClinicApp(LoginMixin, ManagerMixin, DoctorMixin):
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.show_role_selection()

```

**Smart Data Verification:**

```python
# Checks if the drug name in the prescription matches the stock
if any(m.lower() in d[0].lower() or d[0].lower() in m.lower() for m in meds):
    # Allows sale

```

---

### 👨‍💻 Developed by [MD WASI KHAN](https://mdwasikhan-portfolio.netlify.app/) 

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdwasikhan54)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mdwasikhan54)
</div>

If you find this project helpful, please drop a ⭐ star on the repo\!
