from user import User
from database import (
    load_data, append_data, 
    load_raw_lines, delete_line, format_datetime, clear_screen)
from datetime import datetime
import sys

class Doctor(User):
    def __init__(self, username):
        super().__init__(username)
        self._role = "Doctor"

    def show_menu(self):
        while self._is_logged_in:
            self._header()
            print("1. View Patient Queue 📋")
            print("2. Prescribe Patient 📝")
            print("3. View History 📜")
            print("4. View Old Patient List 📂")
            print("5. Logout 🔒")
            print("6. Exit 🚪")
            ch = input("\nChoice (1-6): ").strip()
            
            if ch == '1': self.view_patient_queue()
            elif ch == '2': self.prescribe_patient()
            elif ch == '3': self.view_history()
            elif ch == '4': self.view_old_patients()
            elif ch == '5': self.logout()
            elif ch == '6': sys.exit(0)
            else: input("\nInvalid! Press Enter...")

    def view_patient_queue(self):
        self._header()
        print("PATIENT QUEUE 📋")
        
        data = load_data("serials.txt")
        serials = [d for d in data if len(d) > 3 and d[3]]
        
        if not serials:
            print("\nNo patients waiting in queue today. 📋")
            input("\nPress Enter...")
            return

        w_id, w_sid, w_name, w_phone = 4, 8, 18, 14
        header = f"{'SL':<{w_id}} │ {'SmartID':<{w_sid}} │ {'Name':<{w_name}} │ {'Phone':<{w_phone}}"
        separator = "─" * len(header)

        print("\n" + header)
        print(separator)
        
        for i, d in enumerate(serials, 1):
            smart_id = d[4] if len(d) > 4 else "N/A"
            print(f"{i:<{w_id}} │ {smart_id:<{w_sid}} │ {d[1]:<{w_name}} │ {d[2]:<{w_phone}}")
            
        print("\nTotal Waiting: ", len(serials))
        input("Press Enter to return...")

    def prescribe_patient(self):
        self._header()
        print("PRESCRIBE PATIENT 📝")
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
            print("Patient not found in active serials. ❗")
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
            print("1. Set Age/Gender 👤")
            print("2. Add Medicine 📝")
            print("3. Add Test 🧪")
            print("4. SAVE Prescription 💾")
            print("5. Cancel ❌")
            
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
                
                print("Prescription saved successfully! ✅")
                input("\nPress Enter to continue..."); break
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
            print("No history available. ❗")
            input("Press Enter...")
            return

        full_content = "".join(lines)
        separator = "═" * 60
        records = full_content.split(separator)
        
        found_records = []
        for rec in records:
            if rec.strip() and search in rec:
                found_records.append(rec.strip())

        clear_screen()
        print(f" History Results for: {search}")
        print("═" * 50)

        if not found_records:
            print("No history found for this patient. ❗")
        else:
            for rec in found_records:
                print(rec)
                print(separator)
                print()

        input("Press Enter to continue...")

    def view_old_patients(self):
        self._header()
        print("OLD PATIENT RECORDS (Processed) 🕰️")
        
        data = load_data("old_patients.txt")
        if not data:
            print("\nNo old patient records found. ❗")
            input("Press Enter...")
            return

        w_name, w_phone, w_sid, w_date = 20, 15, 10, 25
        header = f"{'Name':<{w_name}} │ {'Phone':<{w_phone}} │ {'SmartID':<{w_sid}} │ {'Visit Date':<{w_date}}"
        separator = "─" * len(header)

        print("\n" + header)
        print(separator)

        for d in data:
            if len(d) < 4: continue
            
            name = d[1]
            phone = d[2]
            visit_time = format_datetime(d[3])
            smart_id = d[4] if len(d) > 4 else "N/A"

            print(f"{name:<{w_name}} │ {phone:<{w_phone}} │ {smart_id:<{w_sid}} │ {visit_time:<{w_date}}")

        print(f"\nTotal Records: {len(data)}")
        input("Press Enter to return...")