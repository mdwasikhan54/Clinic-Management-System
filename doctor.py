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
            print("1. View Patient Queue")
            print("2. Prescribe Patient")
            print("3. View History")
            print("4. Logout")
            print("5. Exit")
            ch = input("\nChoice (1-5): ").strip()
            
            if ch == '1': self.view_patient_queue()
            elif ch == '2': self.prescribe_patient()
            elif ch == '3': self.view_history()
            elif ch == '4': self.logout()
            elif ch == '5': sys.exit(0)
            else: input("Invalid! Press Enter...")

    def view_patient_queue(self):
        self._header()
        print("TODAY'S PATIENT QUEUE")
        
        data = load_data("serials.txt")
        today = datetime.now().strftime('%Y-%m-%d')
        today_serials = [d for d in data if len(d) > 3 and d[3].startswith(today)]
        
        if not today_serials:
            print("\nNo patients waiting in queue today.")
            input("Press Enter...")
            return

        w_id, w_sid, w_name, w_phone = 4, 8, 18, 14
        header = f"{'SL':<{w_id}} │ {'SmartID':<{w_sid}} │ {'Name':<{w_name}} │ {'Phone':<{w_phone}}"
        separator = "─" * len(header)

        print("\n" + header)
        print(separator)
        
        for i, d in enumerate(today_serials, 1):
            smart_id = d[4] if len(d) > 4 else "N/A"
            print(f"{i:<{w_id}} │ {smart_id:<{w_sid}} │ {d[1]:<{w_name}} │ {d[2]:<{w_phone}}")
            
        print("\nTotal Waiting: ", len(today_serials))
        input("Press Enter to return...")

    def prescribe_patient(self):
        self._header()
        print("PRESCRIBE PATIENT")
        search = input("Enter Patient Phone or SmartID: ").strip()
        if not search:
            return

        serials = load_data("serials.txt")
        patient = None
        index = -1

        for i, s in enumerate(serials):
            if len(s) < 4: continue
            phone_match = s[2] == search
            smart_id_match = len(s) > 4 and s[4] == search
            
            if (phone_match or smart_id_match):
                patient = s
                index = i
                break

        if not patient:
            print("Patient not found in active serials.")
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
            print(f"Prescribing: {name} | ID: {smart_id}")
            print("-" * 50)
            print(f"Age/Gen : {rx['age']} / {rx['gender']}")
            print(f"Meds    : {len(rx['meds'])} added")
            print(f"Tests   : {len(rx['tests'])} added")
            print("-" * 50)
            print("1. Set Age/Gender")
            print("2. Add Medicine")
            print("3. Add Test")
            print("4. SAVE Prescription")
            print("5. Cancel")
            
            ch = input(">> ").strip()
            
            if ch == '1':
                rx["age"] = input("Age: ").strip()
                rx["gender"] = input("Gender: ").strip()
            elif ch == '2':
                print("--- Add Medicine ---")
                m = input("Name: ")
                if m:
                    d = input("Dose (e.g. 1+0+1): ")
                    dur = input("Duration (e.g. 7 days): ")
                    rx["meds"].append(f"{m} - {d} - {dur}")
            elif ch == '3':
                t = input("Test Name: ")
                if t: rx["tests"].append(t)
            elif ch == '4':
                if not rx["meds"] and not rx["tests"]:
                    if input("Prescription is empty. Save anyway? (y/n): ").lower() != 'y':
                        continue
                
                if input("Confirm Save & Finish? (y/n): ").lower() != 'y':
                    print("Cancelled.")
                    continue
                    
                self.save_rx(rx)
                removed = delete_line("serials.txt", index)
                if removed:
                    append_data("old_patients.txt", "|".join(removed))
                
                print("✓ Prescription saved successfully!")
                input(); break
            elif ch == '5': 
                break

    def save_rx(self, rx):
        formatted_date = format_datetime(rx['date'])
        rec = ""
        rec += f"Name: {rx['name']} │ Phone: {rx['phone']} │ SmartID: {rx['smart_id']}\n"
        rec += f" Visit: {formatted_date} \n"
        
        if rx.get('age'): rec += f"Age: {rx['age']} │ Gender: {rx['gender']}\n"
        
        if rx["meds"]:
            rec += "Medicines:\n" + "\n".join([f"  • {m}" for m in rx["meds"]]) + "\n"
        
        if rx["tests"]:
            rec += "Tests:\n" + "\n".join([f"  • {t}" for t in rx["tests"]]) + "\n"
            
        rec += "═" * 60 + "\n"
        append_data("patients.txt", rec)

    def view_history(self):
        self._header()
        search = input("Enter Patient Phone or SmartID: ").strip()
        if not search:
            input("Invalid input! Press Enter...")
            return

        lines = load_raw_lines("patients.txt")
        if not lines:
            print("No history available.")
            input("Press Enter...")
            return

        full_content = "".join(lines)
        
        separator = "═" * 60
        records = full_content.split(separator)

        found = False
        print(f"\nSearching history for: {search}...\n")

        for rec in records:
            if not rec.strip():
                continue

            if search in rec:
                found = True
                print(rec.strip())
                print(separator)
                print()

        if not found:
            print("No history found for this patient.")

        input("Press Enter to continue...")