from user import User
from database import (
    load_data, save_data, append_data, get_next_id,
    delete_line, format_datetime, generate_smart_id, load_raw_lines)
from datetime import datetime
import sys

class Manager(User):
    def __init__(self, username):
        super().__init__(username)
        self._role = "Manager"

    def show_menu(self):
        while self._is_logged_in:
            self._header()
            print("1. Take Serial")
            print("2. Manage Serials")
            print("3. Manage Drugs & Sales")
            print("4. Logout")
            print("5. Exit")
            choice = input("\nChoice (1-5): ").strip()

            if choice == '1': self.take_serial()
            elif choice == '2': self.manage_serials()
            elif choice == '3': self.drug_menu()
            elif choice == '4': self.logout()
            elif choice == '5': sys.exit(0)
            else: input("Invalid! Press Enter...")

    def take_serial(self):
        self._header()
        name = input("Patient Name: ").strip()
        phone = input("Phone: ").strip()
        if not name or not phone or len(phone) < 4:
            print("Valid name and phone (min 4 digits) required!")
            input(); return

        today = datetime.now().strftime('%Y-%m-%d')
        serials = load_data("serials.txt")
        if any(s[2] == phone and s[3].startswith(today) for s in serials):
            print("Patient already has a serial today!")
            input(); return

        sid = get_next_id("serials.txt")
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        smart_id = generate_smart_id(phone, now_str)

        entry = f"{sid}|{name}|{phone}|{now_str}|{smart_id}"
        append_data("serials.txt", entry)
        print(f"Serial #{sid} created | Smart ID: {smart_id}")
        input("Press Enter...")

    def manage_serials(self):
        while True:
            self._header()
            print("MANAGE SERIALS")
            print("1. View Serials (Today)")
            print("2. Cancel Serial")
            print("3. Back")
            ch = input("Choice (1-3): ").strip()
            if ch == '1': self.view_serials()
            elif ch == '2': self.cancel_serial()
            elif ch == '3': break
            else: input("Invalid! Press Enter...")

    def view_serials(self):
        self._header()
        data = load_data("serials.txt")
        today = datetime.now().strftime('%Y-%m-%d')
        today_serials = [d for d in data if len(d) > 3 and d[3].startswith(today)]
        
        if not today_serials:
            print("No serials today.")
            input("Press Enter...")
            return

        w_id, w_sid, w_name, w_phone, w_time = 3, 7, 16, 13, 25
        header = f"{'ID':<{w_id}} │ {'SmartID':<{w_sid}} │ {'Name':<{w_name}} │ {'Phone':<{w_phone}} │ {'Date & Time':<{w_time}}"
        separator = "─" * len(header)

        print(header)
        print(separator)
        for d in today_serials:
            smart_id = d[4] if len(d) > 4 else "N/A"
            print(f"{d[0]:<{w_id}} │ {smart_id:<{w_sid}} │ {d[1]:<{w_name}} │ {d[2]:<{w_phone}} │ {format_datetime(d[3]):<{w_time}}")
        input("Press Enter...")

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
                            print("Serial has been deleted.")
                        else:
                            print("Operation cancelled.")
                        input(); return
                print("Serial not found.")
            except:
                print("Invalid input!")
            input()

    def drug_menu(self):
        while True:
            self._header()
            print("DRUGS & SALES")
            print("1. Add Drug")
            print("2. Edit Drug")
            print("3. Delete Drug")
            print("4. Sell Drug")
            print("5. View Stock")
            print("6. View Sales")
            print("7. Back")
            ch = input("Choice (1-7): ").strip()
            if ch == '1': self.add_drug()
            elif ch == '2': self.edit_drug()
            elif ch == '3': self.delete_drug()
            elif ch == '4': self.sell_drug()
            elif ch == '5': self.view_stock()
            elif ch == '6': self.view_sales()
            elif ch == '7': break
            else: input("Invalid! Press Enter...")

    def add_drug(self):
        self._header()
        name = input("Drug Name: ").strip()
        qty = input("Quantity: ").strip()
        price = input("Price: ").strip()
        
        expiry = ""
        while True:
            date_input = input("Expiry Date (YYYY-MM-DD): ").strip()
            try:
                exp_date = datetime.strptime(date_input, '%Y-%m-%d')
                if exp_date.date() <= datetime.now().date():
                    print("Error: Expiry date must be a future date (after today).")
                else:
                    expiry = date_input
                    break
            except ValueError:
                print("Invalid format! Use YYYY-MM-DD.")

        if not (name and qty.isdigit() and price.replace('.','').isdigit()):
            print("Invalid input!")
            input(); return
            
        append_data("drugs.txt", f"{name}|{qty}|{price}|{expiry}")
        print(f"Drug added successfully with expiry: {expiry}")
        input()

    def edit_drug(self):
        self._header()
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs.")
            input(); return
        self.view_stock()
        try:
            idx = int(input("Enter Drug ID to edit: ")) - 1
            if idx < 0 or idx >= len(drugs):
                print("Invalid ID!")
                input(); return
            
            curr_exp = drugs[idx][3] if len(drugs[idx]) > 3 else "N/A"
            
            print(f"Current: {drugs[idx][0]} | Qty: {drugs[idx][1]} | ৳{drugs[idx][2]} | Exp: {curr_exp}")
            
            name = input("New Name (enter to keep): ").strip() or drugs[idx][0]
            qty = input("New Qty (enter to keep): ").strip()
            qty = drugs[idx][1] if not qty.isdigit() else qty
            price = input("New Price (enter to keep): ").strip()
            price = drugs[idx][2] if not price.replace('.','').isdigit() else price
            
            new_exp = input("New Expiry YYYY-MM-DD (enter to keep): ").strip()
            final_exp = curr_exp
            if new_exp:
                try:
                    ed = datetime.strptime(new_exp, '%Y-%m-%d')
                    if ed.date() <= datetime.now().date():
                        print("Warning: Date is not in future. Keeping old date.")
                    else:
                        final_exp = new_exp
                except:
                    print("Invalid date format. Keeping old date.")
            
            drugs[idx] = [name, qty, price, final_exp]
            save_data("drugs.txt", drugs)
            print("Drug updated.")
        except:
            print("Invalid input!")
        input()

    def delete_drug(self):
        self._header()
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs.")
            input(); return
        self.view_stock()
        try:
            idx = int(input("Enter Drug ID to delete: ")) - 1
            if idx < 0 or idx >= len(drugs):
                print("Invalid ID!")
                input(); return
            if input(f"Delete {drugs[idx][0]}? (y/n): ").lower() == 'y':
                delete_line("drugs.txt", idx)
                print("Drug deleted.")
            else:
                print("Cancelled.")
        except:
            print("Invalid input!")
        input()

    def sell_drug(self):
        self._header()
        
        print("--- Patient Verification ---")
        search_id = input("Enter Patient Phone or SmartID: ").strip()
        if not search_id:
            print("Patient ID is required to sell drugs!")
            input(); return

        prescribed_meds = self._get_prescribed_meds(search_id)
        
        if not prescribed_meds:
            print("\nNo prescription found for this patient ID in records!")
            print("Cannot sell drugs without a valid doctor's prescription.")
            input(); return

        print(f"\n✓ Prescription Found! Allowed Medicines: {', '.join(prescribed_meds)}")
        input("Press Enter to start selling...")

        while True:
            self._header()
            print(f"Selling to: {search_id}")
            print(f"Rx: {', '.join(prescribed_meds)}")
            print("-" * 50)

            drugs = load_data("drugs.txt")
            if not drugs:
                print("No drugs in stock.")
                input(); return

            w_id, w_name, w_qty, w_price, w_exp = 4, 18, 6, 8, 12
            header = f"{'ID':<{w_id}} │ {'Drug Name':<{w_name}} │ {'Qty':>{w_qty}} │ {'Price':>{w_price}} │ {'Expiry':<{w_exp}}"
            print(header)
            print("─" * len(header))
            for i, d in enumerate(drugs):
                expiry = d[3] if len(d) > 3 else "N/A"
                print(f"{i+1:<{w_id}} │ {d[0]:<{w_name}} │ {d[1]:>{w_qty}} │ ৳{d[2]:>{w_price-2}} │ {expiry:<{w_exp}}")
            print("-" * 50)

            print("Enter Drug ID to sell (or '0' to Finish/Exit):")
            choice = input(">> ").strip()

            if choice == '0' or choice.lower() == 'back':
                break
            
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(drugs):
                    print("Invalid ID! Try again.")
                    input("Press Enter..."); continue
                
                selected_drug_name = drugs[idx][0]
                
                is_prescribed = False
                for med in prescribed_meds:
                    if selected_drug_name.lower() in med.lower():
                        is_prescribed = True
                        break
                
                if not is_prescribed:
                    print(f"\n[!] REJECTED: '{selected_drug_name}' is NOT in the prescription.")
                    input("Press Enter to continue..."); continue

                qty_avail = int(drugs[idx][1])
                if qty_avail <= 0:
                    print("Out of stock!")
                    input("Press Enter..."); continue
                
                qty_input = input(f"Qty (max {qty_avail}): ")
                if not qty_input.isdigit(): 
                    continue
                qty = int(qty_input)

                if qty <= 0 or qty > qty_avail:
                    print("Invalid quantity!")
                    input("Press Enter..."); continue
                
                total = qty * float(drugs[idx][2])
                
                expiry = drugs[idx][3] if len(drugs[idx]) > 3 else "N/A"
                drugs[idx] = [drugs[idx][0], str(qty_avail - qty), drugs[idx][2], expiry]
                
                save_data("drugs.txt", drugs)
                
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
                append_data("sales.txt", f"{selected_drug_name}|{qty}|{total}|{now_str}|{search_id}")
                
                print(f"\n✓ SOLD: {qty}x {selected_drug_name} = ৳{total:.2f}")
                print(f"Remaining Stock: {drugs[idx][1]}")
                input("Press Enter to sell next item...") 

            except ValueError:
                print("Invalid input! Please enter a number.")
                input("Press Enter...")

    def _get_prescribed_meds(self, search_id):
        """Scans patients.txt to find the latest prescription for the given ID"""
        lines = load_raw_lines("patients.txt")
        if not lines: return []

        meds_list = []
        current_block_meds = []
        is_target_patient = False
        in_med_section = False
        
        for line in lines:
            stripped = line.strip()
            
            if "Phone:" in stripped and "SmartID:" in stripped:
                if search_id in stripped:
                    is_target_patient = True
                    current_block_meds = []
                else:
                    is_target_patient = False
                    in_med_section = False

            if is_target_patient:
                if stripped.startswith("Medicines:"):
                    in_med_section = True
                    continue
                if stripped.startswith("Tests:") or stripped.startswith("═" * 20):
                    in_med_section = False
                
                if in_med_section and stripped.startswith("•"):
                    parts = stripped.replace("•", "").strip().split("-")
                    if parts:
                        med_name = parts[0].strip()
                        current_block_meds.append(med_name)
        return current_block_meds

    def view_stock(self):
        self._header()
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs.")
        else:
            w_id, w_name, w_qty, w_price, w_exp = 4, 18, 6, 8, 12
            header = f"{'ID':<{w_id}} │ {'Drug Name':<{w_name}} │ {'Qty':>{w_qty}} │ {'Price':>{w_price}} │ {'Expiry':<{w_exp}}"
            separator = "─" * len(header)
            print(header)
            print(separator)
            for i, d in enumerate(drugs):
                expiry = d[3] if len(d) > 3 else "N/A"
                print(f"{i+1:<{w_id}} │ {d[0]:<{w_name}} │ {d[1]:>{w_qty}} │ ৳{d[2]:>{w_price-2}} │ {expiry:<{w_exp}}")
        input("Press Enter...")

    def view_sales(self):
        self._header()
        sales = load_data("sales.txt")
        if not sales:
            print("No sales.")
        else:
            w_drug, w_qty, w_total, w_time = 20, 6, 12, 25
            header = f"{'Drug':<{w_drug}} │ {'Qty':>{w_qty}} │ {'Total':>{w_total}} │ {'Date & Time':<{w_time}}"
            separator = "─" * len(header)
            print(header)
            print(separator)
            for s in sales:
                if len(s) >= 4:
                    total = float(s[2])
                    print(f"{s[0]:<{w_drug}} │ {s[1]:>{w_qty}} │ ৳{total:>{w_total-2}.2f} │ {format_datetime(s[3]):<{w_time}}")
        input("Press Enter...")