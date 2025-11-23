from user import User
from database import (
    load_data, append_data, get_next_id,
    delete_line, format_datetime, generate_smart_id
)
from drug_manager import DrugManager
from datetime import datetime
import sys

class Manager(User):
    def __init__(self, username):
        super().__init__(username)
        self._role = "Manager"
        self.drug_manager = DrugManager(self)

    def show_menu(self):
        while self._is_logged_in:
            self._header()
            print("1. Take Serial 📋")
            print("2. Manage Serials 🗂️")
            print("3. Manage Drugs & Sales 💊")
            print("4. Logout 🔒")
            print("5. Exit 🚪")
            choice = input("\nChoice (1-5): ").strip()

            if choice == '1': self.take_serial()
            elif choice == '2': self.manage_serials()
            elif choice == '3': self.drug_manager.show_menu()
            elif choice == '4': self.logout()
            elif choice == '5': sys.exit(0)
            else: input("\nInvalid! Press Enter...")

    def take_serial(self):
        while True:
            self._header()
            print("TAKE PATIENT SERIAL 📋")
            print("[ Enter '0' or 'q' to Go Back ]")
            print("─" * 30)
            
            name = input("Patient Name: ").strip()
            if name.lower() in ['0', 'q']:
                break
            
            phone = input("Phone: ").strip()

            if not name or not phone or len(phone) < 4:
                print(">> Valid name and phone (min 4 digits) required! ❗")
                input("\nPress Enter to try again..."); continue

            today = datetime.now().strftime('%Y-%m-%d')
            serials = load_data("serials.txt")
            
            if any(s[2] == phone and s[3].startswith(today) for s in serials):
                print(">> Patient already has a serial today! ⚠️")
                input("\nPress Enter to try again..."); continue

            sid = get_next_id("serials.txt")
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            smart_id = generate_smart_id(phone, now_str)

            entry = f"{sid}|{name}|{phone}|{now_str}|{smart_id}"
            append_data("serials.txt", entry)
            
            print(f"\n Serial #{sid} created | Smart ID: {smart_id} ✅")
            input("\nPress Enter for NEXT patient...")

    def manage_serials(self):
        while True:
            self._header()
            print("MANAGE SERIALS 🗂️")
            print("1. View Serials 📋")
            print("2. Cancel Serial ❌")
            print("3. Back ↩️")
            ch = input("\nChoice (1-3): ").strip()
            if ch == '1': self.view_serials()
            elif ch == '2': self.cancel_serial()
            elif ch == '3': break
            else: input("\nInvalid! Press Enter...")

    def view_serials(self):
        self._header()
        data = load_data("serials.txt")
        serials = [d for d in data if len(d) > 3 and d[3]]
        
        if not serials:
            print("No serials today❗")
            input("\nPress Enter...")
            return

        w_id, w_sid, w_name, w_phone, w_time = 3, 7, 16, 13, 25
        header = f"{'ID':<{w_id}} │ {'SmartID':<{w_sid}} │ {'Name':<{w_name}} │ {'Phone':<{w_phone}} │ {'Date & Time':<{w_time}}"
        separator = "─" * len(header)

        print(header)
        print(separator)
        for d in serials:
            smart_id = d[4] if len(d) > 4 else "N/A"
            print(f"{d[0]:<{w_id}} │ {smart_id:<{w_sid}} │ {d[1]:<{w_name}} │ {d[2]:<{w_phone}} │ {format_datetime(d[3]):<{w_time}}")
        input("\nPress Enter...")

    def cancel_serial(self):
            self._header()
            self.view_serials()
            try:
                sid = input("Enter Serial ID to cancel: ").strip()
                data = load_data("serials.txt")
                for i, d in enumerate(data):
                    if d[0] == sid:
                        if input(f"DELETE serial for {d[1]}? (y/n): ").lower() == 'y':
                            delete_line("serials.txt", i)
                            print("\nSerial has been deleted. ✅")
                        else:
                            print("Operation cancelled. ❗")
                        input("\nPress Enter..."); return
                print("Serial not found. ❗")
            except:
                print("Invalid input ❗")
            input("\nPress Enter...")