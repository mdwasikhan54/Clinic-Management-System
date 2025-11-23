from database import (
    clear_screen, load_data, save_data, append_data, 
    delete_line, format_datetime, load_raw_lines
)
from datetime import datetime

class DrugManager:
    def __init__(self, user_context):
        self.user = user_context

    def show_menu(self):
        while True:
            self.user._header()
            print("DRUGS & SALES 💊")
            print("1. Add Drug 💊")
            print("2. Edit Drug ✏️")
            print("3. Delete Drug 🗑️")
            print("4. Sell Drug 💵")
            print("5. View Stock 📦")
            print("6. Sales Reports 📊")
            print("7. Back ↩️")
            
            ch = input("\nChoice (1-7): ").strip()
            if ch == '1': self.add_drug()
            elif ch == '2': self.edit_drug()
            elif ch == '3': self.delete_drug()
            elif ch == '4': self.sell_drug()
            elif ch == '5': self.view_stock()
            elif ch == '6': self.sales_menu()
            elif ch == '7': break
            else: input("\nInvalid! Press Enter... ❗")

    def add_drug(self):
        self.user._header()
        print("ADD NEW DRUG 💊")
        name = input("Drug Name: ").strip()
        qty = input("Quantity: ").strip()
        price = input("Price: ").strip()
        
        expiry = input("Expiry Date (YYYY-MM-DD): ").strip()
        try:
            if datetime.strptime(expiry, '%Y-%m-%d').date() <= datetime.now().date():
                print("Error: Date must be in the future! ❗")
                input("\nPress Enter..."); return
        except ValueError:
            print("Invalid format! Use YYYY-MM-DD. ❗")
            input("\nPress Enter..."); return

        if name and qty.isdigit() and price.replace('.','').isdigit():
            append_data("drugs.txt", f"{name}|{qty}|{price}|{expiry}")
            print(f"Drug added successfully! ✅")
        else:
            print("Invalid input values! ❗")
        input("\nPress Enter...")

    def edit_drug(self):
        self.user._header()
        drugs = load_data("drugs.txt")
        if not drugs:
            print("No drugs found."); input("\nPress Enter..."); return
            
        self._render_stock_table(drugs)
        try:
            idx = int(input("\nEnter Drug ID to edit: ")) - 1
            if not (0 <= idx < len(drugs)): raise ValueError
            
            d = drugs[idx]
            print(f"Editing: {d[0]} (Enter to keep current value)")
            
            name = input(f"Name ({d[0]}): ").strip() or d[0]
            qty = input(f"Qty ({d[1]}): ").strip() or d[1]
            price = input(f"Price ({d[2]}): ").strip() or d[2]
            expiry = input(f"Exp ({d[3]}): ").strip() or d[3]
            
            drugs[idx] = [name, qty, price, expiry]
            save_data("drugs.txt", drugs)
            print("Drug updated successfully! ✅")
        except:
            print("Invalid ID or Input! ❗")
        input("\nPress Enter...")

    def delete_drug(self):
        self.user._header()
        drugs = load_data("drugs.txt")
        if not drugs: print("No drugs."); input("\nPress Enter..."); return
        
        self._render_stock_table(drugs)
        try:
            idx = int(input("\nEnter Drug ID to delete: ")) - 1
            if 0 <= idx < len(drugs):
                if input(f"Delete '{drugs[idx][0]}'? (y/n): ").lower() == 'y':
                    delete_line("drugs.txt", idx)
                    print("Deleted successfully! ✅")
            else: print("Invalid ID! ❗")
        except: print("Invalid Input! ❗")
        input("\nPress Enter...")

    def sell_drug(self):
        self.user._header()
        print("--- Patient Verification ---")
        pid = input("Enter Patient Phone or SmartID: ").strip()
        meds = self._get_prescribed_meds(pid)
        
        if not meds:
            print("\nNo valid prescription found for this ID! ❌")
            input("\nCannot sell without prescription. Press Enter..."); return

        print(f"\n✓ Prescription Found! Allowed: {', '.join(meds)}")
        input("\nPress Enter to start selling... ✅")

        while True:
            self.user._header()
            print(f"Selling to: {pid} | Rx: {', '.join(meds)}")
            print("-" * 50)
            drugs = load_data("drugs.txt")
            if not drugs: print("Stock Empty!"); break
            
            self._render_stock_table(drugs)
            
            ch = input("Enter Drug ID to sell (0 to Finish): ").strip()
            if ch == '0': break
            
            try:
                idx = int(ch) - 1
                if not (0 <= idx < len(drugs)): continue
                
                drug = drugs[idx]
                drug_name, stock, price = drug[0], int(drug[1]), float(drug[2])
                
                if not any(m.lower() in drug_name.lower() for m in meds):
                    print(f"\n[!] REJECTED: '{drug_name}' is NOT in prescription! ❌")
                    input("\nPress Enter..."); continue
                
                qty = int(input(f"Quantity (Avail: {stock}): "))
                if 0 < qty <= stock:
                    total = qty * price
                    drugs[idx][1] = str(stock - qty)
                    save_data("drugs.txt", drugs)
                    now = datetime.now().strftime('%Y-%m-%d %H:%M')
                    append_data("sales.txt", f"{drug_name}|{qty}|{total}|{now}|{pid}")
                    
                    print(f"\n✓ SOLD: {qty}x {drug_name} = ৳{total:.2f} ✅")
                    input("\nPress Enter to sell next...")
                else:
                    print("Invalid Quantity! ❗"); input("\nPress Enter...")
            except ValueError:
                print("Invalid Input! ❗"); input("\nPress Enter...")

    def _get_prescribed_meds(self, pid):
        """Scans patients.txt for the latest prescription block for the PID"""
        lines = load_raw_lines("patients.txt")
        meds = []
        is_target = False
        
        for line in lines:
            clean = line.strip()
            if "Phone:" in clean and "SmartID:" in clean:
                if pid in clean:
                    is_target = True
                    meds = []
                else:
                    is_target = False
            
            if is_target and clean.startswith("•"):
                parts = clean.replace("•", "").split("-")
                if parts: meds.append(parts[0].strip())
                
        return meds

    def view_stock(self):
        self.user._header()
        print("CURRENT STOCK 📦")
        drugs = load_data("drugs.txt")
        self._render_stock_table(drugs)
        input("\nPress Enter...")

    def _render_stock_table(self, drugs):
        if not drugs: print("No drugs in stock."); return
        w_id, w_nm, w_qt, w_pr, w_ex = 4, 18, 6, 8, 12
        header = f"{'ID':<{w_id}} │ {'Drug Name':<{w_nm}} │ {'Qty':>{w_qt}} │ {'Price':>{w_pr}} │ {'Expiry':<{w_ex}}"
        print(header + "\n" + "─" * len(header))
        for i, d in enumerate(drugs):
            exp = d[3] if len(d)>3 else "N/A"
            print(f"{i+1:<{w_id}} │ {d[0]:<{w_nm}} │ {d[1]:>{w_qt}} │ ৳{d[2]:>{w_pr-2}} │ {exp:<{w_ex}}")

    def sales_menu(self):
        while True:
            self.user._header()
            print("SALES REPORTS 📊")
            print("1. All Sales Log 📝")
            print("2. Summary (By Medicine) 💊")
            print("3. By Date 📅")
            print("4. Back ↩️")
            
            ch = input("\nChoice (1-4): ").strip()
            if ch == '1': self.view_all_sales()
            elif ch == '2': self.view_sales_summary()
            elif ch == '3': self.view_sales_by_date()
            elif ch == '4': break

    def view_all_sales(self):
        self.user._header()
        print("ALL SALES LOG 📝")
        sales = load_data("sales.txt")
        self._render_sales_table(sales)
        input("Press Enter...")

    def view_sales_summary(self):
        self.user._header()
        print("TOTAL SALES SUMMARY (Item-wise) 💊")
        sales = load_data("sales.txt")
        if not sales: print("No sales records."); input(); return

        report = {}
        for s in sales:
            if len(s) < 3: continue
            name, qty, amt = s[0], int(s[1]), float(s[2])
            if name not in report: report[name] = [0, 0.0]
            report[name][0] += qty
            report[name][1] += amt

        w_nm, w_qt, w_tot = 25, 10, 15
        print(f"\n{'Drug Name':<{w_nm}} │ {'Tot Qty':>{w_qt}} │ {'Tot Sales':>{w_tot}}")
        print("─" * (w_nm + w_qt + w_tot + 6))
        
        grand_total = 0
        for name, data in report.items():
            print(f"{name:<{w_nm}} │ {data[0]:>{w_qt}} │ ৳{data[1]:>{w_tot-2}.2f}")
            grand_total += data[1]
            
        print("-" * (w_nm + w_qt + w_tot + 6))
        print(f"{'GRAND TOTAL':<{w_nm}} │ {' ':>{w_qt}} │ ৳{grand_total:>{w_tot-2}.2f}")
        input("\nPress Enter...")

    def view_sales_by_date(self):
        self.user._header()
        date_in = input("Enter Date (YYYY-MM-DD): ").strip()
        sales = load_data("sales.txt")
        clear_screen()
        
        filtered = [s for s in sales if len(s)>3 and s[3].startswith(date_in)]
        
        if not filtered:
            print(f"\nNo sales found for {date_in} 📅")
        else:
            print(f"REPORT FOR: {date_in} 📅\n")
            self._render_sales_table(filtered)
            day_total = sum(float(s[2]) for s in filtered)
            print("-" * 70)
            print(f"Total Day Sales: ৳{day_total:.2f}")
            
        input("Press Enter...")

    def _render_sales_table(self, sales):
        if not sales: print("No records found."); return
        w_dg, w_qt, w_tt, w_tm = 20, 6, 12, 22
        header = f"{'Drug':<{w_dg}} │ {'Qty':>{w_qt}} │ {'Total':>{w_tt}} │ {'Time':<{w_tm}}"
        print(header + "\n" + "─" * len(header))
        for s in sales:
            if len(s) >= 4:
                print(f"{s[0]:<{w_dg}} │ {s[1]:>{w_qt}} │ ৳{float(s[2]):>{w_tt-2}.2f} │ {format_datetime(s[3]):<{w_tm}}")