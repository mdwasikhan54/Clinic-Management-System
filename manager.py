from user import User
from database import (
    load_data, save_data, append_data, get_next_id,
    delete_line, format_datetime, generate_smart_id)
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
                    if input(f"Cancel {d[1]}? (y/n): ").lower() == 'y':
                        removed = delete_line("serials.txt", i)
                        print("Serial cancelled and moved to old patients.")
                    else:
                        print("Cancelled.")
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
        if not (name and qty.isdigit() and price.replace('.','').isdigit()):
            print("Invalid input!")
            input(); return
        append_data("drugs.txt", f"{name}|{qty}|{price}")
        print("Drug added.")
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
            print(f"Current: {drugs[idx][0]} | {drugs[idx][1]} | ৳{drugs[idx][2]}")
            name = input("New Name (enter to keep): ").strip() or drugs[idx][0]
            qty = input("New Qty (enter to keep): ").strip()
            qty = drugs[idx][1] if not qty.isdigit() else qty
            price = input("New Price (enter to keep): ").strip()
            price = drugs[idx][2] if not price.replace('.','').isdigit() else price
            drugs[idx] = [name, qty, price]
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
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs.")
            input(); return
        self.view_stock()
        try:
            idx = int(input("Select ID: ")) - 1
            if idx < 0 or idx >= len(drugs):
                print("Invalid ID!")
                input(); return
            qty_avail = int(drugs[idx][1])
            if qty_avail <= 0:
                print("Out of stock!")
                input(); return
            qty = int(input(f"Qty (max {qty_avail}): "))
            if qty <= 0 or qty > qty_avail:
                print("Invalid quantity!")
                input(); return
            total = qty * float(drugs[idx][2])
            drugs[idx][1] = str(qty_avail - qty)
            save_data("drugs.txt", drugs)
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            append_data("sales.txt", f"{drugs[idx][0]}|{qty}|{total}|{now_str}")
            print(f"Sold: ৳{total:.2f} | Remaining: {drugs[idx][1]}")
        except:
            print("Invalid input!")
        input()

    def view_stock(self):
        self._header()
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs.")
        else:
            w_id, w_name, w_qty, w_price = 4, 20, 6, 10
            header = f"{'ID':<{w_id}} │ {'Drug Name':<{w_name}} │ {'Qty':>{w_qty}} │ {'Price':>{w_price}}"
            separator = "─" * len(header)
            print(header)
            print(separator)
            for i, d in enumerate(drugs):
                print(f"{i+1:<{w_id}} │ {d[0]:<{w_name}} │ {d[1]:>{w_qty}} │ ৳{d[2]:>{w_price-2}}")
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