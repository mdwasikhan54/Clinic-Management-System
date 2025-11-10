from user import User
from database import (
    load_data, append_data, 
    load_raw_lines, delete_line, format_datetime)
from datetime import datetime
import sys

class Doctor(User):
    def __init__(self, username):
        super().__init__(username)
        self._role = "Doctor"

    def show_menu(self):
        while self._is_logged_in:
            self._header()
            print("1. Check Patient (by Phone/SmartID)")
            print("2. View History")
            print("3. Logout")
            print("4. Exit")
            ch = input("\nChoice (1-4): ").strip()
            if ch == '1': self.check_patient()
            elif ch == '2': self.view_history()
            elif ch == '3': self.logout()
            elif ch == '4': sys.exit(0)
            else: input("Invalid! Press Enter...")

    def check_patient(self):
        self._header()
        search = input("Patient Phone or SmartID: ").strip()
        serials = load_data("serials.txt")
        today = datetime.now().strftime('%Y-%m-%d')
        patient = None
        index = -1

        for i, s in enumerate(serials):
            if len(s) < 4: continue
            phone_match = s[2] == search
            smart_id_match = len(s) > 4 and s[4] == search
            # today_match = s[3].startswith(today)
            # if (phone_match or smart_id_match) and today_match:
            if (phone_match or smart_id_match):
                patient = s
                index = i
                break

        if not patient:
            print("Patient not in serial.")
            input(); return

        name, phone, smart_id = patient[1], patient[2], (patient[4] if len(patient) > 4 else "N/A")
        rx = {
            "name": name, "phone": phone, "smart_id": smart_id,
            "age": "", "gender": "",
            "meds": [], "tests": [],
            "date": datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        while True:
            self._header()
            print(f"Patient: {name} | Phone: {phone} | SmartID: {smart_id}")
            print("\n1. Info  2. Medicine  3. Test  4. Save  5. Cancel")
            ch = input(">> ").strip()
            if ch == '1':
                rx["age"] = input("Age: ").strip()
                rx["gender"] = input("Gender: ").strip()
            elif ch == '2':
                m = input("Medicine: "); d = input("Dose: "); dur = input("Duration: ")
                if m: rx["meds"].append(f"{m} - {d} - {dur}")
            elif ch == '3':
                t = input("Test: ")
                if t: rx["tests"].append(t)
            elif ch == '4':
                if input("Confirm Save? (y/n): ").lower() != 'y':
                    print("Cancelled.")
                    input(); break
                self.save_rx(rx)
                removed = delete_line("serials.txt", index)
                if removed:
                    append_data("old_patients.txt", "|".join(removed))
                print("Prescription saved! Patient moved to old records.")
                input(); break
            elif ch == '5': break

    def save_rx(self, rx):
        formatted_date = format_datetime(rx['date'])
        rec += f"Name: {rx['name']} │ Phone: {rx['phone']} │ SmartID: {rx['smart_id']}\n"
        rec += f" Visit: {formatted_date} \n"
        
        if rx.get('age'): rec += f"Age: {rx['age']} │ Gender: {rx['gender']}\n"
        rec += "Medicines:\n" + "\n".join([f"  • {m}" for m in rx["meds"]]) + "\n"
        rec += "Tests:\n" + "\n".join([f"  • {t}" for t in rx["tests"]]) + "\n"
        rec += "═" * 60 + "\n"
        append_data("patients.txt", rec)

    def view_history(self):
        self._header()
        search = input("Patient Phone or SmartID: ").strip()
        if not search:
            input("Invalid input! Press Enter...")
            return

        lines = load_raw_lines("patients.txt")
        if not lines:
            print("No history available.")
            input()
            return

        found = False
        current_block = []
        in_block = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith("═" * 60):
                if in_block and search in " ".join(current_block):
                    found = True
                    print("".join(current_block).rstrip("\n"))
                    print() 
                current_block = [line]
                in_block = True

            elif in_block:
                current_block.append(line)

                if (i + 1 < len(lines) and lines[i + 1].strip().startswith("═" * 60)) or (i == len(lines) - 1):
                    if search in " ".join(current_block):
                        found = True
                        print("".join(current_block).rstrip("\n"))
                        print()
                    current_block = []
                    in_block = False

        if in_block and search in " ".join(current_block):
            found = True
            print("".join(current_block).rstrip("\n"))

        if not found:
            print("No history found for this patient.")

        input("Press Enter to continue...")